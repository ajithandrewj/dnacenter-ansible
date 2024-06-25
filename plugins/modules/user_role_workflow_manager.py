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

options:
  create_user:
    email:
      description: The email address of the user. Example Email: syedkhadeerahmed@example.com
      type: str
    first_name:
      description: The first name of the user.
      type: str
    last_name:
      description: The last name of the user.
      type: str
    password:
      description: The password for the user's account. Criteria: should contain 1 special character, capital letter, small letter and minimum length should be 15 characters 
      type: str
    username:
      description: The username for the user's account.
      type: str
    role_list:
      description: A list of role name assigned to the user. It should be exactly as in the Cisco DNA center
      elements: str
      type: list

  update_user:
    email:
      description: The email address of the user. This must be set if the original value is not empty.
                   Example Email: syedkhadeerahmed@example.com
      type: str
    first_name:
      description: The first name of the user. This must be set if the original value is not empty.
      type: str
    last_name:
      description: The last name of the user. This must be set if the original value is not empty.
      type: str
    username:
      description: The username for the user's account.
      type: str
    role_list:
      description: A list of role name assigned to the user. It should be exactly as in the Cisco DNA center
      elements: str
      type: list

  delete_user:
    username:
      description: The username of the user to be deleted.
      type: str
      required: true
  
  For Role Create or Update for each sub-param:
  description: User must select any one of the options "Deny or Read or Write" for each parameter.
  type: str
  create_new_custom_role:
    # Assigning permissions for each parameter in the playbook.
    - Assurance:
        Monitoring_and_Troubleshooting: "Deny/Read/Write"
        Monitoring_Settings: "Deny/Read/Write"
        Troubleshooting_Tools: "Deny/Read/Write"
    - Network_Analytics:
        Data_Access: "Deny/Read/Write"  # Restricting data access permissions.
    - Network_Design:
        # Restricting advanced network settings and configurations.
        Advanced_Network_Settings: "Deny/Read/Write"
        Image_Repository: "Deny/Read/Write"
        Network_Hierarchy: "Deny/Read/Write"
        Network_Profiles: "Deny/Read/Write"
        Network_Settings: "Deny/Read/Write"
        Virtual_Network: "Deny/Read/Write"
    - Network_Provision:
        # Managing compliance, inventory, and provisioning operations.
        Compliance: "Deny/Read/Write"
        Image_Update: "Deny/Read/Write"
        Inventory_Management:
          Device_Configuration: "Deny/Read/Write"
          Discovery: "Deny/Read/Write"
          Network_Device: "Deny/Read/Write"
          Port_Management: "Deny/Read/Write"
          Topology: "Deny/Read/Write"
        License: "Deny/Read/Write"
        Network_Telemetry: "Deny/Read/Write"
        PnP: "Deny/Read/Write"
        Provision: "Deny/Read/Write"
    - Network_Services:
        # Controlling services related to application hosting and security.
        App_Hosting: "Deny/Read/Write"
        Bonjour: "Deny/Read/Write"
        Stealthwatch: "Deny/Read/Write"
        Umbrella: "Deny/Read/Write"
    - Platform:
        # Managing API access, bundles, and reporting.
        APIs: "Deny/Read/Write"
        Bundles: "Deny/Read/Write"
        Events: "Deny/Read/Write"
        Reports: "Deny/Read/Write"
    - Security:
        # Enforcing policies and access controls.
        Group_Based_Policy: "Deny/Read/Write"
        IP_Based_Access_Control: "Deny/Read/Write"
        Security_Advisories: "Deny/Read/Write"
    - System:
        # Governing machine reasoning and system management.
        Machine_Reasoning: "Deny/Read/Write"
        System_Management: "Deny/Read/Write"
    - Utilities:
        # Managing utility functions like auditing, event viewing, and scheduling.
        Audit_Log: "Deny/Read/Write"
        Event_Viewer: "Deny/Read/Write"
        Network_Reasoner: "Deny/Read/Write"
        Scheduler: "Deny/Read/Write"
        Search: "Deny/Read/Write"
  
      Example: Creating a Custom Role Configuration with mixed Permission under different main parameters:
    Description: This configuration creates a custom role with specific permissions tailored for various modules in the Cisco Catalyst Center. 
                 It allows Write permissions for Advanced Network Settings, Image Repository, Network Hierarchy, and Network Profiles under Network Design. 
                 It also provides Read permissions for Device Configuration and Network Device under Inventory Management within Network Provision, 
                 while denying access (Deny) to all other parameters across different modules.
    config:
    create_new_custom_role:
    - Assurance:
        Monitoring_and_Troubleshooting: "Deny"
        Monitoring_Settings: "Deny"
        Troubleshooting_Tools: "Deny"
    - Network_Analytics:
        Data_Access: "Deny"
    - Network_Design:
        Advanced_Network_Settings: "Write"
        Image_Repository: "Write"
        Network_Hierarchy: "Write"
        Network_Profiles: "Write"
        Network_Settings: "Write"
        Virtual_Network: "Deny"
    - Network_Provision:
        Compliance: "Deny"
        Image_Update: "Deny"
        Inventory_Management:
            Device_Configuration: "Read"
            Discovery: "Deny"
            Network_Device: "Read"
            Port_Management: "Deny"
            Topology: "Deny"
        License: "Deny"
        Network_Telemetry: "Deny"
        PnP: "Deny"
        Provision: "Deny"
    - Network_Services:
        App_Hosting: "Deny"
        Bonjour: "Deny"
        Stealthwatch: "Deny"
        Umbrella: "Deny"
    - Platform:
        APIs: "Deny"
        Bundles: "Deny"
        Events: "Deny"
        Reports: "Deny"
    - Security:
        Group_Based_Policy: "Deny"
        IP_Based_Access_Control: "Deny"
        Security_Advisories: "Deny"
    - System:
        Machine_Reasoning: "Deny"
        System_Management: "Deny"
    - Utilities:
        Audit_Log: "Deny"
        Event_Viewer: "Deny"
        Network_Reasoner: "Deny"
        Scheduler: "Deny"
        Search: "Deny"
    
    Explanation: This playbook configuration defines a custom role with specific access permissions for different modules in Cisco Catalyst Center. It ensures that the custom 
                 role has write permissions (Write) for Advanced Network Settings, Image Repository, Network Hierarchy, and Network Profiles under Network Design. It also grants 
                 read permissions (Read) for Device Configuration and Network Device under Inventory Management within Network Provision. All other parameters across Assurance, 
                 Network Analytics, Network Services, Platform, Security, System, and Utilities are denied access (Deny), aligning with security policies and specific role 
                 requirements in your environment. Adjust the permissions as needed based on your organization's security and operational needs.

  For Role Create or Update for each main-param:
  # Top-level configuration for custom role permissions.
  description: User must select any one of the options "Deny or Read or Write" for each parameter.
  type: str
  create_new_custom_role:
    Assurance: "Deny/Read/Write"  # Permissions for Assurance module.
    Network_Analytics: "Deny/Read/Write"  # Permissions for Network Analytics module.
    Network_Design: "Deny/Read/Write"  # Permissions for Network Design module.
    Network_Provision: "Deny/Read/Write"  # Permissions for Network Provision module.
    Network_Services: "Deny/Read/Write"  # Permissions for Network Services module.
    Platform: "Deny/Read/Write"  # Permissions for Platform module.
    Security: "Deny/Read/Write"  # Permissions for Security module.
    System: "Deny/Read/Write"  # Permissions for System module.
    Utilities: "Deny/Read/Write"  # Permissions for Utilities module.

    Example 1: Creating a Custom Role for Network Design
    Description: If you want to grant, write permissions for a custom role, you need to specify "Write" for Network Design and "Deny" for all other parameters.
                 The example below grants write permission only for Network Design.
    config:
    create_new_custom_role:
      - Assurance: “Deny” 
        Network_Analytics: "Deny "
        Network_Design: "Write "
        Network_Provision: "Deny "
        Network_Services: "Deny "
        Platform: "Deny "
        Security: "Deny "
        System: "Deny "
        Utilities: "Deny "
    The above configuration ensures that the custom role has write permissions exclusively for Network Design, while denying write permissions for all other parameters.

    Example 2: Creating a Custom Role with Mixed Permissions
    Description: This example demonstrates how to configure a custom role with specific permissions for various parameters. It grants write permission for Network Design, 
                 read permission for Network Analytics, and denies access for all other parameters.
    config:
    create_new_custom_role:
    - Assurance: "Deny"
      Network_Analytics: "Read"
      Network_Design: "Write"
      Network_Provision: "Deny"
      Network_Services: "Deny"
      Platform: "Deny"
      Security: "Deny"
      System: "Deny"
      Utilities: "Deny"
    In the above configuration:
    Network_Analytics: Read access (Read)
    Network_Design: Write access (Write)
    Assurance,Network_Provision, Network_Services, Platform, Security, System, Utilities: All denied access (Deny)
    Adjust the permissions (Write, Read, or Deny) as per your specific role requirements for each parameter

    delete_role:
    rolename:
      description: The rolename in the Cisco Catalyst Center to be deleted.
      type: str
      required: true
    
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

  - name: Cisco Catalyst Center documentation for User and Roles AddUserAPI
    description: Complete reference of the GetRolesAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!get-roles-api
  
  - name: Cisco Catalyst Center documentation for User and Roles AddUserAPI
    description: Complete reference of the AddRoleAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!add-role-api
  
  - name: Cisco Catalyst Center documentation for User and Roles UpdateUserAPI
    description: Complete reference of the UpdateRoleAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!update-role-api
  
  - name: Cisco Catalyst Center documentation for User and Roles DeleteUserAPI
    description: Complete reference of the DeleteRoleAPI API.
    link: https://developer.cisco.com/docs/dna-center/#!delete-role-api

