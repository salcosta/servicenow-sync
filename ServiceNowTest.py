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

# 'import http.cookiejar
# 'import string


table_field_list = '{"asmt_metric": [{"field": "script","extension": "js"}],"automation_pipeline_transformer_javascript": [{"field": "script","extension": "js"}],"bsm_chart": [{"field": "chart","extension": "js"}, {"field": "filter","extension": "js"}],"bsm_context_menu": [{"field": "script","extension": "js"}],"bsm_map_filter": [{"field": "filter","extension": "js"}],"chat_queue": [{"field": "not_available","extension": "html"}],"ci_identifier": [{"field": "script","extension": "js"}],"clm_contract_history": [{"field": "terms_and_conditions","extension": "html"}],"clone_cleanup_script": [{"field": "script","extension": "js"}],"cmdb_ci_outage": [{"field": "details","extension": "html"}],"cmdb_ci_translation_rule": [{"field": "rule","extension": "js"}],"cmdb_depreciation": [{"field": "script","extension": "js"}],"cmdb_sw_license_calculation": [{"field": "calculation","extension": "js"}],"cmn_map_page": [{"field": "script","extension": "js"}],"cmn_relative_duration": [{"field": "script","extension": "js"}],"cmn_schedule_page": [{"field": "client_script","extension": "js"}, {"field": "server_script","extension": "js"}],"connect_action": [{"field": "script","extension": "js"}],"content_block": [{"field": "condition","extension": "js"}],"content_block_detail": [{"field": "script","extension": "js"}],"content_block_lists": [{"field": "script","extension": "js"}],"content_block_programmatic": [{"field": "programmatic_content","extension": "html"}],"content_css": [{"field": "style","extension": "css"}],"content_page_rule": [{"field": "advanced_condition","extension": "js"}],"content_type_detail": [{"field": "script","extension": "js"}],"cxs_table_config": [{"field": "search_as_script","extension": "js"}],"diagrammer_action": [{"field": "script","extension": "js"}],"discovery_classy": [{"field": "script","extension": "js"}],"discovery_port_probe": [{"field": "script","extension": "js"}],"discovery_probes": [{"field": "script","extension": "js"}, {"field": "post_processor_script","extension": "js"}],"ecc_agent_capability_value_test": [{"field": "script","extension": "js"}],"ecc_agent_ext": [{"field": "script","extension": "js"}],"ecc_agent_script": [{"field": "script","extension": "js"}],"ecc_agent_script_include": [{"field": "script","extension": "js"}],"ecc_handler": [{"field": "condition_script","extension": "js"}, {"field": "script","extension": "js"}],"expert_panel_template": [{"field": "script","extension": "js"}],"expert_panel_transition": [{"field": "transition_script","extension": "js"}],"fm_distribution_cost_rule": [{"field": "script","extension": "js"}],"fm_expense_allocation_rule": [{"field": "script","extension": "js"}],"item_option_new": [{"field": "description","extension": "html"}],"itil_agreement_ci": [{"field": "description","extension": "html"}],"itil_agreement_target_ci": [{"field": "description","extension": "html"}],"kb_submission": [{"field": "text","extension": "html"}],"live_table_notification": [{"field": "before_script","extension": "js"}],"metric_definition": [{"field": "script","extension": "js"}],"ngbsm_context_menu": [{"field": "script","extension": "js"}],"ngbsm_filter": [{"field": "filter","extension": "js"}],"ngbsm_script": [{"field": "script_plain","extension": "js"}],"ola": [{"field": "performance","extension": "html"}],"pa_scripts": [{"field": "script","extension": "js"}],"planned_change_validation_script": [{"field": "script","extension": "js"}],"planned_task": [{"field": "html_description","extension": "html"}],"pm_portfolio_project": [{"field": "html_description","extension": "html"}],"process_guide": [{"field": "advanced_condition","extension": "js"}],"process_step_approval": [{"field": "approval_script","extension": "js"}, {"field": "approver_script","extension": "js"}, {"field": "rejection_script","extension": "js"}],"proposed_change_verification_rules": [{"field": "rule_script","extension": "js"}],"question": [{"field": "default_html_value","extension": "html"}],"release_feature": [{"field": "documentation","extension": "html"}],"release_task": [{"field": "documentation","extension": "html"}],"risk_conditions": [{"field": "advanced_condition","extension": "js"}],"sc_cart_item": [{"field": "hints","extension": "html"}],"sc_cat_item": [{"field": "delivery_plan_script","extension": "js"}, {"field": "entitlement_script","extension": "js"}],"sc_cat_item_delivery_task": [{"field": "condition_script","extension": "js"}, {"field": "generation_script","extension": "js"}],"sc_cat_item_dt_approval": [{"field": "approval_script","extension": "js"}],"sc_cat_item_guide": [{"field": "validator","extension": "js"}, {"field": "script","extension": "js"}],"sc_cat_item_option": [{"field": "description","extension": "html"}],"sc_cat_item_producer": [{"field": "script","extension": "js"}],"sc_category": [{"field": "entitlement_script","extension": "js"}],"sc_ic_aprvl_type_defn": [{"field": "approver_script","extension": "js"}],"sc_ic_aprvl_type_defn_staging": [{"field": "approver_script","extension": "js"}],"sc_ic_task_assign_defn": [{"field": "assignment_script","extension": "js"}],"sc_ic_task_assign_defn_staging": [{"field": "assignment_script","extension": "js"}],"scheduled_data_export": [{"field": "pre_script","extension": "js"}],"scheduled_data_export": [{"field": "post_script","extension": "js"}],"sf_sm_order": [{"field": "auto_script_script","extension": "js"}, {"field": "ui_action_script","extension": "js"}],"sf_sm_task": [{"field": "auto_script_script","extension": "js"}, {"field": "ui_action_script","extension": "js"}],"sf_state_flow": [{"field": "automatic_script","extension": "js"}, {"field": "manual_script","extension": "js"}],"signature_image": [{"field": "signed_name","extension": "html"}, {"field": "data","extension": "js"}],"sla": [{"field": "reponsibilities","extension": "html"}, {"field": "change_procedures","extension": "html"}, {"field": "disaster_recovery","extension": "html"}, {"field": "notes","extension": "html"}, {"field": "description","extension": "html"}, {"field": "signatures","extension": "html"}, {"field": "service_goals","extension": "html"}, {"field": "security_notes","extension": "html"}, {"field": "incident_procedures","extension": "html"}],"sn_sec_cmn_calculator": [{"field": "script_values","extension": "js"}, {"field": "advanced_condition","extension": "js"}],"sn_sec_cmn_integration": [{"field": "integration_factory_script","extension": "js"}, {"field": "processor_factory_script","extension": "js"}],"sn_si_incident": [{"field": "pir","extension": "html"}],"sn_si_severity_calculator": [{"field": "advanced_condition","extension": "js"}],"sp_angular_provider": [{"field": "script","extension": "js"}],"sp_css": [{"field": "css","extension": "css"}],"sp_instance": [{"field": "css","extension": "css"}, {"field": "widget_parameters","extension": "js"}],"sp_ng_template": [{"field": "template","extension": "html"}],"sp_page": [{"field": "css","extension": "css"}],"sp_portal": [{"field": "quick_start_config","extension": "js"}],"sp_rectangle_menu_item": [{"field": "record_script","extension": "js"}],"sp_widget": [{"field": "template","extension": "html"}, {"field": "css","extension": "css"}, {"field": "link","extension": "js"}, {"field": "client_script","extension": "js"}, {"field": "script","extension": "js"}],"sys_amb_processor": [{"field": "user_subscribe_listener","extension": "js"}, {"field": "channel_create_advanced_authorization","extension": "js"}, {"field": "message_send_advanced_authorization","extension": "js"}, {"field": "user_unsubscribe_listener","extension": "js"}, {"field": "message_send_listener","extension": "js"}, {"field": "message_receive_listener","extension": "js"}, {"field": "channel_subscribe_advanced_authorization","extension": "js"}, {"field": "message_receive_advanced_authorization","extension": "js"}],"sys_dictionary": [{"field": "calculation","extension": "js"}],"sys_email_canned_message": [{"field": "body","extension": "html"}],"sys_embedded_help_action": [{"field": "onclick","extension": "js"}],"sys_home": [{"field": "text","extension": "html"}],"sys_impex_entry": [{"field": "script","extension": "js"}],"sys_impex_map": [{"field": "script","extension": "js"}],"sys_installation_exit": [{"field": "script","extension": "js"}],"sys_listener_detail": [{"field": "script","extension": "js"}],"sys_nav_link": [{"field": "url_script","extension": "js"}, {"field": "text_script","extension": "js"}],"sys_navigator": [{"field": "script","extension": "js"}],"sys_process_flow": [{"field": "description","extension": "html"}],"sys_processor": [{"field": "script","extension": "js"}],"sys_push_notif_act_script": [{"field": "script","extension": "js"}],"sys_push_notif_msg_content": [{"field": "script","extension": "js"}],"sys_relationship": [{"field": "insert_callback","extension": "js"}, {"field": "apply_to","extension": "js"}, {"field": "query_from","extension": "js"}, {"field": "query_with","extension": "js"}],"sys_report": [{"field": "content","extension": "html"}],"sys_script": [{"field": "script","extension": "js"}],"sys_script_ajax": [{"field": "script","extension": "js"}],"sys_script_client": [{"field": "script","extension": "js"}],"sys_script_email": [{"field": "script","extension": "js"}],"sys_script_fix": [{"field": "script","extension": "js"}],"sys_script_include": [{"field": "script","extension": "js"}],"sys_script_validator": [{"field": "validator","extension": "js"}],"sys_security_acl": [{"field": "script","extension": "js"}],"sys_service_api": [{"field": "script","extension": "js"}],"sys_soap_message": [{"field": "wsdl_xml","extension": "html"}],"sys_soap_message_function": [{"field": "envelope","extension": "html"}],"sys_soap_message_import": [{"field": "external_document","extension": "html"}],"sys_soap_message_test": [{"field": "response","extension": "html"}, {"field": "request","extension": "html"}],"sys_transform_entry": [{"field": "source_script","extension": "js"}],"sys_transform_map": [{"field": "script","extension": "js"}],"sys_transform_script": [{"field": "script","extension": "js"}],"sys_ui_action": [{"field": "script","extension": "js"}],"sys_ui_context_menu": [{"field": "dynamic_actions_script","extension": "js"}, {"field": "on_show_script","extension": "js"}, {"field": "action_script","extension": "js"}],"sys_ui_list_control": [{"field": "edit_condition","extension": "js"}, {"field": "new_condition","extension": "js"}, {"field": "link_condition","extension": "js"}, {"field": "empty_condition","extension": "js"}, {"field": "filter_condition","extension": "js"}, {"field": "columns_condition","extension": "js"}],"sys_ui_list_control_embedded": [{"field": "new_condition","extension": "js"}, {"field": "empty_condition","extension": "js"}, {"field": "columns_condition","extension": "js"}, {"field": "link_condition","extension": "js"}],"sys_ui_list_script_client": [{"field": "script","extension": "js"}],"sys_ui_list_script_server": [{"field": "script","extension": "js"}],"sys_ui_macro": [{"field": "xml","extension": "html"}],"sys_ui_ng_action": [{"field": "script","extension": "js"}],"sys_ui_page": [{"field": "html","extension": "html"}, {"field": "processing_script","extension": "js"}, {"field": "client_script","extension": "js"}],"sys_ui_policy": [{"field": "script_true","extension": "js"}, {"field": "script_false","extension": "js"}],"sys_ui_script": [{"field": "script","extension": "js"}],"sys_ui_title": [{"field": "script","extension": "js"}],"sys_update_diff": [{"field": "payload_diff","extension": "html"}],"sys_update_preview_xml": [{"field": "payload_diff","extension": "html"}],"sys_upgrade_history_log": [{"field": "payload_diff","extension": "html"}],"sys_web_service": [{"field": "script","extension": "js"}],"sys_widgets": [{"field": "script","extension": "js"}],"sys_ws_operation": [{"field": "operation_script","extension": "js"}],"sysauto": [{"field": "condition","extension": "js"}],"sysauto_report": [{"field": "report_body","extension": "html"}],"sysauto_script": [{"field": "script","extension": "js"}],"sysevent_email_action": [{"field": "message_html","extension": "html"}, {"field": "advanced_condition","extension": "js"}],"sysevent_email_style": [{"field": "style","extension": "html"}],"sysevent_email_template": [{"field": "message_html","extension": "html"}],"sysevent_in_email_action": [{"field": "reply_email","extension": "html"}, {"field": "script","extension": "js"}],"sysevent_script_action": [{"field": "script","extension": "js"}],"sysrule_escalate": [{"field": "advanced_condition","extension": "js"}, {"field": "assignment_script","extension": "js"}],"sysrule_view": [{"field": "script","extension": "js"}],"task_activity": [{"field": "message","extension": "html"}],"tm_test": [{"field": "test_data","extension": "html"}, {"field": "test_description","extension": "html"}],"tm_test_case": [{"field": "prereq","extension": "html"}],"tm_test_case_instance": [{"field": "prereq","extension": "html"}],"tm_test_instance": [{"field": "test_description","extension": "html"}],"tm_test_plan": [{"field": "instructions","extension": "html"}],"treemap_metric": [{"field": "custom_script","extension": "js"}, {"field": "click_through_url_script","extension": "js"}],"u_field_testing": [{"field": "u_html","extension": "html"}],"usageanalytics_count_cfg": [{"field": "script","extension": "js"}],"user_criteria": [{"field": "script","extension": "js"}],"wf_activity_definition": [{"field": "script","extension": "js"}],"wf_element_activity": [{"field": "input_process_script","extension": "js"}, {"field": "processing_script","extension": "js"}, {"field": "output_process_script","extension": "js"}],"wf_workflow_version": [{"field": "on_cancel","extension": "js"}],"workbench_config": [{"field": "phase_actions","extension": "js"}]}'


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

        if settings is not False:
            full_file_name = view.file_name()
            file_path = get_file_path(full_file_name)
            file_name = get_file_name(full_file_name)
            file_type = get_file_type(full_file_name)

            if file_name == "service-now.json" or file_type == "spec":
                return False

            table_settings = load_settings(file_path)

            if table_settings is False:
                return False

            reg = sublime.Region(0, view.size())
            text = view.substr(reg)
            data = dict()
            data[table_settings['body_field']] = text

            if file_name in table_settings['files']:
                sys_id = table_settings['files'][file_name]['sys_id']
                result = get_record(settings, table_settings['table'], sys_id)

                if result is not False:
                    item = result[0]

                    body_field = table_settings['body_field']

                    doc = item[body_field]
                    diffs = diff_file_to_doc(full_file_name, doc)

                    if diffs:
                        diffs = diff_doc_to_doc(text, doc)
                        if diffs:
                            action = sublime.yes_no_cancel_dialog("Remote record does not match local.",
                                                                  "Overwrite Remote", "View Differences")
                            if action == sublime.DIALOG_YES:
                                result = update_record(settings, data, table_settings['table'], sys_id)
                                print(json.dumps(result))
                                add_file(file_path, sys_id, file_name, result['records'][0]['sys_updated_on'])

                            if action == sublime.DIALOG_NO:
                                diffs = map(lambda line: (line and line[-1] == "\n") and line or line + "\n", diffs)
                                diffs = ''.join(diffs)
                                scratch = view.window().new_file()
                                scratch.set_scratch(True)
                                scratch.run_command('create_diff_scratch', {'content': diffs})

                            return False

                        else:
                            return True

                    result = update_record(settings, data, table_settings['table'], sys_id)
                    add_file(file_path, sys_id, file_name, time.mktime(convert_time(result['records'][0]['sys_updated_on']).timetuple()))

            else:
                data[table_settings['display']] = str.replace(file_name, "." + table_settings['extension'], "")
                result = create_record(settings, data, table_settings['table'])

                if result is not False:
                    add_file(file_path, result['records'][0]['sys_id'], file_name, time.mktime(convert_time(result['records'][0]['sys_updated_on']).timetuple()))


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
            self.items = get_list(settings, self.table_settings['table'], query)
            item_list = []

            for item in self.items:
                item_list.append([item[self.table_settings['display']], item['sys_id']])

            self.window.show_quick_panel(item_list, self.on_done)

    def on_done(self, index):
        if index != -1:
            item = self.items[index]

            if 'multi' in self.table_settings:
                for child in os.listdir(self.file_dir):
                    test_path = os.path.join(self.file_dir, child)
                    if os.path.isdir(test_path):
                        sub_settings = load_settings(test_path)
                        body_field = child
                        name_field = sub_settings['display']
                        extension = sub_settings['extension']
                        name = item[name_field] + "." + extension

                        doc = item[body_field]
                        file_name = os.path.join(self.file_dir, child, name)

                        if os.path.exists(file_name):
                            if sublime.ok_cancel_dialog("File already exists.\nOverwrite?") is False:
                                return False

                        write_doc_file(file_name, doc)

                        add_file(test_path, item['sys_id'], name)

            else:
                body_field = self.table_settings['body_field']
                name_field = self.table_settings['display']
                extension = self.table_settings['extension']
                name = item[name_field] + "." + extension

                doc = item[body_field]
                file_name = os.path.join(self.file_dir, name)

                if os.path.exists(file_name):
                    if sublime.ok_cancel_dialog("File already exists.\nOverwrite?") is False:
                        return False

                write_doc_file(file_name, doc)

                add_file(self.file_dir, item['sys_id'], name)

                self.window.open_file(os.path.join(self.file_dir, name))

            return

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0


