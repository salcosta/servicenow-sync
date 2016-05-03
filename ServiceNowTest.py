import sublime
import sublime_plugin
import urllib.request
import urllib.error
import re
import time
import base64
import json
import os
import string
import webbrowser
import difflib
import http.cookiejar
import codecs

class OpenSnowRecordCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name():
            working_dir = self.view.window().folders()[0]
            settings = load_settings(working_dir)

            full_file_name = self.view.file_name()
            file_pieces = re.split(r"(?i)[\\/]", full_file_name)
            file_name = file_pieces[ len(file_pieces) - 1]

            if file_name=="service-now.json":
                return False

            file_type = file_pieces[ len(file_pieces) - 2]
            table_settings = load_settings(os.path.join(working_dir, file_type))

            if file_name in table_settings['files']:
                sys_id = table_settings['files'][file_name]['sys_id']
                url = "https://" + settings['instance'] + ".service-now.com/" 
                url = url + table_settings['table'] + ".do?sys_id=" + sys_id
                webbrowser.open_new_tab(url)

    def is_visible(self):
        return is_sn(self.view.window().folders())  


class ServiceNowListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        working_dir = view.window().folders()[0]
        settings = load_settings(working_dir)

        if settings!=False:
            full_file_name = view.file_name()
            file_pieces = re.split(r"(?i)[\\/]", full_file_name)
            file_name = file_pieces[ len(file_pieces) - 1]
            file_type = file_pieces[ len(file_pieces) - 2]

            if file_name=="service-now.json" or file_type =="spec":
                return False

            table_settings = load_settings(os.path.join(working_dir, file_type))

            if table_settings==False:
                return False

            reg = sublime.Region(0, view.size())
            text = view.substr(reg)
            data = dict()
            data[table_settings['body_field']] = text


            if file_name in table_settings['files']:
                sys_id = table_settings['files'][file_name]['sys_id']
                result = get_record(settings, table_settings['table'], sys_id)

                if result!=False:
                    item = result[0]

                    body_field = table_settings['body_field']
                    name = full_file_name

                    doc = item[body_field]
                    diffs = diff_file_to_doc(full_file_name,doc)

                    if diffs:
                        diffs = diff_doc_to_doc(text,doc)
                        if diffs:
                            action = sublime.yes_no_cancel_dialog("Remote record does not match local.","Overwrite Remote","View Differences")
                            if action==sublime.DIALOG_YES:
                                update_record(settings, data, table_settings['table'],sys_id)

                            if action==sublime.DIALOG_NO:
                                diffs = map(lambda line: (line and line[-1] == "\n") and line or line + "\n", diffs)
                                diffs = ''.join(diffs)
                                scratch = view.window().new_file()
                                scratch.set_scratch(True)
                                scratch.run_command('create_diff_scratch', {'content': diffs})

                            return False

                        else:
                            return True
                    
                    update_record(settings, data, table_settings['table'],sys_id)
                
            else:
                data[table_settings['display']] = str.replace(file_name,"." + table_settings['extension'],"")
                result = create_record(settings, data, table_settings['table'])

                if result!=False:
                    add_file(os.path.join(working_dir, file_type), result['records'][0]['sys_id'], file_name)


class LoadSnowTableCommand(sublime_plugin.WindowCommand):
    items = []

    def run(self):
        working_dir = self.window.folders()
        settings = load_settings(working_dir[0])
        self.file_dir = working_dir[0]

        if settings!=False:
            self.items = get_tables(settings)
            item_list = []

            for item in self.items:
                item_list.append([item['label'], item['name'] ])

            self.window.show_quick_panel(item_list, self.get_folder_name)        

    def get_folder_name(self, index):
        if index!=-1:
            self.item = self.items[index]
            name = self.item['name']
            friendly_name = str.replace(str.lower(self.item['label'])," ","_")

            self.window.show_input_panel("Table Folder Name:", friendly_name + "s", self.create_folder, None, None)
            
        return

    def create_folder(self, name):
        self.file_dir = os.path.join(self.file_dir, name)

        os.makedirs(self.file_dir)

        self.window.show_input_panel("Table settings (Display Field,Body Field,File Extension):", "name,script,js", self.create_settings, None, None)

    def create_settings(self, settings_string):
        settings_list = settings_string.split(",")
        settings = {}

        if len(settings_list)!=3:
            settings_list = ['name','script','js']

        settings['table'] = self.item['name']
        settings['display'] = settings_list[0]
        settings['body_field'] = settings_list[1]
        settings['extension'] = settings_list[2]

        settings['files'] = {};

        file_name = os.path.join(self.file_dir, "service-now.json")
        f = open( file_name, 'wb')
        f.write( bytes(json.dumps(settings, indent=4),'utf-8'))
        f.close()

        return


    def is_visible(self):
        return is_sn(self.window.folders())        

