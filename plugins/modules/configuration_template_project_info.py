#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: configuration_template_project_info
short_description: Information module for Configuration Template Project
description:
- Get all Configuration Template Project.
- Get Configuration Template Project by id.
- Get the details of the given project by its id.
- List the projects.
version_added: '3.1.0'
extends_documentation_fragment:
  - cisco.dnac.module_info
author: Rafael Campos (@racampos)
options:
  headers:
    description: Additional headers.
    type: dict
  name:
    description:
    - Name query parameter. Name of project to be searched.
    type: str
  sortOrder:
    description:
    - SortOrder query parameter. Sort Order Ascending (asc) or Descending (des).
    type: str
  projectId:
    description:
    - ProjectId path parameter. ProjectId(UUID) of project to get project details.
    type: str
requirements:
- dnacentersdk == 2.4.5
- python >= 3.5
notes:
  - SDK Method used are
    configuration_templates.ConfigurationTemplates.get_project_details,
    configuration_templates.ConfigurationTemplates.get_projects,

  - Paths used are
    get /dna/intent/api/v1/template-programmer/project,
    get /dna/intent/api/v1/template-programmer/project/{projectId},

"""

EXAMPLES = r"""
- name: Get all Configuration Template Project
  cisco.dnac.configuration_template_project_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers:
      custom: value
    name: string
    sortOrder: string
  register: result

- name: Get Configuration Template Project by id
  cisco.dnac.configuration_template_project_info:
    dnac_host: "{{dnac_host}}"
    dnac_username: "{{dnac_username}}"
    dnac_password: "{{dnac_password}}"
    dnac_verify: "{{dnac_verify}}"
    dnac_port: "{{dnac_port}}"
    dnac_version: "{{dnac_version}}"
    dnac_debug: "{{dnac_debug}}"
    headers:
      custom: value
    projectId: string
  register: result

"""

RETURN = r"""
dnac_response:
  description: A dictionary or list with the response returned by the Cisco DNAC Python SDK
  returned: always
  type: dict
  sample: >
    {
      "tags": [
        {
          "id": "string",
          "name": "string"
        }
      ],
      "createTime": 0,
      "description": "string",
      "id": "string",
      "lastUpdateTime": 0,
      "name": "string",
      "templates": [
        {
          "tags": [
            {
              "id": "string",
              "name": "string"
            }
          ],
          "author": "string",
          "composite": true,
          "containingTemplates": [
            {
              "tags": [
                {
                  "id": "string",
                  "name": "string"
                }
              ],
              "composite": true,
              "description": "string",
              "deviceTypes": [
                {
                  "productFamily": "string",
                  "productSeries": "string",
                  "productType": "string"
                }
              ],
              "id": "string",
              "language": "string",
              "name": "string",
              "projectName": "string",
              "rollbackTemplateParams": [
                {
                  "binding": "string",
                  "customOrder": 0,
                  "dataType": "string",
                  "defaultValue": "string",
                  "description": "string",
                  "displayName": "string",
                  "group": "string",
                  "id": "string",
                  "instructionText": "string",
                  "key": "string",
                  "notParam": true,
                  "order": 0,
                  "paramArray": true,
                  "parameterName": "string",
                  "provider": "string",
                  "range": [
                    {
                      "id": "string",
                      "maxValue": 0,
                      "minValue": 0
                    }
                  ],
                  "required": true,
                  "selection": {
                    "defaultSelectedValues": [
                      "string"
                    ],
                    "id": "string",
                    "selectionType": "string",
                    "selectionValues": {}
                  }
                }
              ],
              "templateContent": "string",
              "templateParams": [
                {
                  "binding": "string",
                  "customOrder": 0,
                  "dataType": "string",
                  "defaultValue": "string",
                  "description": "string",
                  "displayName": "string",
                  "group": "string",
                  "id": "string",
                  "instructionText": "string",
                  "key": "string",
                  "notParam": true,
                  "order": 0,
                  "paramArray": true,
                  "parameterName": "string",
                  "provider": "string",
                  "range": [
                    {
                      "id": "string",
                      "maxValue": 0,
                      "minValue": 0
                    }
                  ],
                  "required": true,
                  "selection": {
                    "defaultSelectedValues": [
                      "string"
                    ],
                    "id": "string",
                    "selectionType": "string",
                    "selectionValues": {}
                  }
                }
              ],
              "version": "string"
            }
          ],
          "createTime": 0,
          "customParamsOrder": true,
          "description": "string",
          "deviceTypes": [
            {
              "productFamily": "string",
              "productSeries": "string",
              "productType": "string"
            }
          ],
          "documentDatabase": true,
          "failurePolicy": "string",
          "id": "string",
          "language": "string",
          "lastUpdateTime": 0,
          "latestVersionTime": 0,
          "name": "string",
          "parentTemplateId": "string",
          "projectAssociated": true,
          "projectId": "string",
          "projectName": "string",
          "rollbackTemplateContent": "string",
          "rollbackTemplateParams": [
            {
              "binding": "string",
              "customOrder": 0,
              "dataType": "string",
              "defaultValue": "string",
              "description": "string",
              "displayName": "string",
              "group": "string",
              "id": "string",
              "instructionText": "string",
              "key": "string",
              "notParam": true,
              "order": 0,
              "paramArray": true,
              "parameterName": "string",
              "provider": "string",
              "range": [
                {
                  "id": "string",
                  "maxValue": 0,
                  "minValue": 0
                }
              ],
              "required": true,
              "selection": {
                "defaultSelectedValues": [
                  "string"
                ],
                "id": "string",
                "selectionType": "string",
                "selectionValues": {}
              }
            }
          ],
          "softwareType": "string",
          "softwareVariant": "string",
          "softwareVersion": "string",
          "templateContent": "string",
          "templateParams": [
            {
              "binding": "string",
              "customOrder": 0,
              "dataType": "string",
              "defaultValue": "string",
              "description": "string",
              "displayName": "string",
              "group": "string",
              "id": "string",
              "instructionText": "string",
              "key": "string",
              "notParam": true,
              "order": 0,
              "paramArray": true,
              "parameterName": "string",
              "provider": "string",
              "range": [
                {
                  "id": "string",
                  "maxValue": 0,
                  "minValue": 0
                }
              ],
              "required": true,
              "selection": {
                "defaultSelectedValues": [
                  "string"
                ],
                "id": "string",
                "selectionType": "string",
                "selectionValues": {}
              }
            }
          ],
          "validationErrors": {
            "rollbackTemplateErrors": [
              {}
            ],
            "templateErrors": [
              {}
            ],
            "templateId": "string",
            "templateVersion": "string"
          },
          "version": "string"
        }
      ],
      "isDeletable": true
    }
"""