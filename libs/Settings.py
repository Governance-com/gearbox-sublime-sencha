
import sublime;

class Settings(object):

	@staticmethod
	def get(path, default=None):
		result = default;
		if sublime.active_window().active_view().settings().get('Gearbox'):
			result = Settings.getFrom(sublime.active_window().active_view().settings().get('Gearbox'), path, default);

		if result == default:
			result = Settings.getFrom(sublime.load_settings('Gearbox.sublime-settings'), path, default);

		# print(path, result);
		return result;

	@staticmethod
	def getFrom(settings, path, default=None):
		parts = path.split('.');
		for part in parts:
			if not settings or not hasattr(settings, 'get'):
				return settings;
			else:
				settings = settings.get(part, default);

		return settings;
