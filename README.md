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
| glusterfs_perf_clients | | | Clients on which to mount the volume and run the tests|
| glusterfs_perf_client | | First among the list of clients | Client on which to mount. This will the client where the perf test is launched. |
| glusterfs_perf_resdir | | /var/tmp/glusterperf | Directory to store perf results|
| glusterfs_perf_mail_sender || sac@redhat.com | email address which has to be listed in the from field of the status email. |
| glusterfs_perf_to_list || UNDEF | email addresses of the list of people to whom the report has to be sent. Not this is not comma separated addresses, but yaml list. Plese see playbooks/cluster_setup.yml for an example. |
| glusterfs_perf_ofile || /tmp/perf-results-<date> | Output file where results have to be stored |
| glusterfs_perf_git_repo | | https://github.com/gluster/glusterfs.git | Set the URL of new repo to be cloned |
| glusterfs_perf_git_refspec | | - | Details of particular patch to be fetched. Check the details in 'Download' section in gerrit for refspec details |


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

Setting up and running the tests
--------------------------------
Bootstrapping: Ensure Ansible >= 2.7 is present.
Install the roles gluster-ansible-infra and glusterfs-perf.
Copy the playbook under playbooks/cluster_setup.yml directory in the
glusterfs-perf role and change the variables appropriately and run the command:

\# gluster-ansible -i \<inventory-file\> cluster_setup.yml

Scripts to run a particular patch
---------------------------------

If you need to run the whole tests on any of the patch from https://review.gluster.org use the below command.

```
# cd /etc/ansible/roles/glusterfs.perf
# ./playbooks/run_perfs-with-patch.sh -t new-tag -s refs/changes/76/22576/3 -e me@gluster.org,you@someother.org,she@my.org,he@your.org

# git stash
# ./playbooks/run_perfs-with-patch.sh -t another-tag -v release-6 -e me@gluster.org,you@someother.org,she@my.org,he@your.org


```


License
-------

GPLv3

