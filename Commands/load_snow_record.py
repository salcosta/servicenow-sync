from Common.utils import *
import sublime
import sublime_plugin

class LoadSnowRecordCommand(sublime_plugin.WindowCommand):
    items = []
    table_settings = {}
    working_dir = ''
    file_dir = ""

    def run(self, dirs):
        self.working_dir = self.window.folders()[0]
        settings = load_settings(self.working_dir)
        self.file_dir = dirs[0]
        self.table_settings = load_settings(self.file_dir)

        query = ""

        if 'query' in self.table_settings:
            query = self.table_settings['query']

        if settings is not False and self.table_settings is not False:
            fields = ['sys_id','sys_updated_on']
            
            if "display" in self.table_settings:
                fields.append(self.table_settings["display"])

            fields = ",".join(fields);
            self.items = get_list(settings, self.table_settings['table'], query, fields)
            item_list = []

            for item in self.items:
                item_list.append([item[self.table_settings['display']], item['sys_id']])

            self.window.show_quick_panel(item_list, self.on_done)

    def on_done(self, index):
        if index != -1:
            item = self.items[index]
            settings = load_settings(self.working_dir)

            if settings is not False and self.table_settings is not False:
                record = get_record(settings,self.table_settings['table'],item['sys_id'])

            if 'grouped' in self.table_settings:
                name_field = self.table_settings['display']
                name = record[name_field]
                name = re.sub('[^-a-zA-Z0-9_.() ]+', '', name)
                grouped_dir = os.path.join(self.file_dir, name)
                
                if os.path.exists(grouped_dir):
                        grouped_dir = grouped_dir + "_" + record['sys_id']

                os.makedirs(grouped_dir)
                settings = json.loads('{}')
                settings['grouped_child'] = True
                settings['id'] = record['sys_id']
                save_settings(grouped_dir, settings)

                for child in self.table_settings['fields']:
                    body_field = child['field'];
                    extension = child['extension']
                    name = convert_file_name(child['name'] + "." + extension)
                    file_name = os.path.join(grouped_dir , name)

                    if os.path.exists(file_name):
                            if sublime.ok_cancel_dialog("File already exists.\nOverwrite?")==False:
                                return False

                    doc = record[body_field]
                    write_doc_file(file_name, doc)

            if 'multi' in self.table_settings:
                for child in os.listdir(self.file_dir):
                    test_path = os.path.join(self.file_dir, child)
                    if os.path.isdir(test_path):
                        sub_settings = load_settings(test_path)
                        body_field = child
                        name_field = sub_settings['display']
                        extension = sub_settings['extension']
                        name = convert_file_name(record[name_field] + "." + extension)

                        doc = record[body_field]
                        file_name = os.path.join(self.file_dir, child, name)

                        if os.path.exists(file_name):
                            if sublime.ok_cancel_dialog("File already exists.\nOverwrite?") is False:
                                return False

                        write_doc_file(file_name, doc)

                        add_file(test_path, record['sys_id'], name)

            else:
                body_field = self.table_settings['body_field']
                name_field = self.table_settings['display']
                extension = self.table_settings['extension']
                name = convert_file_name(record[name_field] + "." + extension)

                doc = record[body_field]
                file_name = os.path.join(self.file_dir, name)

                if os.path.exists(file_name):
                    if sublime.ok_cancel_dialog("File already exists.\nOverwrite?") is False:
                        return False

                write_doc_file(file_name, doc)

                add_file(self.file_dir, record['sys_id'], name)

                self.window.open_file(os.path.join(self.file_dir, name))

            return

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0