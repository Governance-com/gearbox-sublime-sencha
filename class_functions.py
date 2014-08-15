import sublime, sublime_plugin, os, re, glob, itertools, json, os.path, sys, time;
from sublime import Region;

try:
	# python 3 / Sublime Text 3
	from .libs.ClassFunctions import ClassFunctions
	from .libs.JsDuck import JsDuck
	from .libs.Settings import Settings
except ValueError:
	# python 2 / Sublime Text 2
	from libs.ClassFunctions import ClassFunctions
	from libs.JsDuck import JsDuck
	from libs.Settings import Settings

def isJavascriptFile(view):
	return view.score_selector(0, Settings.get('syntax_scopes', 'source.js')) > 0

class ClassBase(sublime_plugin.TextCommand):

	# Returns the activelly open file path from sublime.
	def active_file_path(self):
		file_path = self.view.file_name()

		if file_path and len(file_path) > 0:
			return file_path

	def window(self):
		return self.view.window();

class ClassFuncBase(ClassBase):
	def run(self, edit):
		if not isJavascriptFile(self.view):
			sublime.status_message('Active file is not a javascript file.');
			return;

		active_file_path = self.active_file_path()
		self._funcs = ClassFunctions(sublime, active_file_path)
		
		if not self._funcs.isValid():
			sublime.status_message('Active file path does not contain project.');
			return;

		JsDuck.checkJsDuck(sublime, self._funcs.appRoot());
		if JsDuck.isActive(): 
			sublime.status_message('JsDuck is active...');
			return;

		if active_file_path:
			self.load();

			self.window().show_quick_panel(self._funcs.descriptions(), self.open_file)
		else:
			sublime.status_message("No open file")

	# Opens the file in path.
	def open_file(self, index):
		if index >= 0 and len(self._funcs.descriptions()) > index:
			curEntry = self._funcs.descriptions()[index]
			self.open(curEntry);
		# else:
		# 	sublime.status_message("Nothing found")

	def load(self):
		pass

	def open(self, curEntry):
		pass

class ClassFunctionsCommand(ClassFuncBase):
	def load(self):
		self._funcs.readJsDuckFunctions();

	def open(self, curEntry):
		curFunction = curEntry[0];
		curClass = curEntry[1];

		# path = self._funcs.classNameToPath(curClass);
		# if not os.path.exists(path):
		# 	sublime.status_message('Source file not found.');
		# 	return;
		# lineIndex = self._getFunctionLine(path, curFunction)

		# path = path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]);
		path = self._funcs.files()[curClass + ':' + curFunction];
		sublime.set_timeout(lambda: self.window().open_file(path, sublime.ENCODED_POSITION))

	# we may fallback on this code later.
	def _getFunctionLine(self, filepath, name):
		lineNumber = 0;
		f = open(filepath, 'r', encoding="utf-8");
		functionRegex = re.compile('^\s*' + name + '\s*:\s*((function\s*\()|(Ext\.emptyFn))');
		result = [0, 0];
		while(True):
			lineNumber += 1;
			line = f.readline();
			if line:
				match = functionRegex.search(line)
				if match:
					result = [lineNumber, match.start() + 1];
					break;
			else:
				break;
		f.close();
		return result;

class ClassPropertiesCommand(ClassFuncBase):
	def load(self):
		self._funcs.readJsDuckProperties();

	# Opens the file in path.
	def open(self, curEntry):
		curProperty = curEntry[0];
		curClass = curEntry[1];

		# path = self._funcs.classNameToPath(curClass);
		# if not os.path.exists(path):
		# 	sublime.status_message('Source file not found.');
		# 	return;
		# lineIndex = self._getPropertyLine(path, curProperty)

		# filepath = path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]);

		# TRANSIENT makes it more confusing.
		# view = sublime.set_timeout(lambda: self.window.open_file(filepath), sublime.ENCODED_POSITION | sublime.TRANSIENT))
		path = self._funcs.files()[curClass + ':' + curProperty];
		view = sublime.set_timeout(lambda: self.window().open_file(path, sublime.ENCODED_POSITION))

	# we may fallback on this code later.
	def _getPropertyLine(self, filepath, name):
		lineNumber = 0;
		f = open(filepath, 'r', encoding="utf-8");
		# ^\s*[a-z][a-z0-9]+\s*:\s*([[{\'"]|null|[0-9.]+|false|true)
		# ^\s*[a-zA-z0-9]+\s*:\s*('.*'|".*"|null|[0-9.]+|false|true)
		propertyRegex = re.compile('^\s*' + name + '\s*:\s*([[{\'"]|null|[0-9.]+|false|true)');
		result = [0, 0];
		while(True):
			lineNumber += 1;
			line = f.readline();
			if line:
				match = propertyRegex.search(line)
				if match:
					result = [lineNumber, match.start() + 1];
					break;
			else:
				break;
		f.close();
		return result;

