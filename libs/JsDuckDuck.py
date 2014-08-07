import threading, os, os.path, subprocess, sys

JsDuckUpdate = None

class JsDuck(object):

	def __init__(self, sublime, curRoot):
		self.__sublime = sublime;
		self.__root = curRoot;
		self.__duckduckpath = JsDuck.detectJsDuck(sublime, curRoot);
		self.__thread = threading.Thread(None, lambda: self.run());
		self.__thread.start();

	def run(self):
		global JsDuckUpdate;
		print('Start jsduck');
		try:
			os.stat(self.__duckduckpath)
		except:
			os.mkdir(self.__duckduckpath) 

		# try:
		# 	os.stat(os.path.join(self.__duckduckpath, 'docs'))
		# except:
		# 	os.mkdir(os.path.join(self.__duckduckpath, 'docs')) 

		args = ['jsduck'];
		args = args + JsDuck.getSettings(self.__sublime, 'jsduckduckargs')
		args.append('--output ' + os.path.join(self.__duckduckpath, 'docs'));

		# command = ' '.join(args);
		print(self.__root);
		print(' '.join(args));

		p = subprocess.Popen(' '.join(args), cwd=self.__root, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE);
		output = '';
		for line in iter(p.stdout.readline, b''):
		    print(line);
		p.communicate();
		print('Finished jsduck');
		self.__sublime.status_message('Finished updating jsduckduck');
		JsDuckUpdate = None;
	@staticmethod
	def isActive():
		global JsDuckUpdate;
		return JsDuckUpdate != None

	@staticmethod
	def checkJsDuck(sublime, curRoot):
		global JsDuckUpdate;
		if JsDuck.isActive():
			return False;

		if curRoot == None:
			return False;

		duckduckpath = JsDuck.detectJsDuck(sublime, curRoot);
		if os.path.exists(os.path.join(duckduckpath, 'docs')):
			return True;

		JsDuckUpdate = JsDuck(sublime, curRoot);
		sublime.status_message('Update jsduckduck');
		return True;

	@staticmethod
	def detectRoot(sublime, curFile, folders):
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

		settings = JsDuck.getSettings(sublime, 'jsduckduckPaths');
		for path in settings:
			if os.path.exists(os.path.join(curRoot, path, 'docs')) :
				return os.path.join(curRoot, path);

		return os.path.join(curRoot, settings[0]);

	@staticmethod
	def getSettings(sublime, name):
		# default settings
		settings = sublime.load_settings("Gearbox.sublime-settings").get(name).copy()

		# per project settings
		if sublime.active_window().active_view().settings().get('Gearbox'):
			settings.update(sublime.active_window().active_view().settings().get('Gearbox').get(name))

		return settings