class ChangeTableConfig(sublime_plugin.WindowCommand):
    working_dir = ""
    file_dir = ""
    table_settings = {}

    def run(self, dirs):
        self.working_dir = self.window.folders()[0]
        self.file_dir = dirs[0]
        self.table_settings = load_settings(self.file_dir)

        self.window.show_input_panel("Display Field:", self.table_settings['display'], self.get_display_field, None,
                                     None)

    def get_display_field(self, display):
        self.table_settings['display'] = display

        self.window.show_input_panel("Body Field:", self.table_settings['body_field'], self.get_extension, None, None)
        return

    def get_extension(self, body_field):
        self.table_settings['body_field'] = body_field

        self.window.show_input_panel("File Extension:", self.table_settings['extension'], self.create_settings, None,
                                     None)
        return

    def create_settings(self, extension):
        self.table_settings['extension'] = extension

        save_settings(self.file_dir, self.table_settings)
        return

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0


class LoadAllSnowRecordCommand(sublime_plugin.WindowCommand):
    this_dirs = []

    def run(self, dirs):
        self.this_dirs = dirs
        self.window.show_input_panel("Enter an encoded query (or leave blank):", "", self.get_records, None, None)
        return

    def get_records(self, query):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)

        for file_dir in self.this_dirs:
            get_records_for_folder(file_dir, settings, query)

        return

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0