class ClassPropertiesInsertCommand(ClassPropertiesCommand):

	def open(self, curEntry):
		curProperty = curEntry[0];
		curClass = curEntry[1];

		propertyType = self._funcs.types()[curClass + ':' + curProperty];
		template = Settings.get('propertyTemplates.' + propertyType, Settings.get('propertyTemplates.String'));
		template = '\n'.join(template);
		template = template.replace('<name>', curProperty);
		
		self.view.run_command('insert_snippet', { "contents": template });

class ClassFunctionsInsertCommand(ClassFunctionsCommand):
	def open(self, curEntry):
		curFunction = curEntry[0];
		curClass = curEntry[1];

		template = Settings.get('functionTemplate');
		template = '\n'.join(template);
		template = template.replace('<name>', curFunction);
		
		self.view.run_command('insert_snippet', { "contents": template });

class ClassRelatedClassesCommand(ClassFuncBase):
	def load(self):
		self._funcs.readJsDuckRelatedClasses();

	# Opens the file in path.
	def open(self, curEntry):
		curClass = curEntry[0];
		curGroup = curEntry[1];

		filepath = self._funcs.classNameToPath(curClass);
		if not os.path.exists(filepath):
			sublime.status_message('Source file not found.');
			return;
		
		# TRANSIENT makes it more confusing.
		# view = sublime.set_timeout(lambda: self.window.open_file(filepath), sublime.ENCODED_POSITION | sublime.TRANSIENT))
		view = sublime.set_timeout(lambda: self.window().open_file(filepath, 0))

class RebuildJsduckCommand(ClassBase):
	def run(self, edit):
		active_file_path = self.active_file_path();

		root = JsDuck.detectRoot(sublime, active_file_path);
		if not root:
			sublime.status_message('Active file path does not contain project.');
			return;

		if JsDuck.isActive(): 
			sublime.status_message('JsDuck is already active...');
			return;

		JsDuck.buildJsDuck(sublime, root);
	
# Disabled until properly fixed.	
# class RebuildJsduckFileCommand(ClassBase):
# 	def run(self):
# 		active_file_path = self.active_file_path();

# 		if JsDuck.isActive(): 
# 			sublime.status_message('JsDuck is already active...');
# 			return;

# 		self._funcs = ClassFunctions(sublime, active_file_path);
		
# 		if not self._funcs.isValid():
# 			sublime.status_message('Invalid file.');
# 			return;

# 		JsDuck.updateJsDuck(sublime, self._funcs.appRoot(), active_file_path, self._funcs.className());

class RestartSublimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		curdir = os.path.dirname(os.path.realpath(__file__));
		if sys.platform == 'win32':
			os.execl(sys.executable, '');
		else:
			if sys.platform == 'darwin':
				os.chmod(os.path.join(curdir, 'restartsublime_mac.sh'), 1877); # 755
				os.execl(os.path.join(curdir, 'restartsublime_mac.sh'), '');
			else:
				os.chmod(os.path.join(curdir, 'restartsublime_mac.sh'), 1877); # 755
				os.execl(os.path.join(curdir, 'restartsublime_linux.sh'), '');
		# #!/bin/bash
		# killall 'Sublime Text'
		# /Applications/Sublime\ Text.app/Contents/MacOS/Sublime\ Text
		# os.execl(os.path.join(curdir, 'restartsublime_mac.sh'), '');



lastRun = time.time(); # Don't run directly after editting first file.
scheduled = False;
scheduleAgain = False;
class ChangeListener(sublime_plugin.EventListener):

	def __timeTillNext(self):
		global lastRun;
		if lastRun > (time.time() - Settings.get('autoUpdate.interval', 120)):
			return lastRun - (time.time() - Settings.get('autoUpdate.interval', 120));
		else:
			return 0; # run now!

	def on_pre_save(self, view):
		global scheduled, lastRun;
		print('OnPreSave', view.file_name());
		if not view.is_dirty(): # No changes, not important.
			print('not dirty');
			return;

		if not isJavascriptFile(view): # only js files.
			print('not js');
			return;

		if not Settings.get('autoUpdate.enabled', False):
			print('not enabled');
			return;

		filePath = view.file_name();
		func = ClassFunctions(sublime, filePath);
		if not func.isValid(): # not valid.
			print('not valid')
			return;

		print('Just before save');
		if scheduled:
			return;
		elif JsDuck.isActive():
			scheduled = True;
			lastRun = time.time();
			sublime.set_timeout(lambda: self.__doUpdate(filePath), self.__timeTillNext() * 1000);
			print('scheduled');
		else:
			print('Running now');
			self.__doUpdate(filePath);

	def __doUpdate(self, filePath):
		global lastRun;
		lastRun = time.time();
		root = JsDuck.detectRoot(sublime, filePath);
		sublime.set_timeout(lambda: JsDuck.buildJsDuck(sublime, root), 10)