notes:
  - SDK Methods used:
    - user_and_roles.UserandRoles.get_user_ap_i
    - user_and_roles.UserandRoles.add_user_ap_i
    - user_and_roles.UserandRoles.update_user_ap_i
    - user_and_roles.UserandRoles.delete_user_ap_i
    - user_and_roles.UserandRoles.get_roles_ap_i
    - user_and_roles.UserandRoles.add_roles_ap_i
    - user_and_roles.UserandRoles.update_roles_ap_i
    - user_and_roles.UserandRoles.delete_roles_ap_i
  
  - Paths used:
    - get /dna/system/api/v1/user
    - post /dna/system/api/v1/user
    - put /dna/system/api/v1/user
    - delete /dna/system/api/v1/user/{userId}
    - get /dna/system/api/v1/roles
    - post /dna/system/api/v1/roles
    - put /dna/system/api/v1/roles
    - delete /dna/system/api/v1/role/{roleId}
"""

EXAMPLES = r"""
---
  - name: Create User
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

  - name: Update User
    cisco.dnac.user_workflow_manager:
      dnac_host: "{{ dnac_host }}"
      dnac_username: "{{ dnac_username }}"
      dnac_password: "{{ dnac_password }}"
      dnac_verify: "{{ dnac_verify }}"
      dnac_port: "{{ dnac_port }}"
      dnac_version: "{{ dnac_version }}"
      dnac_debug: "{{ dnac_debug }}"
      state: present
      config:
        email: "ajithandrew@example.com"
        first_name: "Ajith"
        last_name: "Andrew"
        role_list:
          - "System Administrator"
        username: "ajith"

  - name: Delete User
    cisco.dnac.user_workflow_manager:
      dnac_host: "{{ dnac_host }}"
      dnac_username: "{{ dnac_username }}"
      dnac_password: "{{ dnac_password }}"
      dnac_verify: "{{ dnac_verify }}"
      dnac_port: "{{ dnac_port }}"
      dnac_version: "{{ dnac_version }}"
      dnac_debug: "{{ dnac_debug }}"
      state: absent
      config:
        username: "joel"

    - name: Add or update role to custom select each parameter:
      config:
        create_new_custom_role:
            - Assurance:
              - Monitoring_and_Troubleshooting: "Deny/Read/Write"
                Monitoring_Settings: "Deny/Read/Write"
                Troubleshooting_Tools: "Deny/Read/Write"
            - Network_Analytics:
              - Data_Access: "Deny/Read/Write"
            - Network_Design:
              - Advanced_Network_Settings: "Deny/Read/Write"
                Image_Repository: "Deny/Read/Write"
                Network_Hierarchy: "Deny/Read/Write"
                Network_Profiles: "Deny/Read/Write"
                Network_Settings: "Deny/Read/Write"
                Virtual_Network: "Deny/Read/Write"
            - Network_Provision:
              - Compliance: "Deny/Read/Write"
                Image_Update: "Deny/Read/Write"
                Inventory_Management:
                  - Device_Configuration: "Deny/Read/Write"
                    Discovery: "Deny/Read/Write"
                    Network_Device: "Deny/Read/Write"
                    Port_Management: "Deny/Read/Write"
                    Topology: "Deny/Read/Write"
                License: "Deny/Read/Write"
                Network_Telemetry: "Deny/Read/Write"
                PnP: "Deny/Read/Write"
                Provision: "Deny/Read/Write"
            - Network_Services:
              - App_Hosting: "Deny/Read/Write"
                Bonjour: "Deny/Read/Write"
                Stealthwatch: "Deny/Read/Write"
                Umbrella: "Deny/Read/Write"
            - Platform:
              - APIs: "Deny/Read/Write"
                Bundles: "Deny/Read/Write"
                Events: "Deny/Read/Write"
                Reports: "Deny/Read/Write"
            - Security:
              - Group_Based_Policy: "Deny/Read/Write"
                IP_Based_Access_Control: "Deny/Read/Write"
                Security_Advisories: "Deny/Read/Write"
            - System:
              - Machine_Reasoning: "Deny/Read/Write"
                System_Management: "Deny/Read/Write"
            - Utilities:
              - Audit_Log: "Deny/Read/Write"
                Event_Viewer: "Deny/Read/Write"
                Network_Reasoner: "Deny/Read/Write"
                Scheduler: "Deny/Read/Write"
                Search: "Deny/Read/Write"

    - name: Add or update role to custom select for whole parameter:
    config:
        create_new_custom_role:
          - Assurance: "Deny/Read/Write"
            Network_Analytics: "Deny/Read/Write"
            Network_Design: "Deny/Read/Write"
            Network_Provision: "Deny/Read/Write"
            Network_Services: "Deny/Read/Write"
            Platform: "Deny/Read/Write"
            Security: "Deny/Read/Write"
            System: "Deny/Read/Write"
            Utilities: "Deny/Read/Write"

    - name: Role delete:
      hosts: localhost
      gather_facts: no
      tasks:
        - name: Delete User
          cisco.dnac.user_workflow_manager:
            dnac_host: "{{ dnac_host }}"
            dnac_username: "{{ dnac_username }}"
            dnac_password: "{{ dnac_password }}"
            dnac_verify: "{{ dnac_verify }}"
            dnac_port: "{{ dnac_port }}"
            dnac_version: "{{ dnac_version }}"
            dnac_debug: "{{ dnac_debug }}"
            state: absent
            config:
                role name: "Example_role"
