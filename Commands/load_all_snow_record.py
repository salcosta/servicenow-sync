from Common.utils import *
import sublime
import sublime_plugin

class LoadAllSnowRecordCommand(sublime_plugin.WindowCommand):
    this_dirs = []

    def run(self, dirs):
        self.this_dirs = dirs
        self.window.show_input_panel("Enter an encoded query (or leave blank):", "", self.get_records, None, None)
        return
        

    def get_records(self, query):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)
        file_dir = self.this_dirs[0]
        table_settings = load_settings( file_dir )

        load_multiple(settings, table_settings, file_dir, query)
        return


    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0