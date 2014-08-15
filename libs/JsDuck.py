import threading, os, os.path, subprocess, sys, re, json

from .threadprogress import ThreadProgress 

JsDuckActiveTask = None
ClassPaths = {};

class JsDuckBuild(object):
	def __init__(self, sublime, curRoot):
		self.__sublime = sublime;
		self.__root = curRoot;
		self.__duckduckpath = JsDuck.detectJsDuck(sublime, curRoot);
		self.__thread = threading.Thread(None, lambda: self.run());
		self.__thread.start();

	def thread(self):
		return self.__thread;

	def run(self):
		global JsDuckActiveTask;
		self.__progress = ThreadProgress(self.__thread, 'JsDuck building', 'JsDuck finished building');

		# print('Start jsduck build');
		try:
			os.stat(self.__duckduckpath)
		except:
			os.mkdir(self.__duckduckpath) 

		# try:
		# 	os.stat(os.path.join(self.__duckduckpath, 'docs'))
		# except:
		# 	os.mkdir(os.path.join(self.__duckduckpath, 'docs')) 

		# Use /bin/bash -l to be compatible with ruby 1.9, 2.0 installs gems in /usr/bin
		args = ['/bin/bash -l -c "jsduck'];
		args = args + JsDuck.getSettings(self.__sublime, 'jsduckbuildpaths')
		args = args + JsDuck.getSettings(self.__sublime, 'jsduckargs')
		args.append('--output ' + JsDuck.getJsDuckPath(self.__duckduckpath));
		args.append("\"");
		# command = ' '.join(args);
		print(' '.join(args));

		# Please do not change this, thank you.
		# Start -- 
		p = subprocess.Popen(' '.join(args), cwd=self.__root, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE);
		output = '';
		for line in iter(p.stdout.readline, b''):
			print(line);
		p.communicate();
		# End --
		
		# print('Finished jsduck build');
		# self.__sublime.status_message('Finished building jsduck');
		self.__thread.result = True;
		JsDuckActiveTask = None;

# class JsDuckUpdate(object):
# 	def __init__(self, sublime, curRoot, curFile, className):
# 		self.__sublime = sublime;
# 		self.__root = curRoot;
# 		self.__cur_file = curFile;
# 		self.__classname = className;
# 		self.__duckduckpath = JsDuck.detectJsDuck(sublime, curRoot);
# 		self.__thread = threading.Thread(None, lambda: self.run());
# 		self.__thread.start();

# 	def thread(self):
# 		return self.__thread;
	
# 	def run(self):
# 		global JsDuckActiveTask;
# 		self.__progress = ThreadProgress(self.__thread, 'JsDuck updating', 'JsDuck finished updating');
# 		# print('Start jsduck update', self.__cur_file[len(self.__root) + 1:]);
# 		try:
# 			os.stat(self.__duckduckpath)
# 		except:
# 			os.mkdir(self.__duckduckpath) 

# 		try:
# 			os.stat(os.path.join(self.__duckduckpath, 'tempdocs'))
# 		except:
# 			os.mkdir(os.path.join(self.__duckduckpath, 'tempdocs')) 

# 		args = ['jsduck'];
# 		# args.append(self.__cur_file);
# 		args = args + JsDuck.getSettings(self.__sublime, 'jsduckbuildpaths')
# 		args = args + JsDuck.getSettings(self.__sublime, 'jsduckargs');
# 		# args.append('--output ' + os.path.join(self.__duckduckpath, 'docs'));
# 		args.append('--output=-');
# 		args.append('1> ' + os.path.join(self.__duckduckpath, 'tempdocs', self.__classname + '.json'))

# 		# command = ' '.join(args);
# 		print(' '.join(args));

# 		# Please do not change this, thank you.
# 		# Start -- 
# 		p = subprocess.Popen(' '.join(args), cwd=self.__root, shell=True, stderr=subprocess.PIPE);
# 		output = '';
# 		for line in iter(p.stderr.readline, b''):
# 			print(line);
# 		p.communicate();
# 		# End --
		
# 		# print('Finished jsduck update', self.__cur_file[len(self.__root) + 1:]);
# 		# self.__sublime.status_message('Finished updating jsduck for ' + self.__cur_file[len(self.__root) + 1:]);
# 		self.__thread.result = True;
# 		JsDuckActiveTask = None;

