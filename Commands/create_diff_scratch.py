import sublime
import sublime_plugin

class CreateDiffScratchCommand(sublime_plugin.TextCommand):
    def run(self, edit, content):
        self.view.insert(edit, 0, content)