import sublime, sublime_plugin, os, re, glob, itertools, json, os.path

try:
    # python 3 / Sublime Text 3
    from .JsDuck import JsDuck
except ValueError:
    # python 2 / Sublime Text 2
    from JsDuck import JsDuck

class ClassFunctions(object):
    def __init__(self, sublime, file_path):
        self.__file_path = file_path;
        self.__descriptions = [];
        self.__funcNames = [];
        self.__files = {};
        self.__types = {};
        self.__className = None;
        self.__sublime = sublime;

        self.__appRoot = JsDuck.detectRoot(sublime, file_path);
        if not self.__appRoot:
            return;
        self.__duckRoot = JsDuck.detectJsDuck(sublime, self.__appRoot);
        self.__build();

    # # Retrieves a list of all related descriptions.
    def descriptions(self):
        return self.__descriptions;

    def className(self):
        return self.__className;

    def files(self):
        return self.__files;

    def types(self):
        return self.__types;

    def appRoot(self):
        return self.__appRoot;

    def duckRoot(self):
        return self.__duckRoot;

    def isValid(self):
        return self.__appRoot != None and self.__className != None;

    def __build(self):
        classRegex = re.compile('(^\s*Ext\.define\(\s*[\'"])([A-Za-z.]+)([\'"])')
        f = open(self.__file_path, 'r', encoding="utf-8");

        while(True):
            line = f.readline();
            if line:
                match = classRegex.search(line)
                if match:
                    self.__className = match.group(2);
                    break;
            else:
                break;
        f.close();

        if not self.__className:
            self.__sublime.status_message('No class found in file')

        print(self.__className);

    def notFound(self): 
        build = self.__sublime.ok_cancel_dialog('No jsduck data found, build now?');
        if build:
            JsDuck.buildJsDuck(self.__sublime, self.__appRoot);
        
    def readJsDuckFunctions(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.notFound();
            return;

        known = {};
        for i, member in enumerate(parsedJson['members']):
            if member['tagname'] == 'method':
                # self.__descriptions.append(member['name'] + '(' + member['owner'] + ')')
                self.__descriptions.append([member['name'], member['owner']])
                self.__files[member['owner'] + ':' + member['name']] = member['files'][0]['filename'] + ':' + str(member['files'][0]['linenr']) + ':1';
                known[member['name']] = member['owner']
            
        # Add functions from parentClass that are overriden by this class.
        parentClass = parsedJson['extends']
        if parentClass:
            parsedJson = self.__readJson(self.__getJsDuckPath(parsedJson['extends']));
            if parsedJson:
                for i, member in enumerate(parsedJson['members']):
                    if member['tagname'] == 'method' and known.get(member['name'], '') != member['owner']:
                        self.__files[member['owner'] + ':' + member['name']] = member['files'][0]['filename'] + ':' + str(member['files'][0]['linenr']) + ':1';
                        self.__descriptions.append([member['name'], member['owner']])

        self.__descriptions.sort();

    def readJsDuckProperties(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.notFound();
            return;

        known = {};

        for i, member in enumerate(parsedJson['members']):
            if self.__validProperty(member):
                self.__addProperty(member);
                known[member['name']] = member['owner'];
            
        # Add functions from parentClass that are overriden by this class.
        parentClass = parsedJson['extends']
        if parentClass:
            parsedJson = self.__readJson(self.__getJsDuckPath(parsedJson['extends']));
            if parsedJson:
                for i, member in enumerate(parsedJson['members']):
                    if self.__validProperty(member) and known.get(member['name'], '') != member['owner']:
                        self.__addProperty(member);

        self.__descriptions.sort();

    def __validProperty(self, member):
        return (member['tagname'] == 'property' or member['tagname'] == 'cfg') and not member.get('static', False);

    def __addProperty(self, member):
        desc = [member['name'], member['owner']];
        # if member.get('short_doc', ' ...') != ' ...':
        #     desc.append(member['short_doc']);
        tags = [];
        if member.get('type', None) != None:
            tags.append('type:' + member['type']);
        if member.get('default', None) != None and len(member['default']) < 20:
            tags.append('default:' + member['default']);

        if len(tags) != 0:
            desc.append(', '.join(tags));

        self.__descriptions.append(desc);
        self.__files[member['owner'] + ':' + member['name']] = member['files'][0]['filename'] + ':' + str(member['files'][0]['linenr']) + ':1';
        self.__types[member['owner'] + ':' + member['name']] = member.get('type', 'String');

    def readJsDuckRelatedClasses(self):
        if self.__className == None:
            return;

        parsedJson = self.__readJson(self.__getJsDuckPath(self.__className));
        if parsedJson == None:
            self.notFound();
            return;

        self.__descriptions.append([parsedJson['extends'], 'extends']);

        for i, className in enumerate(parsedJson['requires']):
            self.__descriptions.append([className, 'requires'])

        for i, className in enumerate(parsedJson['mixins']):
            self.__descriptions.append([className, 'mixin'])

        # for i, className in enumerate(parsedJson['subclasses']):
        #     self.__descriptions.append([className, 'subclass'])

        # for i, className in enumerate(parsedJson['superclasses']):
        #     if className == parsedJson['extends']:
        #         continue;
        #     self.__descriptions.append([className, 'superclass'])

        self.__descriptions.sort()

    def __readJson(self, filepath):
        # print(filepath);
        # print(os.path.exists(filepath));
        if os.path.exists(filepath) == False:
            return None;

        f = open(filepath, 'r', encoding="utf-8")
        data = f.read()
        f.close()

        # match = re.search('(.*?\()(.*)(\);)', data)
        # if match:
        # else:
            # return None;
        parsedJson = json.loads(data);
        return parsedJson; 

    def __getJsDuckPath(self, className):
        return os.path.join(JsDuck.getJsDuckPath(self.__duckRoot), className + '.json');

    # TODO: parse the bootstrap or make configurable, maybe jsduckduck knows?
    def classNameToPath(self, className):
        return JsDuck.classNameToPath(self.__sublime, self.__appRoot, className);
