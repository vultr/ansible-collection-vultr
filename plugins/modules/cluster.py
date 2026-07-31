#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026, Rene Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: cluster
short_description: Manages clusters on Vultr
description:
  - Create, update and remove clusters.
version_added: "1.15.0"
author:
  - "Rene Moser (@resmo)"
options:
  label:
    description:
      - Label of the cluster.
    required: true
    aliases: [ name ]
    type: str
  region:
    description:
      - Region where the cluster should be created.
      - Required if I(state=present).
    type: str
  plan:
    description:
      - Plan id for the cluster instances.
      - Mutually exclusive with I(instance_template).
      - One of I(plan) or I(instance_template) is required if I(state=present).
    type: str
  instance_template:
    description:
      - Instance template label for the cluster instances.
      - Resolved to the instance template UUID.
      - Mutually exclusive with I(plan).
      - One of I(plan) or I(instance_template) is required if I(state=present).
    type: str
  min_pool_count:
    description:
      - Minimum number of instances in the cluster pool.
    type: int
  desired_pool_count:
    description:
      - Desired number of instances in the cluster pool.
    type: int
  hostname:
    description:
      - Hostname for cluster instances.
    type: str
  pkey:
    description:
      - Private network key for the cluster.
    type: int
  vlanid:
    description:
      - VLAN ID for the cluster private network.
    type: int
  notify_activate:
    description:
      - Notify by email when the cluster is activated.
    type: bool
  os:
    description:
      - Operating system name to install.
    type: str
  app:
    description:
      - One-click application name to install.
    type: str
  image:
    description:
      - Marketplace application name to install.
    type: str
  gpu_fabric:
    description:
      - Whether this should be a GPU fabric cluster.
    type: bool
  vpcs:
    description:
      - VPC names (descriptions) to attach to the cluster.
      - Values are resolved to VPC ids in the selected I(region).
    type: list
    elements: str
  state:
    description:
      - State of the cluster.
    default: present
    choices: [ present, absent ]
    type: str
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
- name: Ensure a cluster is present
  vultr.cloud.cluster:
    label: my cluster
    region: ewr
    plan: vc2-1c-2gb
    min_pool_count: 1
    desired_pool_count: 1
    hostname: my-cluster

- name: Ensure a cluster is absent
  vultr.cloud.cluster:
    label: my cluster
    state: absent
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
vultr_cluster:
  description: Response from Vultr API.
  returned: success
  type: dict
  contains:
    id:
      description: ID of the cluster.
      returned: success
      type: str
    label:
      description: Label of the cluster.
      returned: success
      type: str
    region:
      description: Region where the cluster is located.
      returned: success
      type: str
    plan:
      description: Plan of the cluster.
      returned: success
      type: str
    min_pool_count:
      description: Minimum number of instances in the cluster pool.
      returned: success
      type: int
    desired_pool_count:
      description: Desired number of instances in the cluster pool.
      returned: success
      type: int
    hostname:
      description: Hostname for cluster instances.
      returned: success
      type: str
    status:
      description: Subscription status of the cluster.
      returned: success
      type: str
    state:
      description: Operational state of the cluster.
      returned: success
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


class AnsibleVultrCluster(AnsibleVultr):
    def get_instance_template(self):
        return self.query_filter_list_by_name(
            key_name="label",
            param_key="instance_template",
            path="/instances/templates",
            result_key="instance_templates",
            fail_not_found=True,
        )

    def get_os(self):
        return self.query_filter_list_by_name(
            key_name="name",
            param_key="os",
            path="/os",
            result_key="os",
            fail_not_found=True,
        )

    def get_app(self):
        return self.query_filter_list_by_name(
            key_name="deploy_name",
            param_key="app",
            path="/applications",
            result_key="applications",
            fail_not_found=True,
            query_params={"type": "one-click"},
        )

    def get_image(self):
        return self.query_filter_list_by_name(
            key_name="deploy_name",
            param_key="image",
            path="/applications",
            result_key="applications",
            fail_not_found=True,
            query_params={"type": "marketplace"},
        )

    def get_vpc_ids(self):
        vpc_names = list(self.module.params["vpc_ids"])
        vpcs = self.query_list(path="/vpcs", result_key="vpcs")

        vpc_ids = list()
        for vpc in vpcs:
            if (
                self.module.params.get("region")
                and self.module.params["region"] != vpc["region"]
            ):
                continue

            if vpc["description"] in vpc_names:
                vpc_ids.append(vpc["id"])
                vpc_names.remove(vpc["description"])

        if vpc_names:
            self.module.fail_json(msg="VPC names not found: %s" % ", ".join(vpc_names))

        return vpc_ids

    def configure(self):
        super(AnsibleVultrCluster, self).configure()

        if self.module.params["state"] != "absent":
            if self.module.params.get("instance_template") is not None:
                self.module.params["instance_template"] = self.get_instance_template()[
                    "id"
                ]

            if self.module.params.get("os") is not None:
                self.module.params["os_id"] = self.get_os()["id"]

            if self.module.params.get("app") is not None:
                self.module.params["app_id"] = self.get_app()["id"]

            if self.module.params.get("image") is not None:
                self.module.params["image_id"] = self.get_image()["image_id"]

            if self.module.params.get("vpcs") is not None:
                self.module.params["vpc_ids"] = self.get_vpc_ids()

    def create_or_update(self):
        resource = super(AnsibleVultrCluster, self).create_or_update()
        if resource:
            resource = self.wait_for_state(
                resource=resource, key="status", states=["active"]
            )
        return resource


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            label=dict(type="str", required=True, aliases=["name"]),
            region=dict(type="str"),
            plan=dict(type="str"),
            instance_template=dict(type="str"),
            min_pool_count=dict(type="int"),
            desired_pool_count=dict(type="int"),
            hostname=dict(type="str"),
            pkey=dict(type="int", no_log=False),
            vlanid=dict(type="int"),
            notify_activate=dict(type="bool"),
            os=dict(type="str"),
            app=dict(type="str"),
            image=dict(type="str"),
            gpu_fabric=dict(type="bool"),
            vpcs=dict(type="list", elements="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        mutually_exclusive=[
            ("plan", "instance_template"),
            ("os", "app", "image"),
        ],
        required_if=[
            ("state", "present", ["region"]),
            ("state", "present", ["plan", "instance_template"], True),
        ],
        supports_check_mode=True,
    )

    vultr = AnsibleVultrCluster(
        module=module,
        namespace="vultr_cluster",
        resource_path="/clusters",
        resource_result_key_singular="cluster",
        resource_create_param_keys=[
            "region",
            "plan",
            "instance_template",
            "label",
            "min_pool_count",
            "desired_pool_count",
            "hostname",
            "pkey",
            "vlanid",
            "notify_activate",
            "os_id",
            "app_id",
            "image_id",
            "gpu_fabric",
            "vpc_ids",
        ],
        resource_update_param_keys=[
            "label",
            "min_pool_count",
            "desired_pool_count",
            "hostname",
            "vpc_ids",
        ],
        resource_key_name="label",
        resource_update_method="PUT",
    )

    if module.params.get("state") == "absent":  # type: ignore
        vultr.absent()
    else:
        vultr.present()


if __name__ == "__main__":
    main()
