import sublime, sublime_plugin, os, re, glob, itertools, json, os.path

class ClassFunctions(object):
    def __init__(self, sublime, file_path, folders):
        self.__file_path = file_path
        self.__root = self.__root(folders)
        self.__descriptions = []
        self.__funcNames = []
        self.__funcs = {}
        self.__className = None
        self.__sublime = sublime
        self.__build()

    # # Retrieves a list of all related descriptions.
    def descriptions(self):
        return self.__descriptions;

    def funcs(self):
        return self.__funcs;

    def root(self):
        return self.__root;

    def __build(self):
        duckduckpath = None
        if os.path.exists(self.getRootApplication() + '/jsduck/docs'):
            duckduckpath = self.getRootApplication() + '/jsduck/docs'
        else:
            self.__sublime.status_message('No jsduck found')
            return
        print(duckduckpath)
        f = open(self.__file_path, 'r')
        data = f.read()
        f.close()
        doesmatch = re.search('(Ext\.define\(\')([A-Za-z.]+)(\')', data)
        if doesmatch:
            self.__className = doesmatch.group(2);
        else:
            self.__sublime.status_message('No class found')
        
    def readJsDuckFunctions(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.__sublime.status_message('JsDuck json parse error')
            return;

        for i, member in enumerate(parsedJson['members']):
            if member['tagname'] == 'method':
                self.__descriptions.append(member['name'] + '(' + member['owner'] + ')')
                self.__funcs[member['name']] = member['owner']
            
        # Add functions from parentClass that are overriden by this class.
        parentClass = parsedJson['extends']
        if parentClass:
            parsedJson = self.__readJson(self.__getJsDuckPath(parsedJson['extends']));
            if parsedJson:
                for i, member in enumerate(parsedJson['members']):
                    if member['tagname'] == 'method' and self.__funcs[member['name']] != member['owner']:
                        self.__descriptions.append(member['name'] + '(' + member['owner'] + ')')

        self.__descriptions.sort()

    def readJsDuckRelatedClasses(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.__sublime.status_message('JsDuck json parse error')
            return;

        self.__descriptions.append(parsedJson['extends'] + '(extends)');

        for i, className in enumerate(parsedJson['requires']):
            self.__descriptions.append(className + '(requires)')

        for i, className in enumerate(parsedJson['mixins']):
            self.__descriptions.append(className + '(mixin)')

        for i, className in enumerate(parsedJson['subclasses']):
            self.__descriptions.append(className + '(subclass)')

        for i, className in enumerate(parsedJson['superclasses']):
            if className == parsedJson['extends']:
                continue;
            self.__descriptions.append(className + '(superclass)')

        self.__descriptions.sort()

    def __readJson(self, filepath):
        if os.path.exists(filepath) == False:
            return None;

        f = open(filepath, 'r')
        data = f.read()
        f.close()

        match = re.search('(.*?\()(.*)(\);)', data)
        if match:
            parsedJson = json.loads(match.group(2));
            return parsedJson; 
        else:
            return None;

    def __getJsDuckPath(self, className):
        duckduckpath = self.getRootApplication() + '/jsduck/docs'
        return duckduckpath + '/output/' + className + '.js';

    # Returns the root folder for the given file and folders
    def __root(self, folders):
        for folder in folders:
            if self.__file_path.startswith(os.path.join(folder, "")):
                return folder

    # TODO: parse the bootstrap or make configurable, maybe jsduckduck knows?
    def classNameToPath(self, className):
        className = re.sub('^Governance', 'app', className);
        className = re.sub('^Gearbox', 'packages/gearbox/src', className);
        className = re.sub('^Ext', 'ext/src', className);
        className = re.sub('\.','/', className)
        return self.getRootApplication() + '/' + className + '.js';

    # TODO: make this dynamic
    def getRootApplication(self):
        if os.path.exists(self.__root + '/desktop/app'):
            return self.__root + '/desktop';
        if os.path.exists(self.__root + '/app'):
            return self.__root;

        return '';

    # Retrieves the file name without the root part.
    def __file_without_root(self, file):
        return os.path.basename(self.__root) + file[len(self.__root):]

    # Converts paths to posixpaths.
    def __to_posixpath(self, path):
        return re.sub("\\\\", "/", path)

class ClassFunctionsCommand(sublime_plugin.WindowCommand):
    def run(self, index=None):
        # self.__status_msg("run")
        active_file_path = self.__active_file_path()

        if active_file_path:
            self.__funcs = ClassFunctions(sublime, active_file_path, sublime.active_window().folders())
            self.__funcs.readJsDuckFunctions();

            if index != None:
                self.__open_file(index)
            else:
                self.window.show_quick_panel(self.__funcs.descriptions(), self.__open_file)
        else:
            sublime.status_message("No open files")

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0 and len(self.__funcs.descriptions()) > index:
            curName = self.__funcs.descriptions()[index]
            match = re.search('([^\(]+)\(([^\(]+)\)', curName)
            print(match.group(1));
            print(match.group(2));
            curFunction = match.group(1);
            curClass = match.group(2);

            path = self.__funcs.classNameToPath(curClass);
            lineIndex = self.__getFunctionLine(path, curFunction)

            filepath = path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]);
            print(filepath);

            # TRANSIENT makes it more confusing.
            # view = sublime.set_timeout(lambda: self.window.open_file(filepath), sublime.ENCODED_POSITION | sublime.TRANSIENT))
            view = sublime.set_timeout(lambda: self.window.open_file(filepath, sublime.ENCODED_POSITION))
        else:
            sublime.status_message("No functions found")

    def __getFunctionLine(self, filepath, name):
        lineNumber = 0;
        f = open(filepath, 'r')
        regex = re.compile(name + ':\s*function\(');
        result = [0, 0];
        while(True):
            lineNumber += 1;
            line = f.readline()
            if line:
                match = regex.search(line)
                if match:
                    result = [lineNumber, match.start() + 1];
                    break;
            else:
                break;
        f.close();
        return result;

    # Returns the activelly open file path from sublime.
    def __active_file_path(self):
        if self.window.active_view():
            file_path = self.window.active_view().file_name()

            if file_path and len(file_path) > 0:
                return file_path


class ClassRelatedClassesCommand(sublime_plugin.WindowCommand):
    def run(self, index=None):
        # self.__status_msg("run")
        active_file_path = self.__active_file_path()

        if active_file_path:
            self.__funcs = ClassFunctions(sublime, active_file_path, sublime.active_window().folders())
            self.__funcs.readJsDuckRelatedClasses();

            if index != None:
                self.__open_file(index)
            else:
                self.window.show_quick_panel(self.__funcs.descriptions(), self.__open_file)
        else:
            sublime.status_message("No open files")

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0 and len(self.__funcs.descriptions()) > index:
            curName = self.__funcs.descriptions()[index]
            match = re.search('([^\(]+)\(([^\(]+)\)', curName)
            print(match.group(1));
            print(match.group(2));
            curClass = match.group(1);
            curGroup = match.group(2);

            filepath = self.__funcs.classNameToPath(curClass);
            print(filepath);

            # TRANSIENT makes it more confusing.
            # view = sublime.set_timeout(lambda: self.window.open_file(filepath), sublime.ENCODED_POSITION | sublime.TRANSIENT))
            view = sublime.set_timeout(lambda: self.window.open_file(filepath, 0))
        else:
            sublime.status_message("No class found")

    # Returns the activelly open file path from sublime.
    def __active_file_path(self):
        if self.window.active_view():
            file_path = self.window.active_view().file_name()

            if file_path and len(file_path) > 0:
                return file_path
