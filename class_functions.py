import sublime, sublime_plugin, os, re, glob, itertools, json, os.path, sys

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.join(os.path.dirname(__file__), 'libs')

if __path__ not in sys.path:
	sys.path.insert(0, __path__)

from ClassFunctions import ClassFunctions
from JsDuckDuck import JsDuck

class ClassBase(sublime_plugin.WindowCommand):

	# Returns the activelly open file path from sublime.
	def active_file_path(self):
		if self.window.active_view():
			file_path = self.window.active_view().file_name()

			if file_path and len(file_path) > 0:
				return file_path

class ClassFuncBase(ClassBase):
	def run(self, index=None):
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

			# print(self.__funcs.descriptions())
			if index != None:
				self.open_file(index)
			else:
				self.window.show_quick_panel(self._funcs.descriptions(), self.open_file)
		else:
			sublime.status_message("No open files")

	# Opens the file in path.
	def open_file(self, index):
		if index >= 0 and len(self._funcs.descriptions()) > index:
			curEntry = self._funcs.descriptions()[index]
			self.open(curEntry);
		else:
			sublime.status_message("Nothing found")

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

		path = self._funcs.classNameToPath(curClass);
		if not os.path.exists(path):
			sublime.status_message('Source file not found.');
			return;
		lineIndex = self._getFunctionLine(path, curFunction)

		path = path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]);
		sublime.set_timeout(lambda: self.window.open_file(path, sublime.ENCODED_POSITION))

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

		path = self._funcs.classNameToPath(curClass);
		if not os.path.exists(path):
			sublime.status_message('Source file not found.');
			return;
		lineIndex = self._getPropertyLine(path, curProperty)

		filepath = path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]);

		# TRANSIENT makes it more confusing.
		# view = sublime.set_timeout(lambda: self.window.open_file(filepath), sublime.ENCODED_POSITION | sublime.TRANSIENT))
		view = sublime.set_timeout(lambda: self.window.open_file(filepath, sublime.ENCODED_POSITION))

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
		view = sublime.set_timeout(lambda: self.window.open_file(filepath, 0))

class RebuildJsduckCommand(ClassBase):
	def run(self):
		active_file_path = self.active_file_path();

		root = JsDuck.detectRoot(sublime, active_file_path);
		if not root:
			sublime.status_message('Active file path does not contain project.');
			return;

		if JsDuck.isActive(): 
			sublime.status_message('JsDuck is already active...');
			return;

		JsDuck.buildJsDuck(sublime, root);
		
class RebuildJsduckFileCommand(ClassBase):
	def run(self):
		active_file_path = self.active_file_path();

		if JsDuck.isActive(): 
			sublime.status_message('JsDuck is already active...');
			return;

		self._funcs = ClassFunctions(sublime, active_file_path);
		
		if not self._funcs.isValid():
			sublime.status_message('Invalid file.');
			return;

		JsDuck.updateJsDuck(sublime, self._funcs.appRoot(), active_file_path, self._funcs.className());

class RestartSublimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# #!/bin/bash
		# killall 'Sublime Text'
		# /Applications/Sublime\ Text.app/Contents/MacOS/Sublime\ Text
		os.execl('/Users/admin/restartsublime.sh', '');