class LoadMyRecordCommand(sublime_plugin.WindowCommand):
    this_dirs = []

    def run(self, dirs):
        self.this_dirs = dirs

        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)

        auth = settings["auth"].replace("Basic ", "")
        credentials = base64.decodestring(bytes(auth, "utf-8"))
        cred = credentials.decode("utf-8")
        user = cred.split(":")[0]

        for file_dir in self.this_dirs:
            get_records_for_folder(file_dir, settings, "sys_updated_by=" + user)

        return

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0


class LoadModifiedRecordCommand(sublime_plugin.WindowCommand):
    this_dirs = []

    def run(self, dirs):
        self.this_dirs = dirs

        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)

        for file_dir in self.this_dirs:
            get_records_for_folder(file_dir, settings, "sys_customer_update=true")

        return

    def is_visible(self, dirs):
        return is_sn(self.window.folders()) and len(dirs) > 0


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

        if file_name in table_settings['files']:
            sys_id = table_settings['files'][file_name]['sys_id']
            result = get_record(settings, table_settings['table'], sys_id)

            if result is not False:
                item = result[0]

                body_field = table_settings['body_field']

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


class TestConnectionCommand(sublime_plugin.WindowCommand):
    def run(self):
        working_dir = self.window.folders()[0]
        settings = load_settings(working_dir)

        if settings is not False:
            response = get_list(settings, "sys_properties", "")
            if response is not False:
                sublime.message_dialog("Connection Successful.")
            else:
                sublime.message_dialog("Connection Unsuccessful.")

        return

    def is_visible(self):
        return is_sn(self.window.folders())


