import sublime, sublime_plugin, os, re, glob, itertools, json, os.path

class ClassFunctions(object):
    def __init__(self, file_path, folders):
        self.__file_path = file_path
        self.__root = self.__root(folders)
        self.__descriptions = []
        self.__funcNames = []
        self.__funcs = {}
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
            self.__status_msg('No jsduck found')
            return
        print(duckduckpath)
        f = open(self.__file_path, 'r')
        data = f.read()
        f.close()
        doesmatch = re.search('(Ext\.define\(\')([A-Za-z.]+)(\')', data)
        if doesmatch:
            className = doesmatch.group(2)
            print(className)
            if os.path.exists(duckduckpath + '/output/' + className + '.js') == False:
                self.__status_msg('No jsduck output found')
                return;
            self.__readJsDuck(duckduckpath + '/output/' + className + '.js')
        else:
            self.__status_msg('No class found')
        
    def __readJsDuck(self, filepath):
        # json.loads

        f = open(filepath, 'r')
        data = f.read()
        f.close()

        match = re.search('(.*?\()(.*)(\);)', data)
        if match:
            parsedJson = json.loads(match.group(2))
            print(parsedJson)
            for i, member in enumerate(parsedJson['members']):
                if member['tagname'] == 'method':
                    self.__descriptions.append(member['name'] + '(' + member['owner'] + ')')
                    self.__funcs[member['name']] = member['owner']
                
            self.__descriptions.sort()
            print(self.__descriptions)
        else:
            self.__status_msg('JsDuck json parse error')
    # Returns the root folder for the given file and folders
    def __root(self, folders):
        for folder in folders:
            if self.__file_path.startswith(os.path.join(folder, "")):
                return folder

    # TODO: make this dynamic
    def getRootApplication(self):
        if os.path.exists(self.__root + '/app'):
            return self.__root;
        if os.path.exists(self.__root + '/desktop/app'):
            return self.__root + '/desktop';

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
            self.__funcs = ClassFunctions(active_file_path, sublime.active_window().folders())

            if index != None:
                self.__open_file(index)
            else:
                self.window.show_quick_panel(self.__funcs.descriptions(), self.__open_file)
        else:
            self.__status_msg("No open files")

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0 and len(self.__funcs.funcs()) > index:
            curName = self.__funcs.descriptions()[index]
            match = re.search('([^\(]+)\(([^\(]+)\)', curName)
            print(match.group(1));
            print(match.group(2));
            curFunction = match.group(1);
            curClass = match.group(2);
            path = self.__classNameToPath(curClass);
            lineIndex = self.__getFunctionLine(path, curFunction)
            print(path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]));
            view = sublime.set_timeout(lambda: self.window.open_file(path + ':' + str(lineIndex[0]) + ':' + str(lineIndex[1]), sublime.ENCODED_POSITION | sublime.TRANSIENT))
        else:
            self.__status_msg("No functions found")

    # TODO: parse the bootstrap or make configurable, maybe jsduckduck knows?
    def __classNameToPath(self, className):
        className = re.sub('^Governance', 'app', className);
        className = re.sub('^Gearbox', 'packages/gearbox/src', className);
        className = re.sub('^Ext', 'ext/src', className);
        className = re.sub('\.','/', className)
        return self.__funcs.getRootApplication() + '/' + className + '.js';

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

    # Displays a status message on sublime.
    def __status_msg(self, message):
        sublime.status_message(message)
