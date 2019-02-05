glusterfs.perf
=========

On a given set of hosts, create a testbed to test GlusterFS builds.
glusterfs.perf role:
  * Installs the necessary packages to build GlusterFS from source.
  * Clones the GlusterFS repository
  * Buils the filesystem from source and installs
  * Creates a GlusterFS volume and mounts it

Requirements
------------

Ansible >= 2.7
gluster-ansible

Role Variables
--------------

| Name                     |Choices| Default value         | Comments                          |
|--------------------------|-------|-----------------------|-----------------------------------|
| glusterfs_perf_volume_state | present/absent/started/stopped | present | GlusterFS volume state.  |
| glusterfs_perf_volume | | UNDEF | Name of the gluster volume |
| glusterfs_perf_bricks | | UNDEF | GlusterFS brick directories for volume creation |
| glusterfs_perf_hosts  | | UNDEF | List of hosts that will be part of the cluster  |
| glusterfs_perf_transport | tcp/tcp,rdma | tcp | Transport to be configured while creating volume |
| glusterfs_perf_replica_count | | Omitted by default | Replica count for the volume |
| glusterfs_perf_arbiter_count | | Omitted by default | Arbiter count for the volume |
| glusterfs_perf_disperse_count | | Omitted by default | Disperse count for the volume |
| glusterfs_perf_redundancy_count | | Omitted by default | Redundancy count for the volume |
| glusterfs_perf_force | yes/no | no | Whether GlusterFS volume should be created by force |
| glusterfs_perf_mountpoint | | /mnt/glusterfs | GlusterFS mount point |
| glusterfs_perf_server | | UNDEF | Server to use while mounting GlusterFS volume |
| glusterfs_perf_client | | glusterfs_perf_server | Client on which to mount the volume|
| glusterfs_perf_resdir | | /var/tmp/glusterperf | Directory to store perf results|

Example Playbook
----------------

```
---
- name: Setup a GlusterFS cluster from source tree
  remote_user: root
  gather_facts: true
  hosts: all
  vars:
    glusterfs_perf_volume: perfvol
    glusterfs_perf_bricks: /gluster_bricks/perfbrick
    glusterfs_perf_hosts: "{{ groups['all'] }}"
    glusterfs_perf_replica_count: 2
    glusterfs_perf_server: "{{ groups['all'][0] }}"

  roles:
    - glusterfs.perf
```

License
-------

GPLv3

