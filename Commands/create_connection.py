from utils import *
import sublime
import sublime_plugin

class CreateConnectionCommand(sublime_plugin.WindowCommand):
    settings = dict()
    user = ""
    dir = ""

    def run(self):
        if not self.window.folders():
            sublime.message_dialog("SNOW Sync Sublime plugin requires an open folder.")
            return
        else:
            self.dir = self.window.folders()[0]
            self.window.show_input_panel("Instance Name:", "", self.create_instance, None, None)

        return

    def create_instance(self, instance):
        self.settings['instance'] = instance

        self.window.show_input_panel("User Name:", "", self.create_user, None, None)

    def create_user(self, user):
        self.user = user
        self.window.show_input_panel("Password:", "", self.create_pass, None, None)

    def create_pass(self, password):
        cred = self.user + ":" + password
        encoded_cred = base64.encodestring(bytes(cred, "utf-8"))

        self.settings['auth'] = "Basic " + encoded_cred.decode("utf-8").replace("\n", "")
        save_settings(self.dir, self.settings)

    def is_visible(self):
        return is_sn(self.window.folders()) is False