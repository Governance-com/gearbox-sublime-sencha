import sublime, sublime_plugin, os, re, glob, itertools

class Related(object):
    # Initializes the RelatedFiles object.
    #
    # file_path - the file to look related files for
    # patterns  - a dictionary of patterns in the following format:
    #               {"(.+)_controller.rb": ["*/the/paths/$1/**", "*/test/$1_controller_test.rb"]}
    #
    # The glob paths will have their $i replaced by the matched groups within the file name
    # matcher.
    def __init__(self, file_path, patterns, folders):
        self.__file_path = file_path
        self.__patterns = patterns
        self.__root = self.__root(folders)
        self.__files = []
        self.__descriptions = []
        self.__build()

    # # Retrieves a list of all related descriptions.
    def descriptions(self):
        return self.__descriptions

    # # Retrieves a list of all related files paths.
    def files(self):
        return self.__files

    # Builds a list with all related files and sets self.descriptions and
    # self.files.
    def __build(self):
        files = set()

        file_path = self.__to_posixpath(self.__file_path)

        # for each matching pattern
        for regex, paths in list(self.__patterns.items()):
            match = re.compile(regex).match(file_path)
            if match:
                # returns a flattened file list
                files.update(self.__files_for_paths(regex, match, paths))

        # sorts items
        files = list(files)
        files.sort()

        self.__files = files
        self.__descriptions = [self.__file_without_root(file) for file in files]

    # Returns the root folder for the given file and folders
    def __root(self, folders):
        for folder in folders:
            if self.__file_path.startswith(os.path.join(folder, "")):
                return folder

    # Retrieves a list of files fot the given match and paths
    def __files_for_paths(self, regex, match, paths):
        paths = [self.__replaced_path(match, path) for path in paths]

        files = [glob.glob(os.path.join(self.__root, path)) for path in paths]
        flattened = [self.__to_posixpath(path) for path in list(itertools.chain.from_iterable(files))]

        # Ignores current file
        if self.__file_path in flattened:
            flattened.remove(self.__file_path)

        return flattened

    # Retrieves the file name without the root part.
    def __file_without_root(self, file):
        return os.path.basename(self.__root) + file[len(self.__root):]

    # Retrieves a path with its interpolation vars replaces by the found groups
    # on match.
    def __replaced_path(self, match, path):
        replaced_path = path
        for i, group in enumerate(match.groups()):
            replaced_path = replaced_path.replace("$%s" % (i + 1), group)
        return replaced_path

    # Converts paths to posixpaths.
    def __to_posixpath(self, path):
        return re.sub("\\\\", "/", path)

class RelatedFilesCommand(sublime_plugin.WindowCommand):
    def run(self, index=None):
        active_file_path = self.__active_file_path()

        if active_file_path:
            # Builds a list of related files for the current open file.
            self.__related = Related(active_file_path, self.__patterns(), sublime.active_window().folders())

            self.window.show_quick_panel(self.__related.descriptions(), self.__open_file)
        else:
            self.__status_msg("No open files")

    # Opens the file in path.
    def __open_file(self, index):
        if index >= 0:
            sublime.set_timeout(lambda: self.window.open_file(self.__related.files()[index]), 0)
        else:
            self.__status_msg("No related files found")

    # Retrieves the patterns from settings.
    def __patterns(self):
        # default settings
        patterns = sublime.load_settings("RelatedFiles.sublime-settings").get('patterns').copy()

        # per project settings
        if sublime.active_window().active_view().settings().get('RelatedFiles'):
            patterns.update(sublime.active_window().active_view().settings().get('RelatedFiles').get('patterns'))

        return patterns

    # Returns the activelly open file path from sublime.
    def __active_file_path(self):
        if self.window.active_view():
            file_path = self.window.active_view().file_name()

            if file_path and len(file_path) > 0:
                return file_path

    # Displays a status message on sublime.
    def __status_msg(self, message):
        sublime.status_message(message)
