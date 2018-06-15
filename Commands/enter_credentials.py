from Common.utils import *
import sublime
import sublime_plugin

class EnterCredentialsCommand(sublime_plugin.WindowCommand):
    settings = dict()
    user = ""
    dir = ""

    def run(self):
        self.dir = self.window.folders()[0]
        self.window.show_input_panel("User Name:", "", self.create_user, None, None)

    def create_user(self, user):
        self.user = user
        self.window.show_input_panel("Password:", "", self.create_pass, None, None)

    def create_pass(self, password):
        cred = self.user + ":" + password
        encoded_cred = base64.encodestring(bytes(cred, "utf-8"))
        save_setting(self.dir, "auth", "Basic " + encoded_cred.decode("utf-8").replace("\n", ""))

    def is_visible(self):
        return is_sn(self.window.folders()) is True