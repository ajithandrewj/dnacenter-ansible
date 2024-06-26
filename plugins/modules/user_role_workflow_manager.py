#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
__author__ = ("Ajith Andrew J, Syed khadeer Ahmed")


DOCUMENTATION = r"""
---
module: user
short_description: Resource module for managing Users in Cisco Catalyst Center
description:
  - Manages operations to create, update, and delete users in the Cisco Catalyst Center system.
  - Allows adding a new user.
  - Supports updating an existing user.
  - Enables deleting a user.
version_added: '6.7.0'
extends_documentation_fragment:
  - cisco.dnac.workflow_manager_params
author:
  - Syed Khadeer Ahmed (@syed-khadeerahmed)
  - Ajith Andrew J (@ajithandrewj)

  options: merged, deleted
    first_name:
      description: The first name of the user.
      type: str
    last_name:
      description: The last name of the user.
      type: str
    username:
      description: The username for the user's account.
      type: str
    email:
      description: The email address of the user. Example Email: syedkhadeerahmed@example.com
      type: str
    password:
      description: The password for the user's account. Criteria: should contain 1 special character, capital letter, small letter and minimum length should be 15 characters 
      type: str
    role_list:
      description: A list of role name assigned to the user. It should be exactly as in the Cisco DNA center
      elements: str
      type: list

      
requirements:
  - dnacentersdk >= V2_3_7_6
  - python >= 3.9

see also:
  - name: Cisco Catalyst Center documentation for User and Roles AddUserAPI
    description: Complete reference of the GetUsersAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!get-users-api

  - name: Cisco Catalyst Center documentation for User and Roles AddUserAPI
    description: Complete reference of the AddUserAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!add-user-api
  
  - name: Cisco Catalyst Center documentation for User and Roles UpdateUserAPI
    description: Complete reference of the UpdateUserAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!update-user-api
  
  - name: Cisco Catalyst Center documentation for User and Roles DeleteUserAPI
    description: Complete reference of the DeleteUserAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!delete-user-api


notes:
  - SDK Methods used:
    - user_and_roles.UserandRoles.get_user_ap_i
    - user_and_roles.UserandRoles.add_user_ap_i
    - user_and_roles.UserandRoles.update_user_ap_i
    - user_and_roles.UserandRoles.delete_user_ap_i

  - Paths used:
    - get /dna/system/api/v1/user
    - post /dna/system/api/v1/user
    - put /dna/system/api/v1/user
    - delete /dna/system/api/v1/user/{userId}
"""

EXAMPLES = r"""
---
  - name: for user creation or updation or deleletion 
    cisco.dnac.user_workflow_manager:
      dnac_host: "{{ dnac_host }}"
      dnac_username: "{{ dnac_username }}"
      dnac_password: "{{ dnac_password }}"
      dnac_verify: "{{ dnac_verify }}"
      dnac_port: "{{ dnac_port }}"
      dnac_version: "{{ dnac_version }}"
      dnac_debug: "{{ dnac_debug }}"
      state: merged
      config:
        email: "syedkhadeer@example.com"
        first_name: "Syed Khadeer"
        last_name: "Ahmed"
        password: "password123"       
        role_list:
          - "Network Administrator"
        username: "syed"
        
"""

RETURN = r"""
# Case 1: User operation successful (create/update/delete)
response_1: create
  description: A dictionary with details of the API execution from Cisco Catalyst Center.
  returned: always
  type: dict
  sample:
    {
        "response": {
            "message": "string",
            "userId": "string"
        }
    }

response_2: update
  description: A dictionary with details of the API execution from Cisco Catalyst Center.
  returned: always
  type: dict
  sample:
    {
        "response": {
            "message": "string",
        }
    }

response_2: delete
  description: A dictionary with details of the API execution from Cisco Catalyst Center.
  returned: always
  type: dict
  sample:
    {
        "response": {
            "message": "string",
        }
    }

# Case 2: User exists and no action needed (for update)
response_2:
  description: A dictionary with existing user details indicating no update needed.
  returned: always
  type: dict
  sample:
    {
      "response": {
        "user": {
          "email": "user@example.com",
          "first_name": "John",
          "last_name": "Doe",
          "username": "johndoe",
          "role_list": ["Network Administrator"]
          # Additional user details as needed
        },
        "userId": "string",  # User ID from Cisco Catalyst Center
        "type": "string"
      },
      "msg": "User already exists and no update needed."
    }

# Case 3: Error during user operation (create/update/delete)
response_3:
  description: A dictionary with details of the API execution and error information.
  returned: always
  type: dict
  sample:
    {
      "response": {
        "msg": "Error during creating or updating or deleting the user."
      }
    }

# Case 4: User not found (during delete operation)
response_4:
  description: A dictionary indicating user not found during delete operation.
  returned: always
  type: dict
  sample:
    {
      "response": {
        "msg": "User not found."
    }
    }
"""


