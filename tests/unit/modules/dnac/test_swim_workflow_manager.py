# Copyright (c) 2024 Cisco and/or its affiliates.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Make coding more python3-ish

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from unittest.mock import patch

from ansible_collections.cisco.dnac.plugins.modules import swim_workflow_manager
from .dnac_module import TestDnacModule, set_module_args, loadPlaybookData


class TestswimWorkflowManager(TestDnacModule):

    module = swim_workflow_manager

    test_data = loadPlaybookData("swim_workflow_manager")

    playbook_config_invalid_param_import_image_url_tag_golden_load = test_data.get("playbook_config_invalid_param_import_image_url_tag_golden_load")
    playbook_untag_image_as_golden_and_load_on_device = test_data.get("playbook_untag_image_as_golden_and_load_on_device")

    def setUp(self):
        super(TestswimWorkflowManager, self).setUp()

        self.mock_dnac_init = patch(
            "ansible_collections.cisco.dnac.plugins.module_utils.dnac.DNACSDK.__init__")
        self.run_dnac_init = self.mock_dnac_init.start()
        self.run_dnac_init.side_effect = [None]
        self.mock_dnac_exec = patch(
            "ansible_collections.cisco.dnac.plugins.module_utils.dnac.DNACSDK._exec"
        )
        self.run_dnac_exec = self.mock_dnac_exec.start()

    def tearDown(self):
        super(TestswimWorkflowManager, self).tearDown()
        self.mock_dnac_exec.stop()
        self.mock_dnac_init.stop()

    def load_fixtures(self, response=None, device=""):
        """
        Load fixtures for user.
        """
        if "playbook_config_invalid_param_import_image_url_tag_golden_load" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("get_software_image_details"),
                self.test_data.get("import_software_image_via_url"),
                self.test_data.get("task_details"),
                self.test_data.get("get_software_image_1_details"),
                self.test_data.get("get_software_image_1_details"),
                self.test_data.get("get_site"),
                self.test_data.get("get_device_family_identifiers"),
                self.test_data.get("get_software_image_1_details"),
                self.test_data.get("get_device_list"),
                self.test_data.get("get_software_image_1_details"),
                self.test_data.get("get_device_list"),
                self.test_data.get("get_software_image_1_details"),
                self.test_data.get("get_golden_tag_status_of_an_image"),
                self.test_data.get("tag_as_golden_image"),
                self.test_data.get("task_1_details"),
                self.test_data.get("get_1_site"),
                self.test_data.get("get_membership"),
                self.test_data.get("trigger_software_image_distribution"),
                self.test_data.get("task_2_details"),
                self.test_data.get("get_1_site"),
                self.test_data.get("get_1_membership"),
                self.test_data.get("trigger_software_image_activation"),
                self.test_data.get("task_3_details"),
                self.test_data.get("task_4_details"),
                self.test_data.get("playbook_config_invalid_param_import_image_url_tag_golden_load_response")
            ]
        elif "playbook_untag_image_as_golden_and_load_on_device" in self._testMethodName:
            self.run_dnac_exec.side_effect = [
                self.test_data.get("get_2_software_image_details"),
                self.test_data.get("get_2_site"),
                self.test_data.get("get_2_device_family_identifiers"),
                self.test_data.get("get_software_image_details_1"),
                self.test_data.get("get_2_golden_tag_status_of_an_image"),
                self.test_data.get("remove_golden_tag_for_image"),
                self.test_data.get("Task_details"),
                self.test_data.get("get_software_image_details_2"),
                self.test_data.get("get_site_1"),
                self.test_data.get("get_device_family_identifiers_1"),
                self.test_data.get("get_software_image_details_3"),
                self.test_data.get("get_golden_tag_status_of_an_image_1"),
                self.test_data.get("untag_image_as_golden_and_load_on_device_responce")
            ]

    def test_swim_workflow_manager_playbook_config_invalid_param_import_image_url_tag_golden_load(self):
        """
        Test case for swim workflow manager when giving invalid param.

        This test case checks the behavior of the swim workflow when giving invalid param in the specified Cisco Catalyst Center.
        """
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_config_invalid_param_import_image_url_tag_golden_load
            )
        )
        result = self.execute_module(changed=False, failed=True)
        print(result)
        self.assertEqual(
            result.get("msg"),
            "Activation for Image with Id '4a3cccfa-dc92-4fad-a7d3-c59876cbebe6' gets failed"
        )

    def test_swim_workflow_manager_playbook_untag_image_as_golden_and_load_on_device(self):
        """
        Test case for user role workflow manager when creating a user.

        This test case checks the behavior of the user workflow when creating a new user in the specified Cisco Catalyst Center.
        """
        set_module_args(
            dict(
                dnac_host="1.1.1.1",
                dnac_username="dummy",
                dnac_password="dummy",
                dnac_log=True,
                state="merged",
                config=self.playbook_untag_image_as_golden_and_load_on_device
            )
        )
        result = self.execute_module(changed=True, failed=False)
        print(result)
        self.assertEqual(
            result.get('msg'),
            "Untagging of image  cat9k_iosxe.17.12.02.SPA.bin for site  LTTS for family Cisco Catalyst 9000 UADP 8 Port Virtual Switch  for device deviceTag ALL successful."
        )
