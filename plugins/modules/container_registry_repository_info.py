#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) jasites <jsites@vultr.com>
# Copyright: Contributors to the Ansible project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: container_registry_repository_info
short_description: Get information about a Vultr container registry's repositories
version_added: "1.15.0"
description:
  - Gather information about a container registry's repositories
author:
  - "jasites (@jasites)"
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Get Vultr container registry information
  vultr.cloud.container_registry_repository_info:
  register: result

- name: Print the infos
  ansible.builtin.debug:
    var: result.vultr_container_registry_repository_info
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
  contains:
    api_timeout:
      description: Timeout used for the API requests.
      returned: success
      type: int
      sample: 60
    api_retries:
      description: Amount of max retries for the API requests.
      returned: success
      type: int
      sample: 5
    api_retry_max_delay:
      description: Exponential backoff delay in seconds between retries up to this max delay value.
      returned: success
      type: int
      sample: 12
    api_results_per_page:
      description: Number of results returned per call to API.
      returned: success
      type: int
      sample: 100
    api_endpoint:
      description: Endpoint used for the API requests.
      returned: success
      type: str
      sample: "https://api.vultr.com/v2"
vultr_container_registry_repository_info:
  description: Response from Vultr API as list.
  returned: success
  type: list
  contains:
    name:
      description: Name of this container registry repository, with registry prepended
      returned: success
      type: str
      sample: my-registry/my-container-image-name
    image:
      description: Name of the container image stored within this repository
      returned: success
      type: str
      sample: my-container-image-name
    description:
      description: User defined description of the container image stored in this repository
      returned: success
      type: str
      sample: My container registry repository description
    added_at:
      description: Date this repository was created
      returned: success
      type: str
      sample: 2023-09-14 09:09:16
    updated_at:
      description: Date this repository was last updated
      returned: success
      type: str
      sample: 2023-09-14 09:09:16
    pull_count:
      description: Number of artifact downloads for this repository
      returned: success
      type: int
    artifact_count:
      description: Number of artifacts contained in this repository
      returned: success
      type: int
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


class AnsibleVultrContainerRegistryRepositoryInfo(AnsibleVultr):
    def get_container_registry(self):
        return self.query_filter_list_by_name(
            key_name="name",
            param_key="registry",
            path="/registries",
            result_key="registries",
            fail_not_found=True,
        )
    
    def configure(self):
        # Set registry id to resource path to ensure registry exists
        self.resource_path = self.resource_path % self.get_container_registry()["id"]


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            registry=dict(type="str", required=True),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vultr = AnsibleVultrContainerRegistryRepositoryInfo(
        module=module,
        namespace="vultr_container_registry_repository_info",
        resource_path="/registry/%s/repositories",
        ressource_result_key_singular="repository",
        ressource_result_key_plural="repositories",
    )

    vultr.get_result(vultr.query_list())


if __name__ == "__main__":
    main()
