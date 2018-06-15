from utils import *
import sublime
import sublime_plugin
import webbrowser

class OpenSnowRecordCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name():
            working_dir = self.view.window().folders()[0]
            settings = load_settings(working_dir)

            full_file_name = self.view.file_name()
            file_path = get_file_path(full_file_name)
            file_name = get_file_name(full_file_name)

            if file_name == "service-now.json":
                return False

            table_settings = load_settings(file_path)
            
            if "id" in table_settings:
                parent_path = file_path[::-1]
                parent_path = parent_path.split('/',1)[1]
                parent_path = parent_path[::-1]
                parent_settings = load_settings(parent_path)
                table = parent_settings["table"]
                sys_id = table_settings["id"]
            else:
                table = table_settings['table']
                sys_id = lookup_record_id(file_name, table_settings)

            if sys_id is not False:
                url = "https://" + settings['instance'] + ".service-now.com/"
                url = url + table + ".do?sys_id=" + sys_id
                webbrowser.open_new_tab(url)

    def is_visible(self):
        return is_sn(self.view.window().folders())