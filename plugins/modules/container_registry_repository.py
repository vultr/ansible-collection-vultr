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
module: container_registry_repository
short_description: Read, update, and delete Vultr container registry repositories
version_added: "1.15.0"
description:
  - Read, update, and delete container registry repositories stored within Vultr
author:
  - "jasites (@jasites)"
options:
  registry:
  image:
  description:
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Update Vultr container registry repository description
  vultr.cloud.container_registry_repository:
    registry: myregistry
    image: my-container-image
    description: Repository for my container image

- name: Delete Vultr container registry repository (and all existing images)
  vultr.cloud.container_registry_repository:
    registry: myregistry
    image: my-container-image
    state: absent
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
vultr_container_registry:
  description: Response from Vultr API as dictionary.
  returned: success
  type: dict
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


class AnsibleVultrContainerRegistryRepository(AnsibleVultr):
    def get_container_registry(self):
        self.response_in_list = True
        result = self.query_filter_list_by_name(
            key_name="name",
            param_key="registry",
            path="/registries",
            result_key="registries",
            fail_not_found=True,
        )

        # reset property
        self.response_in_list = False
        return result

    def query_filter_list(self):
        self.response_in_list = True
        result = self.query_filter_list_by_name(
            path="/registry/%s/repositories" % self.get_container_registry()["id"],
            key_name=self.resource_key_name,
            result_key=self.ressource_result_key_plural,
            param_value="%s%s" % (
                self.module.params.get("registry"),
                "/" + self.module.params.get("image"),
            ),
            key_id=self.resource_key_id,
            get_details=self.resource_get_details,
            skip_transform=False,
        )

        self.response_in_list = False
        return result

    def configure(self):
        # Set registry id to resource path to ensure registry exists
        self.resource_path = self.resource_path % self.get_container_registry()["id"]


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            registry=dict(type="str", required=True),
            image=dict(type="str", required=True),
            description=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    vultr = AnsibleVultrContainerRegistryRepository(
        module=module,
        namespace="vultr_container_registry_repository",
        resource_key_id="image",
        resource_key_name="name",
        resource_path="/registry/%s/repository",
        resource_update_method="PUT",
        resource_update_param_keys=["description"],
        ressource_result_key_singular="repository",
        ressource_result_key_plural="repositories",
        response_in_list=False,
    )

    if module.params.get("state") == "absent":  # type: ignore
        vultr.absent()
    else:
        vultr.present()


if __name__ == "__main__":
    main()
