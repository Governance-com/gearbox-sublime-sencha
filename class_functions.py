import sublime, sublime_plugin, os, re, glob, itertools, json, os.path, sys

__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

libs_path = os.path.join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from ClassFunctions import ClassFunctions
from JsDuckDuck import JsDuck

class ClassFunctionsCommand(sublime_plugin.WindowCommand):
    def run(self, index=None):
        active_file_path = self.__active_file_path()
        self.__funcs = ClassFunctions(sublime, active_file_path, sublime.active_window().folders())

        JsDuck.checkJsDuck(sublime, self.__funcs.appRoot());
        if JsDuck.isActive(): 
            sublime.status_message('JsDuck is updating...');
            return;

        if active_file_path:
            self.__funcs.readJsDuckFunctions();

            print(self.__funcs.descriptions())
            if index != None:
                self.__open_file(index)
            else:
                self.window.show_quick_panel(self.__funcs.descriptions(), self.__open_file)
        else:
            sublime.status_message("No open files")

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0 and len(self.__funcs.descriptions()) > index:
            curEntry = self.__funcs.descriptions()[index]
            curFunction = curEntry[0];
            curClass = curEntry[1];

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
        active_file_path = self.__active_file_path()
        self.__funcs = ClassFunctions(sublime, active_file_path, sublime.active_window().folders())

        JsDuck.checkJsDuck(sublime, self.__funcs.appRoot())
        if JsDuck.isActive(): 
            sublime.status_message('JsDuck is updating...');
            return;

        if active_file_path:
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
            curEntry = self.__funcs.descriptions()[index]
            curClass = curEntry[0];
            curGroup = curEntry[1];

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