class JsDuck(object):

	@staticmethod
	def isActive():
		global JsDuckActiveTask;
		# Fix for floating tasks, just a security measure for errors.
		if JsDuckActiveTask and JsDuckActiveTask.thread():
			if not JsDuckActiveTask.thread().isAlive():
				JsDuckActiveTask = None;

		return JsDuckActiveTask != None

	@staticmethod
	def checkJsDuck(sublime, curRoot):
		if JsDuck.isActive():
			return False;

		if curRoot == None:
			return False;

		duckduckpath = JsDuck.detectJsDuck(sublime, curRoot);
		if os.path.exists(JsDuck.getJsDuckPath(duckduckpath)):
			return True;
		
		JsDuck.buildJsDuck(sublime, curRoot);

		return True;

	@staticmethod
	def buildJsDuck(sublime, curRoot):
		global JsDuckActiveTask;
		if JsDuck.isActive():
			sublime.status_message('A jsduck task is already running');
			return;
		JsDuckActiveTask = JsDuckBuild(sublime, curRoot);
		sublime.status_message('Building jsduck...');

	# @staticmethod
	# def updateJsDuck(sublime, curRoot, curFile, className):
	# 	global JsDuckActiveTask;
	# 	if JsDuck.isActive():
	# 		sublime.status_message('A jsduck task is already running');
	# 		return;
	# 	JsDuckActiveTask = JsDuckUpdate(sublime, curRoot, curFile, className);
	# 	sublime.status_message('Updating jsduck: ' + curFile);

	@staticmethod
	def detectRoot(sublime, curFile):
		folders = sublime.active_window().folders();
		curFolder = None;
		for folder in folders:
			if curFile.startswith(os.path.join(folder, '')) :
				curFolder = folder
				break;

		if not curFolder:
			return None;

		settings = JsDuck.getSettings(sublime, 'applicationPaths');
		for path in settings:
			if os.path.exists(curFolder + path + '/app') :
				return curFolder + path;

		return None;

	# Make configurable ?
	@staticmethod
	def detectExt(sublime, curRoot):
		return os.path.join(curRoot, 'ext');

	@staticmethod
	def detectJsDuck(sublime, curRoot):
		if not curRoot:
			return None;

		settings = JsDuck.getSettings(sublime, 'jsduckPaths');
		for path in settings:
			if os.path.exists(os.path.join(curRoot, path, 'json')) :
				return os.path.join(curRoot, path);

		return os.path.join(curRoot, settings[0]);

	@staticmethod
	def getJsDuckPath(docsRoot):
		return os.path.join(docsRoot, 'json');

	@staticmethod
	def getSettings(sublime, name):
		# global settings;
		# default settings
		setting = sublime.load_settings('Gearbox.sublime-settings').get(name).copy()

		# per project settings
		if sublime.active_window().active_view().settings().get('Gearbox'):
			setting.update(sublime.active_window().active_view().settings().get('Gearbox').get(name))

		return setting;

	@staticmethod
	def loadClassPaths(sublime, curRoot):
		global ClassPaths;
		if ClassPaths.get(curRoot, None) == False:
			return None;

		# addClassPathMappings\(([^;])+\)
		if not os.path.exists(os.path.join(curRoot, 'bootstrap.js')):
			return None;

		f = open(os.path.join(curRoot, 'bootstrap.js'), 'r', encoding="utf-8")
		data = f.read();
		f.close()

		match = re.search('addClassPathMappings\(([^;]+)\)', data)
		if not match:
			# Loading error
			ClassPaths = False;
			return None;

		parsedJson = json.loads(match.group(1));
		parsedList = [];
		for key, value in parsedJson.items():
			parsedList.append([ key, value ]);

		parsedList = sorted(parsedList, key=lambda entry: -len(entry[0].split('.')));
		ClassPaths[curRoot] = parsedList;
		print(parsedList);
		return parsedList;

	@staticmethod
	def classNameToPath(sublime, curRoot, className):
		global ClassPaths;
		if not ClassPaths.get(curRoot, None):
			if not JsDuck.loadClassPaths(sublime, curRoot):
				return '';

		parsedPath = className;

		for path, filePath in ClassPaths.get(curRoot):
			if not className.startswith(path):
				continue;
			if className == path: ## fully represented;
				parsedPath = filePath;
			else:
				parts = className[len(path) + 1:].split('.');
				parts.insert(0, filePath);
				parsedPath = os.sep.join(parts);

			break;
		if not parsedPath.endswith('.js'):
			parsedPath += '.js';

		return os.path.join(curRoot, parsedPath);