import re, time
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import (
    DnacBase,
    validate_list_of_dicts,
    validate_str,
    validate_list
)
from ansible.module_utils.basic import AnsibleModule


class User(DnacBase):
    """Class containing member attributes for user workflow_manager module"""

    def __init__(self, module):
        super().__init__(module)
        self.result["response"] = []
        self.supported_states = ["merged", "deleted"]
        self.payload = module.params
        self.keymap = {}


    # Below function used to validate input over the ansible validation
    def validate_input_yml(self):
        """
        Validate the fields provided in the yml files.
        Checks the configuration provided in the playbook against a predefined specification
        to ensure it adheres to the expected structure and data types based on input.
        Parameters:
          - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
        Returns:
          The method returns an instance of the class with updated attributes:
                - self.msg: A message describing the validation result.
                - self.status: The status of the validation (either 'success' or 'failed').
                - self.validated_config: If successful, a validated version of the 'config' parameter.
        Description:
          Example:
              To use this method, create an instance of the class and call 'validate_input_yml' on it.
              If the validation succeeds, 'self.status' will be 'success' and 'self.validated_config'
              will contain the validated configuration. If it fails, 'self.status' will be 'failed', and
              'self.msg' will describe the validation issues.
            If the validation succeeds, this will allow to go next step, unless this will stop execution.
            based on the fields.
        """

        self.log('Validating the Playbook Yaml File..', "INFO")

        if not self.config:
            self.status = "success"
            self.msg = "Configuration is not available in the playbook for validation"
            self.log(self.msg, "ERROR")
            return self
        
        userlist = self.payload.get("config")
        userlist = self.camel_to_snake_case(userlist)
        user_details = dict(first_name = dict(required = False, type = 'str'),
                    last_name = dict(required = False, type = 'str'),
                    email = dict(required = False, type = 'str'),
                    password = dict(required = False, type = 'str'),
                    username = dict(required = True, type = 'str'),
                    role_list = dict(required = False, type = 'list', elements='str'),
                    )
        valid_param, invalid_param = validate_list_of_dicts(userlist, user_details)

        if invalid_param:
            self.msg("Invalid param found in playbook: '{0}' "\
                            .format(", ".join(invalid_param)))
            self.log(self.msg, "ERROR")
            self.status = "failed"
            return self

        self.validated_config = valid_param
        self.msg = "Successfully validated playbook config params:{0}".format(str(valid_param[0]))
        self.log(self.msg, "INFO")
        self.status = "success"
        return self


    def valid_user_config_parameters(self, user_config):
        """
        Addtional validation for the create user configuration payload.
        Parameters:
          - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
          - ap_config (dict): A dictionary containing the input configuration details.
        Returns:
          The method returns an instance of the class with updated attributes:
                - self.msg: A message describing the validation result.
                - self.status: The status of the validation (either 'success' or 'failed').
        Description:
            Example:
                To use this method, create an instance of the class and call 
                'valid_create_user_config_parameters' on it. If the validation succeeds it return 'success'.
                If it fails, 'self.status' will be 'failed', and
                'self.msg' will describe the validation issues.To use this method, create an
                instance of the class and call 'valid_create_user_config_parameters' on it.
                If the validation succeeds, this will allow to go next step, 
                unless this will stop execution based on the fields.
        """

        errormsg = []

        if user_config.get("first_name"):
            param_spec = dict(type = "str", length_max = 255)
            validate_str(user_config["first_name"], param_spec, "first_name",
                            errormsg)

        if user_config.get("last_name"):
            param_spec = dict(type = "str", length_max = 255)
            validate_str(user_config["last_name"], param_spec, "last_name",
                            errormsg)

        if user_config.get("email"):
            email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if not email_regex.match(user_config["email"]):
                errormsg.append("email: Invalid email format for email: '{0}'".format(user_config["email"]))

        if user_config.get("password"):
            password_regex = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
            if not password_regex.match(user_config["password"]):
                errormsg.append("password: Password does not meet complexity requirements for password: '{0}'".format(user_config["password"]))

        if user_config.get("username"):
            param_spec = dict(type = "str", length_max = 255)
            validate_str(user_config["username"], param_spec, "username",
                            errormsg)

        if user_config.get("role_list"):
            param_spec = dict(type = "list", elements="str")
            validate_list(user_config["role_list"], param_spec, "role_list",
                            errormsg)

        if len(errormsg) > 0:
            self.msg = "Invalid parameters in playbook config: '{0}' "\
                     .format(str("\n".join(errormsg)))
            self.log(self.msg, "ERROR")
            self.status = "failed"
            return self

        self.msg = "Successfully validated config params:{0}".format(str(user_config))
        self.log(self.msg, "INFO")
        self.status = "success"
        return self


    def get_want(self, user_config):
        """
        Get all user-related information from the playbook needed for creation/updation/deletion of user in Cisco Catalyst Center.
        Parameters:
            self (object): An instance of a class used for interacting with Cisco Catalyst Center.
            config (dict): A dictionary containing user information.
        Returns:
            self (object): An instance of a class used for interacting with Cisco Catalyst Center.
        Description:
            Retrieves all user-related information from playbook that is
            required for creating a user in Cisco Catalyst Center. It includes
            parameters such as 'username' and 'email' The gathered
            information is stored in the 'want' attribute for later reference.
        """
        
        for key,value in user_config.items():
            self.want[key] = value
        self.log("Desired State (want): {0}".format(str(self.want)), "INFO")
        return self


    def get_have(self, input_config):
        """
        Get the user details from Cisco Catalyst Center
        Parameters:
          - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
          - input_config (dict): A dictionary containing the configuration details.
        Returns:
          - self (object): An instance of a class used for interacting with  Cisco Catalyst Center.
        Description:
            This method queries Cisco Catalyst Center to check if a specified user
            exists. If the user exists, it retrieves details about the current
            user, including the user ID and other relevant information. The
            results are stored in the 'have' attribute for later reference.
        """
        user_exists = False
        role_exists = False
        current_user_config = None
        current_role_config = None
        # check if given user config exists, if exists store current user info
        (user_exists, role_exists, current_user_config, current_role_config) = self.get_current_config(input_config)

        if not user_exists:
            self.log("The provided user '{0}' is not present in the Cisco Catalyst Center. User_exists = {1}".format(str(input_config.get("username")), str(user_exists)), "INFO")
        self.log("Current user config details (have): {0}".format(str(current_user_config)), "DEBUG")

        if user_exists:
            self.have["username"] = current_user_config.get("username")
            self.have["user_exists"] = user_exists
            self.have["current_user_config"] = current_user_config
            self.have["current_role_config"] = current_role_config
        else:
            self.have["user_exists"] = user_exists
        if role_exists:
            self.have["current_role_config"] = current_role_config

        self.log("Current State (have): {0}".format(str(self.have)), "INFO")
        return self


    def get_diff_merged(self, config):
        """
        Update/Create user in Cisco Catalyst Center with fields
        provided in the playbook.
        Parameters:
          self (object): An instance of a class used for interacting with Cisco Catalyst Center.
          config (dict): A dictionary containing configuration information.
        Returns:
            self (object): An instance of a class used for interacting with Cisco Catalyst Center.
        Description:
            This method determines whether to update or create user details in Cisco
            Catalyst Center based on the provided configuration information. 
            If the specified user exists, the method checks if it requires an update
            by calling the 'update_user_configuration' method. If an update is required, 
            it calls the 'configure_user' function from the 'user_and_roles' family of 
            the Cisco Catalyst Center API. If Current configuration same as input configuration 
            does not require an update, the method exits, indicating that user is up to date.
        """

        config_updated = False
        config_created = False
        task_response = None
        # check if the given user config exists and/or needs to be updated/created.

        if self.have.get("user_exists"):
            #update the user
            self.valid_user_config_parameters(config).check_return_status()
            (consolidated_data, update_required_param) = self.user_requires_update(self.have["current_user_config"], self.have["current_role_config"])

            if not consolidated_data:
                # user does not need update
                self.msg = "user does not need any update"
                self.log(self.msg, "INFO")
                responses = {}
                responses["users_updates"] = {"response": config}
                self.result['msg'] = self.msg
                self.result["response"].append(responses)
                self.result["skipped"] = True
                return self
            user_in_have = self.have["current_user_config"]
            update_param = update_required_param
            update_param["user_id"] = user_in_have.get("user_id")
            self.log('Final user data to update {}'.format(str(update_param)),
                  "INFO")
            task_response = self.update_user(update_param)
            task_res = str(task_response)
            self.log('Task respoonse {}'.format(str(task_res)),"INFO")
            config_updated = True

        else:
            # Create the user
            self.valid_user_config_parameters(config).check_return_status()
            self.log('Creating user with config {}'.format(str(config)), "INFO")
            user_params = self.want

            try:
                user_details = {}

                for key, value in user_params.items():
                    if value is not None:
                        if key != "role_list":
                            user_details[key] = value
                        else:
                            current_role= self.have.get("current_role_config")
                            user_details[key] = []
                            for role_name in user_params['role_list']:
                                role_id = current_role.get(role_name)
                                if role_id:
                                    user_details[key].append(role_id)
                                else:
                                    self.log("Role ID for {0} not found in current_role_config".format(str(role_name)))

                user_params = user_details
            except Exception as e:
                user_name = user_params['username']
                self.log("""The user '{0}' does not need additional filtering for 'None' values \
                         in the 'user_params' dictionary.""".format(user_name), "INFO")

            task_response = self.create_user(user_params)
            self.log('Task response {}'.format(str(task_response)), "INFO")
            config_created = True

        responses = {}
            
        if config_updated:
            responses["users_operation"] = {"response": task_res}
            self.msg = responses
            self.result['response'] = self.msg
            self.status = "success"
            self.log(self.msg, "INFO")

        if config_created:
            responses["users_operation"] = {"response": task_response}
            self.msg = responses
            self.result['response'] = self.msg
            self.status = "success"
            self.log(self.msg, "INFO")

        return self


    def get_current_config(self, input_config):
        """
        Check if the input user details exist in Cisco Catalyst Center.

        Parameters:
          - self (object): An instance of the class containing the method.

        Returns:
            A Dictionary list containing user details based on the input given from
            playbook

        Description:
            Checks the existence of a user and gets the user details in Cisco Catalyst Center
            by querying the 'get_user_ap_i' function in the 'user_and_roles' family to check
            the input data with current config data and return the above response.
        """

        user_exists = False
        role_exists = False
        current_user_configuration = {}
        current_role_configuration = {}
        response_user = None
        response_role = None
        input_param = {}

        if input_config.get("username") is not None and input_config.get("username") != "":
            input_param["username"] = input_config["username"]

        if input_config.get("role_list") and all(item for item in input_config.get("role_list")):
            input_param["role_list"] = input_config["role_list"]

        if not input_param:
            self.log("Required param username or role_list is not in playbook config", "ERROR")
            return (user_exists, current_user_configuration, current_role_configuration)

        try:

            response_user = self.dnac._exec(
                family="user_and_roles",
                function="get_users_ap_i",
                op_modifies=True,
                params={**input_param, 'invoke_source': 'external', 'auth_source': 'internal'},
            )

            response_role = self.dnac._exec(
                family="user_and_roles",
                function="get_roles_ap_i",
                op_modifies=True,
            )

        except Exception as e:
            self.log("The provided user '{0}' is either invalid or not present in the Cisco Catalyst Center."\
                     .format(str(input_param) + str(e)), "WARNING")

        if response_user and response_role:
            response_user = self.camel_to_snake_case(response_user)
            response_role = self.camel_to_snake_case(response_role)
            current_user_configuration = {}
            current_role_configuration = {}
            self.log("Received API response from 'get_users_api': {0}".format(str(response_user)), "DEBUG")
            self.log("Received API response from 'get_roles_api': {0}".format(str(response_role)), "DEBUG")

            users = response_user.get("response", {}).get("users", [])
            roles = response_role.get("response", {}).get("roles", [])

            for user in users:
                if user.get("username") == input_config.get("username"):
                    current_user_configuration = user
                    user_exists = True

            if input_config.get("role_list") != None:
              for role in roles:
                  if role.get("name") in input_config.get("role_list"):
                      current_role_configuration[role.get("name")] = role.get("role_id")
                      role_exists = True

        return (user_exists, role_exists, current_user_configuration, current_role_configuration)


    def create_user(self, user_params):
        """
        Create a new user in Cisco Catalyst Center with the provided parameters.
        Parameters:
            self (object): An instance of a class used for interacting with Cisco Catalyst Center.
            user_params (dict): A dictionary containing user information.
        Returns:
            response (dict): The API response from the 'create_user' function.
        Description:
            This method sends a request to create a new user in Cisco Catalyst Center using the provided
            user parameters. It logs the response and returns it.
        """
        user_info_params= self.snake_to_camel_case(user_params)
        self.log("Create user with user_info_params: {0}".format(str(user_info_params)), "DEBUG")
        response = self.dnac._exec(
            family="user_and_roles",
            function='add_user_ap_i',
            op_modifies=True,
            params=user_info_params,
        )
        self.log("Received API response from 'create_user': {0}".format(str(response)), "DEBUG")
        return response
    

    def user_requires_update(self, current_user, current_role):
        """
        Check if the user requires updates and save parameters to update.

        Parameters:
            current_user (dict): Dictionary containing current user information.
            current_role (dict): Dictionary containing role mappings.
            want (dict): Dictionary containing the desired user information.
            update_user_param (dict): Dictionary to store parameters that need to be updated.

        Returns:
            bool: True if the user requires updates, False otherwise.
        """

        update_required = False
        update_user_param = {}

        if current_user.get('first_name') != self.want.get('first_name'):
            update_user_param['first_name'] = self.want['first_name']
            update_required = True
        elif 'first_name' not in update_user_param:
            update_user_param['first_name'] = current_user['first_name']
        
        if current_user.get('last_name') != self.want.get('last_name'):
            update_user_param['last_name'] = self.want['last_name']
            update_required = True
        elif 'last_name' not in update_user_param:
            update_user_param['last_name'] = current_user['last_name']
        
        if current_user.get('email') != self.want.get('email'):
            update_user_param['email'] = self.want['email']
            update_required = True
        elif 'email' not in update_user_param:
            update_user_param['email'] = current_user['email']
        
        if current_user.get('username') != self.want.get('username'):
            update_user_param['username'] = self.want['username']
            update_required = True
        elif 'username' not in update_user_param:
            update_user_param['username'] = current_user['username']
        
        if current_user.get('role_list')[0] != current_role[self.want.get("role_list")[0]]:
            role_id = current_role[self.want.get("role_list")[0]]
            update_user_param['role_list'] = [role_id]
            update_required = True
        elif 'role_list' not in update_user_param:
            update_user_param['role_list'] = [current_role[self.want.get("role_list")[0]]]

        return (update_required,update_user_param)


    def update_user(self, user_params):
        """
        Update a user in Cisco Catalyst Center with the provided parameters.
        Parameters:
            self (object): An instance of a class used for interacting with Cisco Catalyst Center.
            user_params (dict): A dictionary containing user information.
        Returns:
            response (dict): The API response from the 'update_user' function.
        Description:
            This method sends a request to update a new user in Cisco Catalyst Center using the provided
            user parameters. It logs the response and returns it.
        """

        user_info_params= self.snake_to_camel_case(user_params)
        self.log("Update user with user_info_params: {0}".format(str(user_info_params)), "DEBUG")
        response = self.dnac._exec(
            family="user_and_roles",
            function='update_user_ap_i',
            op_modifies=True,
            params=user_info_params,
        )
        self.log("Received API response from 'update_user': {0}".format(str(response)), "DEBUG")
        return self

    def get_diff_deleted(self, config):
        """
          Delete a user from Cisco Catalyst Center based on the provided parameters.
          Parameters:
             self (object): An instance of a class used for interacting with Cisco Catalyst Center.
              user_params (dict): A dictionary containing user information, such as 'userId' and 'username'.
          Returns:
              response (dict): The API response from the 'delete_user' function.
          Description:
              This method sends a request to delete a user in Cisco Catalyst Center using the provided
               user parameters. It logs the response and returns it.
        """

        config_delete = False

        if self.have.get("user_exists"):
            self.valid_user_config_parameters(config).check_return_status()
            self.log('Deleting user with config {}'.format(str(config)), "INFO")

            # Check if the username exists in self.have
            current_user= self.have.get("current_user_config")
            user_id_to_delete = {}
            user_id_to_delete["user_id"] = current_user.get("user_id")
            task_response = self.delete_user(user_id_to_delete)
            self.log('Task response {}'.format(str(task_response)), "INFO")
            config_delete = True

            if config_delete:
                responses = {}
                responses["users_operation"] = {"response": task_response}
                self.msg = responses
                self.result['response'] = self.msg
                self.status = "success"
                self.log(self.msg, "INFO")

        return self


    def delete_user(self, user_params):
        """
        Delete a user in Cisco Catalyst Center with the provided parameters.
        Parameters:
            self (object): An instance of a class used for interacting with Cisco Catalyst Center.
            user_params (dict): A dictionary containing user information.
        Returns:
            response (dict): The API response from the 'delete_user' function.
        Description:
            This method sends a request to create a new user in Cisco Catalyst Center using the provided
            user parameters. It logs the response and returns it.
        """

        self.log("delete user with user_params: {0}".format(str(user_params)), "DEBUG")
        response = self.dnac._exec(
            family="user_and_roles",
            function='delete_user_ap_i',
            op_modifies=True,
            params=user_params,
        )
        self.log("Received API response from 'delete_user': {0}".format(str(response)), "DEBUG")
        return response


    def verify_diff_merged(self, config):
        """
        Verify the merged status(Creation/Updation) of user details in Cisco Catalyst Center.
        Args:
            - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
            - config (dict): The configuration details to be verified.
        Return:
            - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
        Description:
            This method checks the merged status of a configuration in Cisco Catalyst Center by retrieving the current state
            (have) and desired state (want) of the configuration, logs the states, and validates whether the specified
            user exists in the Catalyst Center configuration.
        """

        self.get_have(config)
        self.log("Current State (have): {0}".format(str(self.have)), "INFO")
        self.log("Desired State (want): {0}".format(str(self.want)), "INFO")

        # Code to validate ccc config for merged state
        user_exist = self.have.get("user_exists")
        user_name = self.want.get("username")

        if user_exist:
            self.status = "success"
            self.msg = "The requested user '{0}' is present in the Cisco Catalyst Center and its creation has been verified.".format(user_name)
            self.log(self.msg, "INFO")

        (require_update, updated_user_info) = self.user_requires_update(self.have["current_user_config"], self.have["current_role_config"])

        if not require_update:
            self.log("The update for user '{0}' has been successfully verified. The updated info - {1}".format(user_name, updated_user_info), "INFO")
            self. status = "success"
            return self

        self.log("""The playbook input for user '{0}' does not align with the Cisco Catalyst Center, indicating that the merge task
                 may not have executed successfully.""".format(user_name), "INFO")

        return self


    def verify_diff_deleted(self, config):
        """
        Verify the deletion status of user detail in Cisco Catalyst Center.
        Args:
            - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
            - config (dict): The configuration details to be verified.
        Return:
            - self (object): An instance of a class used for interacting with Cisco Catalyst Center.
        Description:
            This method checks the deletion status of a configuration in Cisco Catalyst Center.
            It validates whether the specified site exists in the Catalyst Center configuration.
        """

        self.get_have(config)
        self.log("Current State (have): {0}".format(str(self.have)), "INFO")
        self.log("Desired State (want): {0}".format(str(self.want)), "INFO")

        # Code to validate ccc config for delete state
        user_exist = self.have.get("user_exists")

        if not user_exist:
            self.status = "success"
            msg = """The requested user '{0}' has already been deleted from the Cisco Catalyst Center and this has been
                successfully verified.""".format(str(self.want.get("username")))
            self.log(msg, "INFO")
            return self
        self.log("""Mismatch between the playbook input for site '{0}' and the Cisco Catalyst Center indicates that
                 the deletion was not executed successfully.""".format(str(self.want.get("username"))), "INFO")

        return self
    

    def snake_to_camel_case(self, data):
            """
            This function converts keys from snake case to camel case in a given dictionary.
            
            Parameters:
            - data: type Dict: A dictionary with keys in snake case.

            Returns:
            A new dictionary with keys converted to camel case.
            """
            def to_camel_case(snake_str):
                components = snake_str.split('_')
                return components[0] + ''.join(x.title() for x in components[1:])

            if isinstance(data, dict):
                camel_case_data = {}
                for key, value in data.items():
                    new_key = to_camel_case(key)

                    if isinstance(value, dict):
                        camel_case_data[new_key] = self.snake_to_camel_case(value)
                    elif isinstance(value, list):
                        camel_case_data[new_key] = [self.snake_to_camel_case(item) if isinstance(item, dict) else item for item in value]
                    else:
                        camel_case_data[new_key] = value

                return camel_case_data
            elif isinstance(data, list):
                return [self.snake_to_camel_case(item) if isinstance(item, dict) else item for item in data]
            else:
                return data


