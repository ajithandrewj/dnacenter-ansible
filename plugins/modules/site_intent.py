#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2022, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type
__author__ = (
            "Madhan Sankaranarayanan, Rishita Chowdhary"
            )
            
DOCUMENTATION = r"""
---
module: site_intent
short_description: Resource module for Site operations
description:
- Manage operation create, update and delete of the resource Sites.
- Creates site with area/building/floor with specified hierarchy.
- Updates site with area/building/floor with specified hierarchy.
- Deletes site with area/building/floor with specified hierarchy.
version_added: '6.4.0'
extends_documentation_fragment:
  - cisco.dnac.module
author: Madhan Sankaranarayanan (@madhansansel) 
        Rishita Chowdhary (@rishitachowdhary)
options:
  state:
    description: The state of DNAC after module completion.
    type: str
    choices:
      - merged
      - deleted
    default: merged
  config:
    description:
    - List of details of site being managed. 
    type: list
    elements: dict/str
    suboptions:
      type:
        description: Type of site to create/update/delete (eg area, building, floor).
        type: str
      site:
        description: Site Details.
        type: dict
        suboptions:
          area:
            description: Site Create's area.
            type: dict
            suboptions:
              name:
                description: Name of the area (eg Area1).
                type: str
              parentName:
                description: Parent name of the area to be created.
                type: str
          building:
            description: Building Details.
            type: dict
            suboptions:
              address:
                description: Address of the building to be created.
                type: str
              latitude:
                description: Latitude coordinate of the building (eg 37.338).
                type: int
              longitude:
                description: Longitude coordinate of the building (eg -121.832).
                type: int
              name:
                description: Name of the building (eg building1).
                type: str
              parentName:
                description: Parent name of building to be created.
                type: str
          floor:
            description: Site Create's floor.
            type: dict
            suboptions:
              height:
                description: Height of the floor (eg 15).
                type: int
              length:
                description: Length of the floor (eg 100).
                type: int
              name:
                description: Name of the floor (eg floor-1).
                type: str
              parentName:
                description: Parent name of the floor to be created.
                type: str
              rfModel:
                description: Type of floor. Allowed values are 'Cubes And Walled Offices',
                  'Drywall Office Only', 'Indoor High Ceiling', 'Outdoor Open Space'.
                type: str
              width:
                description: Width of the floor (eg 100).
                type: int
                
requirements:
- dnacentersdk == 2.4.5
- python >= 3.5
notes:
  - SDK Method used are
    sites.Sites.create_site,
    sites.Sites.update_site,
    sites.Sites.delete_site

  - Paths used are
    post /dna/intent/api/v1/site,
    put dna/intent/api/v1/site/{siteId},
    delete dna/intent/api/v1/site/{siteId}
"""

EXAMPLES = r"""
- name: Create
  cisco.dnac.site_intent:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    dnac_log: "{{dnac_log}}"
    config:
        site:
          area:
            name: string
            parentName: string
          building:
            address: string
            latitude: 0
            longitude: 0
            name: string
            parentName: string
          floor:
            height: 0
            length: 0
            name: string
            parentName: string
            rfModel: string
            width: 0
        type: string
"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "executionId": "string",
      "executionStatusUrl": "string",
      "message": "string"
    }
"""


import copy
try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
        AnsibleArgSpecValidator,
    )
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import (
    DNACSDK,
    dnac_argument_spec,
    validate_list_of_dicts,
    log,
    get_dict_result,
    dnac_compare_equality,
)
from ansible.module_utils.basic import AnsibleModule

floor_plan = { 
    '57057':'CUBES AND WALLED OFFICES',
    '57058':'DRYWELL OFFICE ONLY',
    '41541500':'FREE SPACE',
    '57060':'INDOOR HIGH CEILING',
    '57059':'OUTDOOR OPEN SPACE'
}


