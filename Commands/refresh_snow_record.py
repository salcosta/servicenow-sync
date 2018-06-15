from Common.utils import *
import sublime
import sublime_plugin

class RefreshSnowRecordCommand(sublime_plugin.WindowCommand):
    items = []
    table_settings = {}

    def run(self, files):
        working_dir = self.window.folders()[0]

        settings = load_settings(working_dir)
        full_file_name = files[0]
        file_path = get_file_path(full_file_name)
        file_name = get_file_name(full_file_name)
        file_type = get_file_type(full_file_name)

        if file_name == "service-now.json" or file_type == "spec":
            return False

        table_settings = load_settings(file_path)

        if table_settings is False:
            return False

        sys_id = lookup_record_id(file_name, table_settings)

        if sys_id is not False:
            result = get_record(settings, table_settings['table'], sys_id)

            if result is not False:
                item = result

                body_field = table_settings['body_field']
                name = full_file_name

                doc = item[body_field]

                if os.path.exists(full_file_name):
                    diffs = diff_file_to_doc(full_file_name, doc)

                    if not diffs:
                        sublime.message_dialog('File is up to date.')
                    else:
                        action = sublime.yes_no_cancel_dialog("Server record is newer than local copy.",
                                                              "Overwrite Local", "View Differences")

                        if action == sublime.DIALOG_YES:
                            write_doc_file(full_file_name, doc)

                        if action == sublime.DIALOG_NO:
                            diffs = map(lambda line: (line and line[-1] == "\n") and line or line + "\n", diffs)
                            diffs = ''.join(diffs)
                            scratch = self.window.new_file()
                            scratch.set_scratch(True)
                            scratch.run_command('create_diff_scratch', {'content': diffs})

        else:
            return False

    def is_visible(self, files):
        return is_sn(self.window.folders()) and len(files) == 1