class LoadSnowRecordCommand(sublime_plugin.WindowCommand):
    items = []
    table_settings = {}

    def run(self, dirs):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)
        self.file_dir = dirs[0]
        self.table_settings = load_settings( self.file_dir )

        query = ""

        if 'query' in self.table_settings:
            query = self.table_settings['query']
        

        if settings!=False and self.table_settings!=False:
            self.items = get_list(settings, self.table_settings['table'], query)
            item_list = []

            for item in self.items:
                item_list.append([item[self.table_settings['display']]])

            self.window.show_quick_panel(item_list, self.on_done)

    def on_done(self, index):
        if index!=-1:
            item = self.items[index]

            body_field = self.table_settings['body_field']
            name_field = self.table_settings['display']
            extension  = self.table_settings['extension'] 
            name = item[name_field] + "." + extension

            doc = item[body_field]
            file_name = os.path.join(self.file_dir , name)

            if os.path.exists(file_name):
                if sublime.ok_cancel_dialog("File already exists.\nOverwrite?")==False:
                    return False


            f = open( file_name, 'wb')
            f.write( bytes(doc, 'UTF-8'))
            f.close()

            add_file(self.file_dir,item['sys_id'],name)

            self.window.open_file( os.path.join(self.file_dir , name) )

            return

    def is_visible(self,dirs):
        return is_sn(self.window.folders()) and len(dirs) >0


class RefreshSnowRecordCommand(sublime_plugin.WindowCommand):
    items = []
    table_settings = {}

    def run(self, files):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)
        
        full_file_name = files[0]
        file_pieces = re.split(r"(?i)[\\/]", full_file_name)
        file_name = file_pieces[ len(file_pieces) - 1]
        file_type = file_pieces[ len(file_pieces) - 2]

        if file_name=="service-now.json" or file_type =="spec":
            return False

        table_settings = load_settings(os.path.join(working_dir, file_type))

        if table_settings==False:
            return False

        if file_name in table_settings['files']:
            sys_id = table_settings['files'][file_name]['sys_id']
            result = get_record(settings, table_settings['table'], sys_id)

            if result!=False:
                print(result[0])
                item = result[0]

                body_field = table_settings['body_field']
                name = full_file_name

                doc = item[body_field]

                if os.path.exists(full_file_name):
                    diffs = diff_file_to_doc(full_file_name, doc)

                    if not diffs:
                        sublime.message_dialog('File is up to date.')
                    else:
                        action = sublime.yes_no_cancel_dialog("Server record is newer than local copy.","Overwrite Local","View Differences")
                        if action==sublime.DIALOG_YES:
                            f = open( full_file_name, 'wb')
                            f.write( bytes(doc, 'UTF-8'))
                            f.close()


                        if action==sublime.DIALOG_NO:
                            diffs = map(lambda line: (line and line[-1] == "\n") and line or line + "\n", diffs)
                            diffs = ''.join(diffs)
                            scratch = self.window.new_file()
                            scratch.set_scratch(True)
                            scratch.run_command('create_diff_scratch', {'content': diffs})
    
        else:
            return False

    def is_visible(self, files):
        return is_sn(self.window.folders()) and len(files) == 1


class TestConnectionCommand(sublime_plugin.WindowCommand):
    def run(self):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)

        if settings!=False:
            response = get_list(settings,"sys_properties","")
            if response!=False:
                sublime.message_dialog("Connection Successful.")
            else:
                sublime.message_dialog("Connection Unsuccessful.")

        return

    def is_visible(self):
        return is_sn(self.window.folders())        


class CreateConnectionCommand(sublime_plugin.WindowCommand):
    settings = dict()
    user = ""

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
        cred = self.user+":" + password
        encodedCred = base64.encodestring(bytes(cred, "utf-8"))
        print(encodedCred)
        self.settings['auth'] = "Basic " + encodedCred.decode("utf-8").replace("\n","")
        save_settings(self.dir, self.settings)

    def is_visible(self):
        return is_sn(self.window.folders())==False