"""

RETURN = r"""
# Case 1: User operation successful (create/update/delete)
response_1:
  description: A dictionary with details of the API execution from Cisco Catalyst Center.
  returned: always
  type: dict
  sample:
    {
      "response": {
        "bapiExecutionId": "string",
        "bapiKey": "string",
        "bapiName": "string",
        "endTime": "string",
        "endTimeEpoch": 0,
        "runtimeInstanceId": "string",
        "userId": "string",  # User ID from Cisco Catalyst Center
        "startTime": "string",
        "startTimeEpoch": 0,
        "status": "string",  # Status of the operation
        "timeDuration": 0
      },
      "msg": "User operation successful."
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
        "bapiError": "string",  # Specific error message
        "bapiExecutionId": "string",
        "bapiKey": "string",
        "bapiName": "string",
        "endTime": "string",
        "endTimeEpoch": 0,
        "runtimeInstanceId": "string",
        "startTime": "string",
        "startTimeEpoch": 0,
        "status": "string",
        "timeDuration": 0
      },
      "msg": "Error during creating or updating or deleting the user."
    }

# Case 4: User not found (during delete operation)
response_4:
  description: A dictionary indicating user not found during delete operation.
  returned: always
  type: dict
  sample:
    {
      "response": [],
      "msg": "User not found."
    }

