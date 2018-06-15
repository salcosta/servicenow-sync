from utils import *
import sublime
import sublime_plugin

class TestConnectionCommand(sublime_plugin.WindowCommand):
    def run(self):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)

        if settings is not False:
            response = get_list(settings, "sys_properties", "")
            if response is not False:
                sublime.message_dialog("Connection Successful.")
            else:
                sublime.message_dialog("Connection Unsuccessful.")

        return

    def is_visible(self):
        return is_sn(self.window.folders())