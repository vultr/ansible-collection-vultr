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
module: container_registry
short_description: Manages container registries on Vultr
version_added: "1.15.0"
description:
  - Manage container registries
author:
  - "jasites (@jasites)"
options:
  name:
    description:
      - Name of container registry
    required: true
    type: str
  public:
    description:
      - If true, container images can be pulled from repositories in this registry without authentication
      - Required for creation
      - Can be updated
    type: bool
  region:
    description:
      - Region in which to deploy the container registry
      - Required for creation
    type: str
  plan:
    description:
      - Name of the plan to use for the container registry
      - Required for creation
      - Can be updated
    type: str
  state:
    description:
      - State of the container registry
    default: present
    choices: [ present, absent ]
    type: str
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Ensure a container registry is present
  vultr.cloud.container_registry:
    name: myregistry
    plan: start_up
    public: true
    region: ewr

- name: Ensure a container registry is absent
  vultr.cloud.container_registry:
    name: myregistry
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
  description: Response from Vultr API.
  returned: success
  type: dict
  contains:
    id:
      description: UUID of the registry.
      returned: success
      type: str
      sample: 36f91844-b6d2-4e80-8fe0-bca5015d27cf
    name:
      description: Name of registry
      returned: success
      type: str
      sample: myregistry
    urn:
      description: URN (URL without connection scheme, i.e., 'https://') for this registry
      returned: success
      type: str
      sample: sjc.vultrcr.com/my-registry
    storage:
      description: Used and allowed storage metrics for this registry
      returned: success
      type: dict
      contains:
        used:
          description: Currently consumed storage capacity for this registry
          returned: success
          type: dict
          contains:
            updated_at:
              description: Date at which storage usage was last updated
              returned: success
              type: str
              sample: 2024-11-26 18:16:08
            bytes:
              description: Capacity consumed by this registry expressed in bytes
              returned: success
              type: float
              sample: 4194304
            mb:
              description: Capacity consumed by this registry expressed in megabytes
              returned: success
              type: float
              sample: 4
            gb:
              description: Capacity consumed by this registry expressed in gigabytes
              returned: success
              type: float
              sample: 0
            tb:
              description: Capacity consumed by this registry expressed in terabytes
              returned: success
              type: float
              sample: 0
        allowed:
          description: Capacity allowed to be consumed by the current plan selected for this registry
          returned: success
          type: dict
          contains:
            bytes:
              description: Capacity allowed to be consumed by this registry expressed in bytes
              returned: success
              type: float
              sample: 10737418240
            mb:
              description: Capacity allowed to be consumed by this registry expressed in megabytes
              returned: success
              type: float
              sample: 10240
            gb:
              description: Capacity allowed to be consumed by this registry expressed in gigabytes
              returned: success
              type: float
              sample: 10
            tb:
              description: Capacity allowed to be consumed by this registry expressed in terabytes
              returned: success
              type: float
              sample: 0.01
    date_created:
      description: Date on which this registry was created
      returned: success
      type: str
      sample: 2024-11-26 13:16:07
    public:
      description: True if this registry does not require authentication to pull from child repositories.
      returned: success
      type: bool
    root_user:
      description: Information concerning the root user of this registry
      returned: success
      type: dict
      contains:
        id:
          description: Numeric ID of this user.
          returned: success
          type: int
          sample: 48747
        username:
          description: Globally unique username for the root user
          returned: success
          type: str
          sample: d4518e8f-a495-40eb-86c7-95430522998d
        password:
          description: Password to be used by the root user to authenticate to this registry
          returned: success
          type: str
          sample: 00example1122334455667788990011
        root:
          description: True if this user cannot be deleted or renamed
          returned: success
          type: str
        added_at:
          description: Date on which this user was added to this registry
          returned: success
          type: str
          sample: 2024-11-26 13:16:07
        updated_at:
          description: Date on which this user was last updated
          returned: success
          type: str
          sample: 2024-11-26 13:16:07
    metadata:
      description: Information regarding the subscription associated with this registry
      returned: success
      type: dict
      contains:
        region:
          description: Information regarding the region in which this registry was deployed
          returned: success
          type: dict
          contains:
            id:
              description: ID of the region.
              returned: success
              type: int
              sample: 3
            name:
              description: Region name
              returned: success
              type: str
              sample: sjc
            urn:
              description: Base URN (URL without connection scheme, i.e., 'https://') for this region
              returned: success
              type: str
              sample: sjc.vultrcr.com
            base_url:
              description: Base URL for registries deployed to this region
              returned: success
              type: str
              sample: https://sjc.vultrcr.com
            public:
              description: True if this region is generally available for new registries to be created
              returned: success
              type: bool
            added_at:
              description: Date of when this region was added
              returned: success
              type: str
              sample: 2023-09-14 09:09:16
            updated_at:
              description: Date of when this region was last updated
              returned: success
              type: str
              sample: 2023-09-14 09:09:16
            data_center:
              description: Additional details regarding this region
              returned: success
              type: dict
              contains:
                id:
                  description: ID of this data center
                  returned: success
                  type: int
                  sample: 12
                name:
                  description: Name of data center
                  returned: success
                  type: str
                  sample: Silicon Valley
                site_code:
                  description: Code used to differentiate data centers within a region
                  returned: success
                  type: str
                  sample: SJC2
                region:
                  description: Geographical description of the placement of this data center within the region
                  returned: success
                  type: str
                  sample: West
                country:
                  description: Two letter country code (ISO 3166-1 alpha-2) of country containing this data center
                  returned: success
                  type: str
                  sample: US
                continent:
                  description: Continent containing this data center
                  returned: success
                  type: str
                  sample: North America
                description:
                  description: Additional descriptive data for this data center
                  returned: success
                  type: str
                  sample: Silicon Valley, California
                airport:
                  description: IATA airport code
                  returned: success
                  type: str
                  sample: SJC
        subscription:
          description: Information pertaining directly to the subscription itself
          returned: success
          type: dict
          contains:
            billing:
              description: Billing information for this subscription
              returned: success
              type: dict
              contains:
                monthly_price:
                  description: Monthly price of this subscription
                  returned: success
                  type: float
                pending_charges:
                  description: Pending charges for this subscription
                  returned: success
                  type: float
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.dict_transformations import dict_merge

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