# Case 5: Role not found (during get operation)
response_5:
  description: A dictionary indicating role not found during get operation.
  returned: always
  type: dict
  sample:
    {
      "response": [],
      "msg": "Role not found."
    }

# Case 6: Get all role
Responce_6:
  dnac_response:
    description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
    returned: always
    type: dict
    sample:
      {
        "roles": [
          {
            "resourceTypes": [
              {
                "operations": [
                  "string"
                ],
                "type": "string"
              }
            ],
            "meta": {
              "createdBy": "string",
              "created": "string",
              "lastModified": "string"
            },
            "roleId": "string",
            "name": "string",
            "description": "string",
            "type": "string"
          }
        ]
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
        user_details = dict(first_name = dict(required=False, type='str'),
                    last_name = dict(required=False, type='str'),
                    email = dict(required=False, type='str'),
                    password = dict(required=False, type='str'),
                    username = dict(required=False, type='str'),
                    role_list = dict(required=False, type='list', elements='str'),
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


    def valid_create_user_config_parameters(self, user_config):
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


    def valid_update_user_config_parameters(self, user_config):
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


    def valid_delete_user_config_parameters(self, user_config):
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

        if user_config.get("username"):
            param_spec = dict(type = "str", length_max = 255)
            validate_str(user_config["username"], param_spec, "username",
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

        # config_updated = False
        config_created = False
        task_response = None
        # check if the given user config exists and/or needs to be updated/created.

        if self.have.get("user_exists"):
            #update the user
            self.valid_update_user_config_parameters(config).check_return_status()
            consolidated_data = self.compare_user_cofig_with_inputdata(self.have["current_user_config"])
            if consolidated_data:
                self.log('Final user data to update {}'.format(str(consolidated_data)),
                      "INFO")
                task_response = self.update_user(consolidated_data)
                self.log('Task respoonse {}'.format(str(task_response)),"INFO")
                config_updated = True
            else:
                # user does not need update
                self.msg = "user - {0} does not need any update"\
                    .format(self.have.get("current_user_config").get("username"))
                self.log(self.msg, "INFO")
                responses = {}
                responses["users_updates"] = {"response": config}
                self.result['msg'] = self.msg
                self.result["response"].append(responses)
                self.result["skipped"] = True
                return self
        else:
            # Create the user
            self.valid_create_user_config_parameters(config).check_return_status()
            self.log('Creating user with config {}'.format(str(config)), "INFO")
            user_params = self.want

            try:
                # Additional filtering can be added here if necessary
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

        # if config_updated or config_created:
        if config_created:
            responses = {}
            responses["users_updates"] = {"response": task_response}
            
            # if config_updated:
            #     self.msg = "User details - {0} Updated Successfully"\
            #         .format(self.have["current_user_config"].get("username"))
            #     self.log(self.msg, "INFO")
            #     self.result['msg'] = self.msg
            #     self.result['response'].append(responses)

            self.msg = "User created successfully"
            self.log(self.msg, "INFO")
            self.result['msg'] = self.msg
            self.result['response'].append(responses)
        return self


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


    def get_current_config(self, input_config):
        """
        Check if the input user details exist in Cisco Catalyst Center.

        Parameters:
          - self (object): An instance of the class containing the method.

        Returns:
            A Dictionary list containing user details based on the input given from
            playbook like username
            [
                {
                    "first_name": "Ajith",
                    "last_name": "Andrew",
                    "email": "ajith.andrew@example.com",
                    "password": "Ajith@123",
                    "username": "ajithandrewj",
                    "role_list": ["SUPER-ADMIN-ROLE"]
                }
            ]

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
            self.keymap = self.keymaping(self.keymap, response_user)
            self.keymap = self.keymaping(self.keymap, response_role)
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
                    break
            if roles:
              for role in roles:
                  if role.get("name") in input_config.get("role_list"):
                      current_role_configuration[role.get("name")] = role.get("role_id")
                      role_exists = True

        return (user_exists, role_exists, current_user_configuration, current_role_configuration)


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
            self.valid_delete_user_config_parameters(config).check_return_status()
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
                responses["users_updates"] = {"response": task_response}
                self.msg = "User deleted successfully"
                self.log(self.msg, "INFO")
                self.result['msg'] = self.msg
                self.result['response'].append(responses)

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


    def keymaping(self, keymap = any, data = any):
        """
        This function used to create the key value by snake case and Camal Case
        we need to pass the input as the user details this function collects
        all key which is in Camal case and convert the key to Snake Case 
        Snake case will be key and value will be as Camal Case return as Dict
        Parameters:
          - keymap: type Dict : Already any Key map dict was available add here or empty dict.{}
          - data: Type :Dict : Which key need do the key map use the data {}
            eg: user details response as a input
        Returns:
            {
                {
                    "first_name": "firstName",
                    "last_name": "lastName"
                }
            }
        Example:
            functions = User(module)
            keymap = functions.keymaping(keymap,user_config)
        """
        if isinstance(data, dict):
            keymap.update(keymap)
            for key, value in data.items():
                new_key = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', key).lower()
                keymap[new_key] = key
                if isinstance(value, dict):
                    self.keymaping(keymap, value)
                elif isinstance(value, list):
                    self.keymaping(keymap, (item for item in value if isinstance(item, dict)))
            return keymap
        elif isinstance(data, list):
            self.keymaping(keymap, (item for item in data if isinstance(item, dict)))
        else:
            return keymap


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
        
        # if config_verify:
        #     time.sleep(5)
        #     ccc_user.verify_diff_state_apply[state](config).check_return_status()

    module.exit_json(**ccc_user.result)

if __name__ == '__main__':
    main()