class EnterCredentialsCommand(sublime_plugin.WindowCommand):
    settings = dict()
    user = ""

    def run(self):
        self.dir = self.window.folders()[0]
        self.window.show_input_panel("User Name:", "", self.create_user, None, None)

    def create_user(self, user):
        self.user = user
        self.window.show_input_panel("Password:", "", self.create_pass, None, None)


    def create_pass(self, password):
        cred = self.user+":" + password
        encodedCred = base64.encodestring(bytes(cred, "utf-8"))
        save_setting(self.dir, "auth", "Basic " + encodedCred.decode("utf-8").replace("\n",""))

    def is_visible(self):
        return is_sn(self.window.folders())==True


class CreateDiffScratchCommand(sublime_plugin.TextCommand):
    def run(self, edit, content):
        self.view.insert(edit, 0, content)


def is_sn(dirs):
    if len(dirs) == 0:
        return False

    settings_file = os.path.join(dirs[0] , "service-now.json")
    return os.path.exists(settings_file)  


def add_file(dir,id,name):
    settings = load_settings(dir)

    if name in settings['files']:
        settings['files'][name]['sys_id'] = id
    else:
        settings['files'][name] = dict()
        settings['files'][name]['sys_id'] = id

    save_settings(dir, settings)


def load_settings(dir):
    settings_file = os.path.join(dir , "service-now.json")
    
    if os.path.exists(settings_file) == False:
        return False

    f = open( settings_file, 'r')
    json_data = f.read()
    settings = json.loads(json_data)

    return settings


def save_settings(dir, settings):
    settings_file = os.path.join(dir , "service-now.json")
    f = open( settings_file, 'wb')
    f.write(bytes(json.dumps(settings, indent=4),'utf-8'))
    f.close()


def save_setting(dir, key, value):
    settings_file = os.path.join(dir , "service-now.json")
    settings = load_settings(dir)
    settings[key] = value
    f = open( settings_file, 'wb')
    f.write( bytes(json.dumps(settings, indent=4),'utf-8'))
    f.close()

    return true


def diff_file_to_doc(full_file_name, doc):
    f = codecs.open( full_file_name, 'r', "utf-8")
    originalDoc = prep_content(f.read())
    f.close()
    newDoc = prep_content(doc)
    diffs = list(difflib.unified_diff(originalDoc, newDoc))    

    return diffs

def diff_doc_to_doc(originalDoc, doc):
    originalDoc = prep_content(originalDoc)
    newDoc = prep_content(doc)
    diffs = list(difflib.unified_diff(originalDoc, newDoc))    

    return diffs


def http_call(settings, url, data="", content="application/json"):
   
    if type(data) == dict:
        data = json.dumps(data).encode('utf8')

    err = ""        
    timeout = 5


    if data!="":
        request = urllib.request.Request(url, data)
    else:
        request = urllib.request.Request(url)

    request.add_header("Authorization", settings['auth'])
    
    if content!="":
        request.add_header("Content-type", content)

    try:
        http_file = urllib.request.urlopen(request, timeout=timeout)
        result = http_file.read()
    except urllib.error.HTTPError as e:
        err = 'Error %s' % (str(e.code))
    except urllib.error.URLError as e:
        err = 'Error %s' % (str(e.code))

    if err!="":
        print(err)
        return False
    else:
        return result.decode()


def update_record(settings, data, table, sys_id):
    url = "https://" + settings['instance'] + ".service-now.com/" + table +".do?JSONv2"
    url = url + "&sysparm_action=update"
    url = url + "&sysparm_query=sys_id=" + sys_id

    return json.loads( http_call(settings, url, data))

def get_record(settings, table, sys_id):
    url = "https://" + settings['instance'] + ".service-now.com/" + table +".do?JSONv2"
    url = url + "&sysparm_query=sys_id=" + sys_id

    response_data = json.loads(http_call(settings, url))['records']

    return response_data

def create_record(settings, data, table):
    url = "https://" + settings['instance'] + ".service-now.com/" + table +".do?JSONv2"
    url = url + "&sysparm_action=insert"
    
    return json.loads( http_call(settings, url, data))

def get_list(settings, table, query):
    data = dict()
    url = "https://" + settings['instance'] + ".service-now.com/" + table +".do?JSONv2"
    if query!="":
        url = url + "&sysparm_query=" + query

    response_data = json.loads(http_call(settings, url, data))['records']

    return response_data

def get_tables(settings):
    list_data = get_list(settings, "sys_documentation", "element=NULL^nameNOT%20LIKEts_c^language=en^nameNOT%20LIKE0")

    return list_data

def prep_content(ab):
        content = ab.splitlines(True)
        content = [line.replace("\r\n", "\n").replace("\r", "\n") for line in content]
        content = [line.rstrip() for line in content]

        return content