class AnsibleVultrContainerRegistry(AnsibleVultr):
    def transform_resource(self, resource):
        resource["region"] = resource["metadata"]["region"]["name"]
        resource["plan"] = self.get_plan_id_by_max_storage_mb(
            resource["storage"]["allowed"]["mb"],
            self.get_plan_list(),
        )

        return resource

    def query_list(self, path=None, result_key=None, query_params=None):
        self.response_in_list = True
        result = super(AnsibleVultrContainerRegistry, self).query_list(
            path="/registries",
            result_key=result_key,
            query_params=query_params,
        )

        # reset property
        self.response_in_list = False
        return result

    def update(self, resource):
        plans = self.get_plan_list()
        current_plan = resource["plan"]
        desired_plan = self.module.params["plan"]
        if desired_plan != current_plan:
            current_limit = self.get_plan_max_storage_mb_by_id(plan_id=current_plan, plans=plans)
            desired_limit = self.get_plan_max_storage_mb_by_id(plan_id=desired_plan, plans=plans)
            if desired_limit < current_limit:
                self.module.params["plan"] = current_plan
                self.module.warn(
                    "Shrinking plans is not supported: current plan %s, desired plan %s"
                    % (current_plan, desired_plan)
                )

        return super(AnsibleVultrContainerRegistry, self).update(resource=resource)

    def get_plan_list(self):
        result = []
        plans = self.api_query(path="/registry/plan/list").get("plans", {})
        if plans:
            for plan in plans.keys():
                result.append(dict_merge(dict(id=plan), plans.get(plan, {})))
        return result

    def get_plan_max_storage_mb_by_id(self, plan_id=None, plans=None):
        for plan in plans:
            if plan_id == plan.get("id", ""):
                return plan.get("max_storage_mb", 0)
        return 0

    def get_plan_id_by_max_storage_mb(self, max_mb=None, plans=None):
        for plan in plans:
            if max_mb == plan.get("max_storage_mb", 0):
                return plan.get("id", "")
        return ""


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            name=dict(type="str", required=True),
            public=dict(type="bool"),
            region=dict(type="str"),
            plan=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=[
            ("state", "present", ["public", "region", "plan"]),
        ],
        supports_check_mode=True,
    )

    vultr = AnsibleVultrContainerRegistry(
        module=module,
        namespace="vultr_container_registry",
        resource_path="/registry",
        resource_create_param_keys=["name", "public", "region", "plan"],
        resource_key_name="name",
        resource_update_method="PUT",
        resource_update_param_keys=["public", "plan"],
        ressource_result_key_singular="registry",
        ressource_result_key_plural="registries",
        response_in_list=False,
    )

    if module.params.get("state") == "absent":  # type: ignore
        vultr.absent()
    else:
        vultr.present()


if __name__ == "__main__":
    main()
