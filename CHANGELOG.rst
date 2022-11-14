==============================
Vultr Collection Release Notes
==============================

.. contents:: Topics


v1.3.1
======

Bugfixes
--------

- instance - Fixed an issue with ssh keys being ignored when deploying an new instance.

v1.3.0
======

Bugfixes
--------

- instance - Fixed the handling for activating/deactivating backups.

v1.2.0
======

Minor Changes
-------------

- block_storage - Added the parameter ``block_type`` to configure block types, default value is ``high_perf``.
- dns_record - Removed the default value ``0`` for the optional parameter ``priority``.

v1.1.0
======

Minor Changes
-------------

- block_storage - the default value for parameter ``live`` while attaching a volume changed to a more sensible default ``false``.

New Modules
-----------

- instance - Manages server instances on Vultr.

v1.0.1
======

Minor Changes
-------------

- Improved documentation and removed unused code.

v1.0.0
======

New Modules
-----------

- account_info - Get information about the Vultr account.
- block_storage - Manages block storage volumes on Vultr.
- block_storage_info - Get information about the Vultr block storage available.
- dns_domain - Manages DNS domains on Vultr.
- dns_domain_info - Gather information about the Vultr DNS domains available.
- dns_record - Manages DNS records on Vultr.
- firewall_group - Manages firewall groups on Vultr.
- firewall_group_info - Gather information about the Vultr firewall groups available.
- firewall_rule - Manages firewall rules on Vultr.
- firewall_rule_info - Gather information about the Vultr firewall rules available.
- network - Manages networks on Vultr.
- network_info - Gather information about the Vultr networks available.
- os_info - Get information about the Vultr OSes available.
- plan_info - Gather information about the Vultr plans available.
- plan_metal_info - Gather information about the Vultr bare metal plans available.
- region_info - Gather information about the Vultr regions available.
- reserved_ip - Manages reserved IPs on Vultr.
- ssh_key - Manages ssh keys on Vultr.
- ssh_key_info - Get information about the Vultr SSH keys available.
- startup_script - Manages startup scripts on Vultr.
- startup_script_info - Gather information about the Vultr startup scripts available.
- user - Manages users on Vultr.
- user_info - Get information about the Vultr user available.
- vpc - Manages VPCs on Vultr.
- vpc_info - Gather information about the Vultr vpcs available.