class CreateConnectionCommand(sublime_plugin.WindowCommand):
    settings = dict()
    user = ""
    dir = ""

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
        cred = self.user + ":" + password
        encoded_cred = base64.encodestring(bytes(cred, "utf-8"))

        self.settings['auth'] = "Basic " + encoded_cred.decode("utf-8").replace("\n", "")
        save_settings(self.dir, self.settings)

    def is_visible(self):
        return is_sn(self.window.folders()) == False


class EnterCredentialsCommand(sublime_plugin.WindowCommand):
    settings = dict()
    user = ""
    dir = ""

    def run(self):
        self.dir = self.window.folders()[0]
        self.window.show_input_panel("User Name:", "", self.create_user, None, None)

    def create_user(self, user):
        self.user = user
        self.window.show_input_panel("Password:", "", self.create_pass, None, None)

    def create_pass(self, password):
        cred = self.user + ":" + password
        encoded_cred = base64.encodestring(bytes(cred, "utf-8"))
        save_setting(self.dir, "auth", "Basic " + encoded_cred.decode("utf-8").replace("\n", ""))

    def is_visible(self):
        return is_sn(self.window.folders()) == True


class CreateDiffScratchCommand(sublime_plugin.TextCommand):
    def run(self, edit, content):
        self.view.insert(edit, 0, content)


