#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, René Moser <mail@renemoser.net>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: block_storage
short_description: Manages block storage volumes on Vultr
description:
  - Manage block storage volumes.
version_added: "1.0.0"
author:
  - "René Moser (@resmo)"
  - "Yanis Guenane (@Spredzy)"
options:
  label:
    description:
      - User-defined label for the VFS subscription
    type: str
    required: true
  region:
    description:
      - Region identifier where to create the VFS
    type: str
    required: true
  state:
    description:
      - State of the block storage volume.
    default: present
    choices: [ present, absent]
    type: str
  storage_size:
    description:
      - Storage provisioned for the VFS
      - Required if I(state) is present.
    type: dict
    contains:
      gb:
        description:
          - Size in gigabytes
        type: int
        required: true
  disk_type:
    description:
      - Type of storage disk
      - Required if I(state) is present.
    type: str
    default: nvme
    choices: [ nvme ]
  tags:
    description:
      - Optional tags to apply to the VFS subscription
    type: list
    elements: str
    sample: [ prod, web ]
  attachments:
    description:
      - VPS instances attached to the VFS subscription
      - Required if I(state) is present.
      - Affected by I(exclusive_attachments).
    type: list
    elements: str
    sample: [ inst-456def ]
  exclusive_attachments:
    description:
      - Whether to detach all other VPS instances not specified in I(attachments).
    type: bool
    default: false
extends_documentation_fragment:
  - vultr.cloud.vultr_v2
"""

EXAMPLES = """
---
- name: Ensure a file system is present
  vultr.cloud.vfs:
    name: myfilesystem
    storage_size:
      gb: 10
    region: ams

- name: Ensure a file system is absent
  vultr.cloud.vfs:
    name: myfilesystem
    state: absent

- name: Ensure a file system exists and is attached a server instance
  vultr.cloud.vfs:
    name: myfilesystem
    attachments:
      - inst-456def
    storage_size:
      gb: 50
    block_type: high_perf

- name: Ensure a file system exists but is not attached to any server instance
  vultr.cloud.vfs:
    name: myvolume
    storage_size:
      gb: 50
    attachments: []
    exclusive_attachments: true
"""

RETURN = """
---
vultr_api:
  description: Response from Vultr API with a few additions/modification.
  returned: success
  type: dict
  contains:
    api_account:
      description: Account used in the ini file to select the key.
      returned: success
      type: str
      sample: default
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
vfs:
  description: Response from Vultr API.
  returned: success
  type: dict
  contains:
    id:
      description: Unique identifier for the VFS subscription
      returned: success
      type: str
    region:
      description: Region identifier where the VFS is located
      returned: success
      type: str
    date_created:
      description: Creation timestamp of the VFS subscription
      returned: success
      type: str
      sample: 2024-01-01T12:00:00Z
    status:
      description: Current status of the VFS subscription
      returned: success
      type: str
      sample: active
    label:
      description: User-defined label for the VFS subscription
      returned: success
      type: str
    tags:
      description: List of tags associated with the VFS subscription
      returned: success
      type: list
      elements: str
    disk_type:
      description: Type of storage disk
      returned: success
      type: str
      choice: [ nvme ]
    storage_size:
      description: Storage provisioned for the VFS
      returned: success
      type: dict
      contains:
        bytes:
          description: Size in bytes
          returned: success
          type: int
          sample: 10737418240
        gb:
          description: Size in gigabytes
          returned: success
          type: int
          sample: 10
    storage_used:
      description: Storage used
      returned: success
      type: dict
      contains:
        bytes:
          description: Size in bytes
          returned: success
          type: int
          sample: 10737418240
        gb:
          description: Size in gigabytes
          returned: success
          type: int
          sample: 10
    billing:
      description: Billing info
      returned: success
      type: dict
      contains:
        charges:
          description: Current billing charges
          returned: success
          type: float
          sample: 10.5
        monthly:
          description: Monthly billing amount
          returned: success
          type: float
          sample: 30
  attachments:
    description:
      - VPS instances attached to the VFS subscription
      - Included if I(attachments) is included or I(exclusive_attachments) is true.
    returned: success
    type: list
    elements: str
    sample: [ inst-456def ]
"""

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.vultr_v2 import AnsibleVultr, vultr_argument_spec


class AnsibleVultrVFS(AnsibleVultr):
    def update(self, resource):
        current_size = resource["storage_size"]["gb"]
        desired_size = self.module.params["storage_size"]["gb"]
        if desired_size < current_size:
            self.module.params["storage_size"]["gb"] = current_size
            self.module.warn("Shrinking is not supported: current size %s, desired size %s" % (current_size, desired_size))
        return super(AnsibleVultrVFS, self).update(resource=resource)

    def present(self):
        resource = self.create_or_update() or dict()

        # If attachments are not listed nor exclusive, exit and show result.
        instances_to_attach = set(self.module.params.get("attachments"))
        exclusive_attachments = self.module.params.get("exclusive_attachments")
        if len(instance_to_attach) == 0 and not exclusive_attachments:
            self.get_result(resource)

        # Check instances attached and add them to the result body.
        # GET /vfs/{vfs_id}/attachments
        instances_attached = set(raise Exception("TODO"))  # TODO get attachments
        if exclusive_attachments:
          self.result["attachments"] = instances_to_attach
        else:
          self.result["attachments"] = instances_to_attach + instances_attached

        # If attachments are the in sync, exit and show result.
        is_same_set = instances_to_attach == instances_attached
        is_subset_and_nonexclusive = (not exclusive_attachments) and instances_attached.issubset(instances_to_attach)
        if is_same_set or is_subset_and_nonexclusive:
          self.get_result(resource)

        # Attachments are not in sync
        self.result["changed"] = True

        if not self.module.check_mode:
          # Add specified attachments
          instances_to_add = instances_to_attach - instances_attached
          for instance in instances_to_add:
            # POST /vfs/{vfs_id}/attachments/{vps_id}
            raise Exception("TODO")  # TODO attach each instance

          # If attachments are exclusive, remove unspecified attachments
          if exclusive_attachments:
            instances_to_remove = instances_attached - instances_to_attach
            for instance in instances_to_remove:
              # DELETE /vfs/{vfs_id}/attachments/{vps_id}
              raise Exception("TODO")  # TODO remove each instances

        self.get_result(resource)


def main():
    argument_spec = vultr_argument_spec()
    argument_spec.update(
        dict(
            label=dict(type="str", required=True, aliases=["name"]),
            region=dict(type="str"),
            state=dict(type="str", choices=["present", "absent"], default="present"),
            storage_size=dict(type="dict"),
            disk_type=dict(type="str", choices=["nvme"], default="nvme"),
            tags=dict(type="list", default=[]),
            attachments=dict(type="list", elements="str", default=[]),
            exclusive_attachments=dict(type="bool", default=False),
        )  # type: ignore
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ["state", "present", ["region", "storage_size"]],
        ],
    )

    vultr = AnsibleVultrVFS(
        module=module,
        namespace="vultr_vfs",
        resource_path="/vfs",
        ressource_result_key_singular="vfs",
        resource_create_param_keys=["label", "region", "storage_size", "disk_type", "tags"],
        resource_update_param_keys=["storage_size"],
        resource_key_name="label",
    )

    if module.params.get("state") == "absent":  # type: ignore
        vultr.absent()
    else:
        vultr.present()


if __name__ == "__main__":
    main()
