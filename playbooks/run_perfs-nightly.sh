#!/usr/bin/env bash

# This script executes the 'run-perfs.sh' script in the playbook
# But as it is 'nightly', it runs the 'default' vanilla script from
# the repository. Make sure there are no local changes in repo.

PERF_SCRIPT="/etc/ansible/roles/glusterfs.perf/playbooks/run_perfs.sh"

ANSIBLE_DIR="/etc/ansible/roles/glusterfs.perf"
if [ ! -d $ANSIBLE_DIR ]; then
    echo "$ANSIBLE_DIR not found, exiting..."
    exit 1
fi

cd $ANSIBLE_DIR

git stash
git fetch origin
git rebase origin/master 

# If there are local changes, which is going to conflict
# with master, lets keep the local change itself
# if there are no conflict, then below command will be dummy
git rebase --abort

. ${PERF_SCRIPT}

# get back the changes as is (but now on the master)
git stash apply