def write_doc_file(the_file, doc):
    f = open(the_file, 'wb')
    f.write(bytes(doc, 'utf-8'))
    f.close()

    return


def is_sn(dirs):
    if len(dirs) == 0:
        return False

    settings_file = os.path.join(dirs[0], "service-now.json")
    return os.path.exists(settings_file)


def convert_time(timestamp):
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")


def save_if_newer(the_dir, the_id, name, the_file, doc, timestamp=False):
    settings = load_settings(the_dir)
    update_time = datetime.now()
    prompt = False
    message = ""

    if timestamp is not False:
        update_time = convert_time(timestamp)

    # 'Get the files date here
    file_name = os.path.join(the_dir, name)

    if os.path.isfile(file_name):
        if name in settings['files']:
            if 'update_time' in settings['files'][name]:
                file_time = datetime.fromtimestamp(settings['files'][name]['update_time'])
                if update_time > file_time:
                    prompt = True
                    message = "There's a NEWER version of File '" + name + "' on the instance.\nOverwrite?"
                if file_time > update_time:
                    prompt = True
                    message = "There's an OLDER version of File '" + name + "' on the instance.\n"+str(time.mktime(file_time.timetuple()))+" ==? "+str(time.mktime(update_time.timetuple()))+"\nOverwrite?"
            else:
                prompt = True
                message = "File '" + name + "' has no timestamp on record, and may be out of sync with the instance.\nOverwrite?"

    if prompt is not False:
        if sublime.ok_cancel_dialog(message) is False:
            return False

    write_doc_file(the_file, doc)
    add_file(the_dir, the_id, name, time.mktime(update_time.timetuple()))
    return True