class DnacSite:

    def __init__(self, module):
        self.module = module
        self.params = module.params
        self.config = copy.deepcopy(module.params.get("config"))
        self.have = {} 
        self.want_create = {} 
        self.diff_create = []
        self.validated = []
        dnac_params = self.get_dnac_params(self.params)
        log(str(dnac_params))
        self.dnac = DNACSDK(params=dnac_params)
        self.log = dnac_params.get("dnac_log")

        self.result = dict(changed=False, diff=[], response=[], warnings=[])


    def get_state(self):
        return self.params.get("state")


    def validate_input(self):
        temp_spec = dict(
            type=dict(required=False, type='str'),
            site=dict(required=True, type='dict'),
            )

        if self.config:
            msg = None
            # Validate site params
            valid_temp, invalid_params = validate_list_of_dicts(
                self.config, temp_spec
            )

            if invalid_params:
                msg = "Invalid parameters in playbook: {0}".format(
                    "\n".join(invalid_params)
                )
                self.module.fail_json(msg=msg)

            self.validated = valid_temp

            if self.log:
                log(str(valid_temp))
                log(str(self.validated))


    def get_dnac_params(self, params):
        dnac_params = dict(
            dnac_host=params.get("dnac_host"),
            dnac_port=params.get("dnac_port"),
            dnac_username=params.get("dnac_username"),
            dnac_password=params.get("dnac_password"),
            dnac_verify=params.get("dnac_verify"),
            dnac_debug=params.get("dnac_debug"),
            dnac_log=params.get("dnac_log")
        )
        return dnac_params

    def get_current_site(self,site):
        site_info = {}

        location = get_dict_result(site[0].get("additionalInfo"),'nameSpace', "Location")
        type = location.get("attributes").get("type")
        
        if (type == "area"):
            site_info = dict(
                area=dict(
                    name = site[0].get("name"),
                    parentName = site[0].get("siteNameHierarchy").split("/"+site[0].get("name"))[0]
                )
            )

        elif (type == "building"):
            site_info = dict(
                building=dict(
                    name= site[0].get("name"),
                    parentName = site[0].get("siteNameHierarchy").split("/"+site[0].get("name"))[0],
                    address = location.get("attributes").get("address"),
                    latitude = location.get("attributes").get("latitude"),
                    longitude = location.get("attributes").get("longitude"),
                )
            )

        elif (type == "floor"):
            map_geometry = get_dict_result(site[0].get("additionalInfo"),'nameSpace', "mapGeometry")
            map_summary = get_dict_result(site[0].get("additionalInfo"),'nameSpace', "mapsSummary")
            rf_model = map_summary.get("attributes").get("rfModel")

            site_info = dict(
                floor=dict(
                    name= site[0].get("name"),
                    parentName = site[0].get("siteNameHierarchy").split("/"+site[0].get("name"))[0],
                    rfModel = floor_plan.get(rf_model),
                    width = map_geometry.get("attributes").get("width"),
                    length = map_geometry.get("attributes").get("length"),
                    height = map_geometry.get("attributes").get("height")
                )
            )

        current_site = dict(
            type=type,
            site=site_info,
            site_id=site[0].get("id")
        )

        if self.log:
            log(str(current_site))

        return current_site
        
        
    def site_exists(self):
        site_exists = False
        current_site = {}
        response = None
        try:
            response = self.dnac.exec(
                family="sites",
                function='get_site',
                params={"name":self.want.get("site_name")},
             )

        except:
            if self.log:
                log("The input site is not valid or site is not present.")
            pass

        if response:
            if self.log:
                log(str(response))

            response = response.get("response")
            current_site = self.get_current_site(response) 
            site_exists = True
    
        if self.log:
            log(str(self.validated))

        return (site_exists, current_site)


    def get_site_params(self, params):
        site=params.get("site")
        type=params.get("type")

        if type == "floor":
            site["floor"]["rfModel"] = site.get("floor").get("rfModel").upper()

        site_params = dict(
            type=type,
            site=site,
        )

        return site_params
  

    def get_site_name(self, site):
        site_type = site.get("type")
        parent_name = site.get("site").get(site_type).get("parentName")
        name = site.get("site").get(site_type).get("name")
        site_name = '/'.join([parent_name, name])

        if self.log:
            log(site_name)

        return site_name
        

    def site_requires_update(self):
        requested_site = self.want.get("site_params")
        current_site = self.have.get("current_site")

        if self.log:
            log("Current Site: " + str(current_site))
            log("Requested Site: " + str(requested_site))

        obj_params = [
            ("type", "type"),
            ("site", "site")
        ]

        return any(not dnac_compare_equality(current_site.get(dnac_param),
                                             requested_site.get(ansible_param))
                   for (dnac_param, ansible_param) in obj_params)



    def get_execution_details(self, id):
        response = None
        response = self.dnac.exec(
            family="task",
            function='get_business_api_execution_details',
            params={"execution_id":id}
        )

        if self.log:
            log(str(response))

        if response and isinstance(response, dict):
            return response
            
            
    def get_have(self):
        site_exists = False
        current_site = None
        have = {}

        #check if given site exits, if exists store current site info
        (site_exists, current_site) = self.site_exists()

        if self.log:
            log("Site Exists: " + str(site_exists) + "\n Current Site:" + str(current_site))

        if site_exists:
            have["site_id"] = current_site.get("site_id")
            have["site_exists"] = site_exists
            have["current_site"] = current_site

        self.have = have


    def get_want(self):
        want = {}

        for site in self.validated:
            want = dict(
                site_params = self.get_site_params(site), 
                site_name = self.get_site_name(site),
            )

        self.want = want


    def get_diff_merge(self):
        site_updated = False
        site_created = False

        #check if the given site exists and/or needs to be updated/created.
        if self.have.get("site_exists"):
            if self.site_requires_update():
                #Existing Site requires update
                site_params = self.want.get("site_params")
                site_params["site_id"] = self.have.get("site_id")
                response = self.dnac.exec(
                    family="sites",
                    function='update_site',
                    op_modifies=True,
                    params=site_params,
                )
                site_updated = True

            else:
                #Site does not neet update
                self.result['response'] = self.have.get("current_site") 
                self.module.exit_json(msg="Site does not need update")               
                
        else:
            #Creating New Site
            response = self.dnac.exec(
                family="sites",
                function='create_site',
                op_modifies=True,
                params=self.want.get("site_params"),
            )

            log(str(response))
            site_created = True
               
        if site_created or site_updated:
            if response and isinstance(response, dict):
                executionId = response.get("executionId")
                while (True):
                    execution_details = self.get_execution_details(executionId)
                    if (execution_details.get("status")=="SUCCESS"):
                        self.result['changed'] = True
                        self.result['response'] = execution_details
                        break

                    elif execution_details.get("bapiError"):
                        self.module.fail_json(msg=execution_details.get("bapiError"))
                        break
                
                if site_updated:
                    log("Site Updated Successfully")
                    self.result['msg'] = "Site Updated Successfully"

                else:
                    #Get the site id of the newly created site.
                    (site_exists, current_site) = self.site_exists()
                
                    if site_exists:
                        log("Site Created Successfully")
                        self.result['msg'] = "Site Created Successfully"
                        #self.result["site_id"] = current_site.get("site_id")
        

    def get_diff_delete(self):
        site_exists = self.have.get("site_exists")

        if site_exists:
            response = self.dnac.exec(
                family="sites",
                function="delete_site",
                params={"site_id": self.have.get("site_id")},
            )

            if response and isinstance(response, dict):
                executionId = response.get("executionId")
                while (True):
                    execution_details = self.get_execution_details(executionId)
                    if (execution_details.get("status")=="SUCCESS"):
                        self.result['changed'] = True
                        self.result['response'] = execution_details
                        break

                    elif execution_details.get("bapiError"):
                        self.module.fail_json(msg=execution_details.get("bapiError"))
                        break

        else:
            self.module.exit_json(msg="Site Not Found")


def main():
    """ main entry point for module execution
    """

    element_spec = dict(
        dnac_host=dict(required=True, type='str'),
        dnac_port=dict(required=False, type='str', default='443'),
        dnac_username=dict(required=True, type='str', no_log=True),
        dnac_password=dict(required=True, type='str', no_log=True),
        dnac_verify=dict(required=False, type='bool', default='False'),
        dnac_debug=dict(required=False, type='bool', default='False'),
        dnac_log=dict(required=False, type='bool', default='False'),
        config=dict(required=True, type='list', elements='dict'),
        state=dict(
            default='merged',
            choices=['merged', 'deleted']),
        )
    
    module = AnsibleModule(argument_spec=element_spec,
                           supports_check_mode=False)

    dnac_site = DnacSite(module)
    dnac_site.validate_input()
    state = dnac_site.get_state()

    dnac_site.get_want()
    dnac_site.get_have()

    if state == "merged":
        dnac_site.get_diff_merge()

    elif state == "deleted":
        dnac_site.get_diff_delete()

    module.exit_json(**dnac_site.result)

if __name__ == '__main__':
    main()
