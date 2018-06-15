import sublime
import sublime_plugin
import urllib.parse
import urllib.request
import urllib.error
import re
import base64
import json
import os
import webbrowser
import difflib
import codecs
from datetime import datetime
import time


# noinspection PyUnresolvedReferences
def http_call(request):
    err = ""
    timeout = 5
    result = ""

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


def http_put(settings, url, data):
    json_data = json.dumps(data).encode('utf8');
    request = urllib.request.Request(url, json_data, method="PUT")
    request.add_header("Authorization", settings['auth'])
    request.add_header("Accept", "application/json")
    request.add_header("Content-type", "application/json")    

    return http_call(request);

def http_post(settings, url,data):
    json_data = json.dumps(data).encode('utf8');
    request = urllib.request.Request(url, json_data, method="POST")
    
    request.add_header("Authorization", settings['auth'])
    request.add_header("Accept", "application/json")
    request.add_header("Content-type", "application/json")    

    return http_call(request);

def http_get(settings, url):
    request = urllib.request.Request(url)

    request.add_header("Authorization", settings['auth'])
    request.add_header("Accept", "application/json")
    request.add_header("Content-type", "application/json")    

    return http_call(request);

def update_record(settings, data, table, sys_id):
    url = "https://" + settings['instance'] + ".service-now.com/api/now/table/" + table + '/' + sys_id
    result_body = http_put(settings, url, data)
    result = json.loads(result_body)['result']
    return result


def get_record(settings, table, sys_id):
    url = "https://" + settings['instance'] + ".service-now.com/api/now/table/" + table + '/' + sys_id
    result_body = http_get(settings, url)
    result = json.loads(result_body)['result']
    return result


def create_record(settings, data, table):
    url = "https://" + settings['instance'] + ".service-now.com/" + table + ".do?JSONv2"
    url += "&sysparm_action=insert"

    return json.loads(http_post(settings, url, data))


# noinspection PyUnresolvedReferences,PyTypeChecker
def get_list(settings, table, query, fields="name"):
    try:
        query_params = [];

        url = "https://" + settings['instance'] + ".service-now.com/api/now/table/" + table
        
        if fields!="":
            query_params.append("sysparm_fields=" + fields)

        if query!="":
            query_params.append("sysparm_query=" + urllib.parse.quote(query.encode("utf-8")))


        url = url + "?" + "&".join(query_params)
        result_body = http_get(settings, url)

        response_data = json.loads(result_body)['result']

        return response_data
    except:
        print("An Error occurred while attempting to connect to the instance.")
        return False

def get_records_for_folder(folder, settings, query):
    if settings is not False:
        get_all_records(folder, settings, query)

    for name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, name)):
            if not is_multi(folder):
                get_records_for_folder(os.path.join(folder, name), settings, query)
    return


def get_all_records(folder, settings, query):
    table_settings = load_settings(folder)

    if settings is not False and table_settings is not False:

        if 'table' not in table_settings:
            print("Folder was not a ServiceNow Folder: "+folder)
            return

        print("Grabbing Records for folder: "+folder)

        items = get_list(settings, table_settings['table'], query)

        if 'sub' in table_settings:
            return

        if 'multi' in table_settings:
            for item in items:
                for field in os.listdir(folder):
                    field_path = os.path.join(folder, field)

                    if os.path.isdir(field_path):
                        sub_settings = load_settings(field_path)
                        body_field = field
                        name_field = sub_settings['display']
                        extension = sub_settings['extension']

                        name = item[name_field] + "." + extension

                        doc = item[body_field]

                        file_name = os.path.join(folder, field, convert_file_name(name))

                        save_if_newer(folder, item['sys_id'], name, file_name, doc, item['sys_updated_on'])

        else:
            for item in items:
                body_field = table_settings['body_field']
                name_field = table_settings['display']
                extension = table_settings['extension']
                name = item[name_field] + "." + extension

                doc = item[body_field]
                file_name = os.path.join(folder, convert_file_name(name))

                save_if_newer(folder, item['sys_id'], name, file_name, doc, item['sys_updated_on'])

    return            