def add_file(the_dir, the_id, name, update_time=time.time()):
    settings = load_settings(the_dir)

    if name in settings['files']:
        settings['files'][name]['sys_id'] = the_id
        settings['files'][name]['update_time'] = update_time
    else:
        settings['files'][name] = dict()
        settings['files'][name]['sys_id'] = the_id
        settings['files'][name]['update_time'] = update_time

    save_settings(the_dir, settings)


def load_settings(the_dir):
    settings_file = os.path.join(the_dir, "service-now.json")

    if os.path.exists(settings_file) is False:
        return False

    f = open(settings_file, 'r')
    json_data = f.read()
    settings = json.loads(json_data)

    return settings


def save_settings(the_dir, settings):
    settings_file = os.path.join(the_dir, "service-now.json")
    f = open(settings_file, 'wb')
    f.write(bytes(json.dumps(settings, indent=4), 'utf-8'))
    f.close()


def save_setting(the_dir, key, value):
    settings_file = os.path.join(the_dir, "service-now.json")
    settings = load_settings(the_dir)
    settings[key] = value

    f = open(settings_file, 'wb')
    f.write(bytes(json.dumps(settings, indent=4), 'utf-8'))
    f.close()

    return True


def diff_file_to_doc(full_file_name, doc):
    f = codecs.open(full_file_name, 'r', "utf-8")
    original_doc = prep_content(f.read())
    f.close()
    new_doc = prep_content(doc)
    diffs = list(difflib.unified_diff(original_doc, new_doc))

    return diffs


