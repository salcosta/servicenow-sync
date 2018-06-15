from utils import *
import sublime
import sublime_plugin

class LoadModifiedRecordCommand(sublime_plugin.WindowCommand):
    this_dirs = []

    def run(self, dirs):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)
        file_dir = dirs[0]
        table_settings = load_settings(file_dir)
        query = "sys_customer_update=true"

        settings = load_settings(working_dir)
        table_settings = load_settings( file_dir )

        load_multiple(settings, table_settings, file_dir, query)

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0