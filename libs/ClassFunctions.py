import sublime, sublime_plugin, os, re, glob, itertools, json, os.path

from JsDuckDuck import JsDuck

class ClassFunctions(object):
    def __init__(self, sublime, file_path, folders):
        self.__file_path = file_path;
        self.__appRoot = JsDuck.detectRoot(sublime, file_path, folders);
        self.__duckRoot = JsDuck.detectJsDuck(sublime, self.__appRoot);
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

    def appRoot(self):
        return self.__appRoot;

    def duckRoot(self):
        return self.__duckRoot;

    def __build(self):
        f = open(self.__file_path, 'r')
        data = f.read()
        f.close()
        doesmatch = re.search('(Ext\.define\(\')([A-Za-z.]+)(\')', data)
        if doesmatch:
            self.__className = doesmatch.group(2);
        else:
            self.__sublime.status_message('No class found')

        print(self.__className);
        
    def readJsDuckFunctions(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.__sublime.status_message('JsDuck json parse error')
            return;

        for i, member in enumerate(parsedJson['members']):
            if member['tagname'] == 'method':
                # self.__descriptions.append(member['name'] + '(' + member['owner'] + ')')
                self.__descriptions.append([member['name'], member['owner']])
                self.__funcs[member['name']] = member['owner']
            
        # Add functions from parentClass that are overriden by this class.
        parentClass = parsedJson['extends']
        if parentClass:
            parsedJson = self.__readJson(self.__getJsDuckPath(parsedJson['extends']));
            if parsedJson:
                for i, member in enumerate(parsedJson['members']):
                    if member['tagname'] == 'method' and self.__funcs.get(member['name'], '') != member['owner']:
                        self.__descriptions.append([member['name'], member['owner']])

        self.__descriptions.sort()

    def readJsDuckRelatedClasses(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.__sublime.status_message('JsDuck json parse error')
            return;

        self.__descriptions.append([parsedJson['extends'], 'extends']);

        for i, className in enumerate(parsedJson['requires']):
            self.__descriptions.append([className, 'requires'])

        for i, className in enumerate(parsedJson['mixins']):
            self.__descriptions.append([className, 'mixin'])

        for i, className in enumerate(parsedJson['subclasses']):
            self.__descriptions.append([className, 'subclass'])

        for i, className in enumerate(parsedJson['superclasses']):
            if className == parsedJson['extends']:
                continue;
            self.__descriptions.append([className, 'superclass'])

        self.__descriptions.sort()

    def __readJson(self, filepath):
        # print(filepath);
        # print(os.path.exists(filepath));
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
        return self.__duckRoot + '/docs/output/' + className + '.js';

    # TODO: parse the bootstrap or make configurable, maybe jsduckduck knows?
    def classNameToPath(self, className):
        className = re.sub('^Governance', 'app', className);
        className = re.sub('^Gearbox', 'packages/gearbox/src', className);
        className = re.sub('^Ext', 'ext/src', className);
        className = re.sub('\.','/', className)
        return self.__appRoot + '/' + className + '.js';

    # Converts paths to posixpaths.
    def __to_posixpath(self, path):
        return re.sub("\\\\", "/", path)