def diff_doc_to_doc(original_doc, doc):
    original_doc = prep_content(original_doc)
    new_doc = prep_content(doc)
    diffs = list(difflib.unified_diff(original_doc, new_doc))

    return diffs


# noinspection PyUnresolvedReferences
def http_call(settings, url, data="", content="application/json"):
    if type(data) == dict:
        data = json.dumps(data).encode('utf8')

    err = ""
    timeout = 5
    result = ""

    if data != "":
        request = urllib.request.Request(url, data)
    else:
        request = urllib.request.Request(url)

    request.add_header("Authorization", settings['auth'])

    if content != "":
        request.add_header("Content-type", content)

    try:
        http_file = urllib.request.urlopen(request, timeout=timeout)
        result = http_file.read()
    except urllib.error.HTTPError as e:
        err = 'Error %s' % (str(e.code))
    except urllib.error.URLError as e:
        err = 'Error %s' % (str(e.code))

    if err != "":
        print(err)
        return False
    else:
        return result.decode()


def update_record(settings, data, table, sys_id):
    url = "https://" + settings['instance'] + ".service-now.com/" + table + ".do?JSONv2"
    url += "&sysparm_action=update"
    url += "&sysparm_query=sys_id=" + sys_id

    return json.loads(http_call(settings, url, data))


def get_record(settings, table, sys_id):
    url = "https://" + settings['instance'] + ".service-now.com/" + table + ".do?JSONv2"
    url = url + "&sysparm_query=sys_id=" + sys_id

    response_data = json.loads(http_call(settings, url))['records']

    return response_data


def create_record(settings, data, table):
    url = "https://" + settings['instance'] + ".service-now.com/" + table + ".do?JSONv2"
    url += "&sysparm_action=insert"

    return json.loads(http_call(settings, url, data))


# noinspection PyUnresolvedReferences,PyTypeChecker
def get_list(settings, table, query):
    data = dict()
    url = "https://" + settings['instance'] + ".service-now.com/" + table + ".do?JSONv2"
    if query != "":
        url = url + "&sysparm_query=" + urllib.parse.quote(query.encode("utf-8"))

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


def get_file_path(full_file_name):
    file_pieces = re.split(r"(?i)[\\/]", full_file_name)
    file_pieces.pop()
    full_path = '/'.join(file_pieces)

    return full_path


def get_file_name(full_file_name):
    file_pieces = re.split(r"(?i)[\\/]", full_file_name)
    file_name = file_pieces[len(file_pieces) - 1]

    return file_name


def get_file_type(full_file_name):
    file_pieces = re.split(r"(?i)[\\/]", full_file_name)
    file_type = file_pieces[len(file_pieces) - 2]

    return file_type


def get_records_for_folder(folder, settings, query):
    if settings is not False:
        get_all_records(folder, settings, query)

    for name in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, name)):
            get_records_for_folder(os.path.join(folder, name), settings, query)
    return


def get_all_records(folder, settings, query):
    table_settings = load_settings(folder)

    if settings is not False and table_settings is not False:

        if 'table' not in table_settings.keys():
            return

        items = get_list(settings, table_settings['table'], query)

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

                        file_name = os.path.join(folder, field, name)

                        save_if_newer(folder, item['sys_id'], name, file_name, doc, item['sys_updated_on'])

        else:
            for item in items:
                body_field = table_settings['body_field']
                name_field = table_settings['display']
                extension = table_settings['extension']
                name = item[name_field] + "." + extension

                doc = item[body_field]
                file_name = os.path.join(folder, name)

                save_if_newer(folder, item['sys_id'], name, file_name, doc, item['sys_updated_on'])


    return