def main():
    """ main entry point for module execution
    """
    # Basic Ansible type check or assign default.
    user_details = {'dnac_host': {'required': True, 'type': 'str'},
                    'dnac_port': {'type': 'str', 'default': '443'},
                    'dnac_username': {'type': 'str', 'default': 'admin'},
                    'dnac_password': {'type': 'str', 'no_log': True},
                    'dnac_verify': {'type': 'bool', 'default': 'True'},
                    'dnac_version': {'type': 'str', 'default': '2.2.3.3'},
                    'dnac_debug': {'type': 'bool', 'default': False},
                    'dnac_log': {'type': 'bool', 'default': False},
                    'dnac_log_level': {'type': 'str', 'default': 'WARNING'},
                    "dnac_log_file_path": {"type": 'str', "default": 'dnac.log'},
                    'config_verify': {'type': 'bool', "default": False},
                    "dnac_log_append": {"type": 'bool', "default": True},
                    'dnac_api_task_timeout': {'type': 'int', "default": 1200},
                    'dnac_task_poll_interval': {'type': 'int', "default": 2},
                    'config': {'required': True, 'type': 'list', 'elements': 'dict'},
                    'validate_response_schema': {'type': 'bool', 'default': True},
                    'state': {'default': 'merged', 'choices': ['merged', 'deleted']}
                }

    module = AnsibleModule(
        argument_spec=user_details,
        supports_check_mode=True
    )

    ccc_user = User(module)
    state = ccc_user.params.get("state")

    if state not in ccc_user.supported_states:
        ccc_user.status = "invalid"
        ccc_user.msg = "State {0} is invalid".format(state)
        ccc_user.check_return_status()

    ccc_user.validate_input_yml().check_return_status()
    config_verify = ccc_user.params.get("config_verify")

    for config in ccc_user.validated_config:
        ccc_user.reset_values()
        ccc_user.get_want(config).check_return_status()
        ccc_user.get_have(config).check_return_status()
        ccc_user.get_diff_state_apply[state](config).check_return_status()
        
        if config_verify:
            time.sleep(5)
            ccc_user.verify_diff_state_apply[state](config).check_return_status()

    module.exit_json(**ccc_user.result)

if __name__ == '__main__':
    main()
