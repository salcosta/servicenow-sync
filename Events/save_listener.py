from Common.utils import *
import sublime
import sublime_plugin

class ServiceNowListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if len(view.window().folders()) > 0:
            working_dir = view.window().folders()[0]
            settings = load_settings(working_dir)

            if settings is not False:
                updated_record = False
                full_file_name = view.file_name()
                file_path = get_file_path(full_file_name)
                file_name = get_file_name(full_file_name)
                file_type = get_file_type(full_file_name)
                file_name_no_ext = file_name.split(".")[0];

                if file_name == "service-now.json" or file_type == "spec":
                    return False

                table_settings = load_settings(file_path)

                if table_settings is False:
                    return False

                reg = sublime.Region(0, view.size())
                text = view.substr(reg)
                data = dict()

                if 'grouped_child' in table_settings:
                    child_settings = table_settings
                    parent_path = file_path[::-1]
                    parent_path = parent_path.split('/',1)[1]
                    parent_path = parent_path[::-1]
                    table_settings = load_settings(parent_path)

                    for field in table_settings['fields']:

                        if(field['name'] == file_name_no_ext):
                            sys_id = child_settings['id']
                            record = get_record(settings, table_settings['table'], sys_id)
                            
                            if record is not False:
                                body_field = field['field']
                                name = full_file_name
                                data[body_field] = text
                                doc = record[body_field]

                                continue_update = diff_and_confirm(full_file_name, doc, text);

                                if continue_update is True:
                                    updated_record = update_record(settings, data, table_settings['table'],sys_id)

                else:                
                    data[table_settings['body_field']] = text

                    if file_name in table_settings['files']:
                        sys_id = table_settings['files'][file_name]['sys_id']
                        record = get_record(settings, table_settings['table'], sys_id)

                        if record is not False:
                            body_field = table_settings['body_field']
                            name = full_file_name

                            doc = record[body_field]
                            
                            continue_update = diff_and_confirm(full_file_name, doc, text);

                            if continue_update is True:
                                updated_record = update_record(settings, data, table_settings['table'],sys_id)
                        
                    else:
                        data[table_settings['display']] = str.replace(file_name,"." + table_settings['extension'],"")
                        updated_record = create_record(settings, data, table_settings['table'])

                if updated_record is not False:
                    print("Updated at " + updated_record['sys_updated_on'])
                    add_file(file_path, updated_record['sys_id'], file_name, time.mktime(convert_time(updated_record['sys_updated_on']).timetuple()))

