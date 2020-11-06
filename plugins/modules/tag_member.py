#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, first last <email>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '0.0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: tag_member
short_description: Manage TagMember objects of Tag
description:
- Returns tag members specified by id.
- Adds members to the tag specified by id.
- Removes Tag member from the tag specified by id.
- Returns the number of members in a given tag.
- Updates tag membership. As part of the request payload through this API, only the specified members are added / retained to the given input tags. Possible values of memberType attribute in the request payload can be queried by using the /tag/member/type API.
- Returns list of supported resource types.
version_added: '1.0'
author: first last (@GitHubID)
options:
    id:
        description:
        - Tag ID.
        type: str
        required: True
    level:
        description:
        - Level query parameter.
        type: str
    limit:
        description:
        - Used to Number of maximum members to return in the result.
        type: str
    member_association_type:
        description:
        - Indicates how the member is associated with the tag. Possible values and description. 1) DYNAMIC : The member is associated to the tag through rules. 2) STATIC – The member is associated to the tag manually. 3) MIXED – The member is associated manually and also satisfies the rule defined for the tag.
        type: str
    member_type:
        description:
        - Entity type of the member. Possible values can be retrieved by using /tag/member/type API.
        type: str
    offset:
        description:
        - Used for pagination. It indicates the starting row number out of available member records.
        type: str
    member_id:
        description:
        - TagMember id to be removed from tag.
        type: str
        required: True
    count:
        description:
        - If true gets the number of objects.
        type: bool
        required: True
    memberToTags:
        description:
        - TagMemberDTO's memberToTags.
        type: dict
        suboptions:
            key:
                description:
                - It is the tag member's key.
                type: list

    memberType:
        description:
        - TagMemberDTO's memberType.
        type: str

requirements:
- dnacentersdk
seealso:
# Reference by module name
- module: cisco.dnac.plugins.module_utils.definitions.tag_member
# Reference by Internet resource
- name: TagMember reference
  description: Complete reference of the TagMember object model.
  link: https://developer.cisco.com/docs/dna-center/api/1-3-3-x
# Reference by Internet resource
- name: TagMember reference
  description: SDK reference.
  link: https://dnacentersdk.readthedocs.io/en/latest/api/api.html#v2-1-1-summary
'''

EXAMPLES = r'''
'''

RETURN = r'''
data_0:
    description: Returns tag members specified by id.
    returned: success,changed,always
    type: dict
    contains:
        version:
            description: Version, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        response:
            description: Response, property of the response body (list of objects).
            returned: success,changed,always
            type: list
            contains:
                instanceUuid:
                    description: It is the tag member's instanceUuid.
                    returned: success,changed,always
                    type: str
                    sample: 'sample_string'


data_1:
    description: Adds members to the tag specified by id.
    returned: success,changed,always
    type: dict
    contains:
        version:
            description: List[entry«string,list«string»»]'s version.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        response:
            description: List[entry«string,list«string»»]'s response.
            returned: success,changed,always
            type: dict
            contains:
                taskId:
                    description: It is the tag member's taskId.
                    returned: success,changed,always
                    type: dict
                url:
                    description: It is the tag member's url.
                    returned: success,changed,always
                    type: str
                    sample: 'sample_string'


data_2:
    description: Removes Tag member from the tag specified by id.
    returned: success,changed,always
    type: dict
    contains:
        version:
            description: Version, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        response:
            description: Response, property of the response body.
            returned: success,changed,always
            type: dict
            contains:
                taskId:
                    description: It is the tag member's taskId.
                    returned: success,changed,always
                    type: dict
                url:
                    description: It is the tag member's url.
                    returned: success,changed,always
                    type: str
                    sample: 'sample_string'


data_3:
    description: Returns the number of members in a given tag.
    returned: success,changed,always
    type: dict
    contains:
        version:
            description: Version, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        response:
            description: Response, property of the response body.
            returned: success,changed,always
            type: int
            sample: 0

data_4:
    description: Updates tag membership. As part of the request payload through this API, only the specified members are added / retained to the given input tags. Possible values of memberType attribute in the request payload can be queried by using the /tag/member/type API.
    returned: success,changed,always
    type: dict
    contains:
        version:
            description: TagMemberDTO's version.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        response:
            description: TagMemberDTO's response.
            returned: success,changed,always
            type: dict
            contains:
                taskId:
                    description: It is the tag member's taskId.
                    returned: success,changed,always
                    type: dict
                url:
                    description: It is the tag member's url.
                    returned: success,changed,always
                    type: str
                    sample: 'sample_string'


data_5:
    description: Returns list of supported resource types.
    returned: success,changed,always
    type: dict
    contains:
        version:
            description: Version, property of the response body.
            returned: success,changed,always
            type: str
            sample: 'sample_string'
        response:
            description: Response, property of the response body (list of strings).
            returned: success,changed,always
            type: list

'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.dnac.plugins.module_utils.dnac import ModuleDefinition, DNACModule, dnac_argument_spec
from ansible_collections.cisco.dnac.plugins.module_utils.definitions.tag_member import module_definition


def main():

    moddef = ModuleDefinition(module_definition)

    argument_spec = dnac_argument_spec()
    argument_spec.update(moddef.get_argument_spec_dict())

    required_if = moddef.get_required_if_list()
    
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=False,
        required_if=required_if
    )

    dnac = DNACModule(module, moddef)

    state = module.params.get("state")

    if state == "query":
        dnac.exec("get")

    elif state == "delete":
        dnac.exec("delete")

    elif state == "create":
        dnac.disable_validation()
        dnac.exec("post")

    elif state == "update":
        dnac.disable_validation()
        dnac.exec("put")

    dnac.exit_json()


if __name__ == "__main__":
    main()