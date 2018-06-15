from Common.utils import *
import sublime
import sublime_plugin

class LoadSnowTableCommand(sublime_plugin.WindowCommand):
    items = []
    folder = ''
    display = ''
    description = ''
    body_field = ''
    extension = ''
    settings = {}
    file_dir = ""
    item = {}
    table_fields = {}

    def run(self):
        working_dir = self.window.folders()
        app_settings = load_settings(working_dir[0])
        print(app_settings)
        self.file_dir = working_dir[0]

        if app_settings is not False:
            self.items = get_tables(app_settings)
            item_list = []

            for item in self.items:
                item_list.append([item['label'], item['name']])

            self.window.show_quick_panel(item_list, self.sync_table)

    def sync_table(self, index):
        if index != -1:
            self.item = self.items[index]
            name = self.item['name']

            self.table_fields = json.loads(table_field_list)

            if name in self.table_fields:
                if len(self.table_fields[name]) == 1:
                    self.create_single()
                else:
                    self.create_multi()
            else:
                self.custom_get_folder_name()

        return

    def create_single(self):
        name = self.item['name']
        parent_settings = {}

        friendly_name = str.replace(str.lower(self.item['label']), " ", "_") + "s"
        os.makedirs(os.path.join(self.file_dir, friendly_name))

        parent_settings['table'] = self.item['name']
        parent_settings['display'] = 'name'
        parent_settings['body_field'] = self.table_fields[name][0]['field']
        parent_settings['extension'] = self.table_fields[name][0]['extension']
        parent_settings['files'] = {}

        save_settings(os.path.join(self.file_dir, friendly_name), parent_settings)

    def create_multi(self):
        name = self.item['name']
        parent_settings = {}

        friendly_name = str.replace(str.lower(self.item['label']), " ", "_") + "s"
        base_folder = os.path.join(self.file_dir, friendly_name)
        os.makedirs(base_folder)

        parent_settings['table'] = self.item['name']
        parent_settings['display'] = 'name'
        parent_settings['multi'] = True

        save_settings(base_folder, parent_settings)

        for field in self.table_fields[name]:
            sub_settings = {}
            folder_name = field['field']
            sub_folder = os.path.join(base_folder, folder_name)
            os.makedirs(sub_folder)

            sub_settings['table'] = self.item['name']
            sub_settings['display'] = 'name'
            sub_settings['body_field'] = field['field']
            sub_settings['extension'] = field['extension']
            sub_settings['files'] = {}
            sub_settings['sub'] = 'true'

            save_settings(sub_folder, sub_settings)

    def custom_get_folder_name(self):
        friendly_name = str.replace(str.lower(self.item['label']), " ", "_")
        self.window.show_input_panel("Table Folder Name:", friendly_name + "s", self.custom_create_folder, None, None)

        return

    def custom_create_folder(self, name):
        self.file_dir = os.path.join(self.file_dir, name)

        os.makedirs(self.file_dir)

        self.settings['table'] = self.item['name']
        self.window.show_input_panel("Display Field:", "name", self.custom_get_display_field, None, None)

    def custom_get_display_field(self, display):
        self.settings['display'] = display

        self.window.show_input_panel("Body Field:", "script", self.custom_get_extension, None, None)
        return

    def custom_get_extension(self, body_field):
        self.settings['body_field'] = body_field

        self.window.show_input_panel("File Extension:", "js", self.custom_create_settings, None, None)
        return

    def custom_create_settings(self, extension):
        self.settings['extension'] = extension
        self.settings['files'] = {}

        file_name = os.path.join(self.file_dir, "service-now.json")
        f = open(file_name, 'wb')
        f.write(bytes(json.dumps(self.settings, indent=4), 'utf-8'))
        f.close()

        return

    def is_visible(self):
        return is_sn(self.window.folders())