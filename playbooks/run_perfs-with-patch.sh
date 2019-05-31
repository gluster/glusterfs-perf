#!/usr/bin/env bash

# This script executes the 'run-perfs.sh' script in the playbook
# But as it is 'nightly', it runs the 'default' vanilla script from
# the repository. Make sure there are no local changes in repo.

PERF_SCRIPT="/etc/ansible/roles/glusterfs.perf/playbook/run_perfs.sh"

ANSIBLE_DIR="/etc/ansible/roles/glusterfs.perf"
if [ ! -d $ANSIBLE_DIR ]; then
    echo "$ANSIBLE_DIR not found, exiting..."
    exit 1
fi


function parse_args () {
    #    args=`getopt frcbkphHno:t: "$@"`
    args=`getopt r:t:s:v:e: "$@"`
    set -- $args
    while [ $# -gt 0 ]; do
        case "$1" in
        -r)    repo="$2"; shift;;
        -t)    tag="$2" ; shift;;
        -s)    refspec="$2"; shift ;;
        -v)    version="$2"; shift ;;
        -e)    emails="$2"; shift
        esac
        shift
    done
    if [ "x$refspec" != "x" -a "x$version" != "x" ]; then
        echo "One can provide only refspec(-s) or version/branch(-v) option, not both"
        exit 1
    fi
}

repo="https://review.gluster.org/glusterfs"
parse_args $@

# Make sure there are no local changes
cd $ANSIBLE_DIR
git stash

# Run the below script
cd playbooks

if [ "x$repo" != "x" ]; then
    git grep -l git_repo | xargs sed -i "s/#git_repo/glusterfs_perf_git_repo: $repo/g"
fi

if [ "x$refspec" != "x" ]; then
    git grep -l git_refspec | xargs sed -i "s/#git_refspec/glusterfs_perf_git_refspec: $refspec/g"
fi

if [ "x$version" != "x" ]; then
    git grep -l git_version | xargs sed -i "s/#git_version/glusterfs_perf_git_version: $version/g"
fi

if [ "x$tag" != "x" ]; then
    git grep -l "perf_tag: " | xargs sed -i "s/perf_tag: nightly/perf_tag: $tag/g"
fi

#Emails should be 'comma' separated
if [ "x$emails" != "x" ]; then
    IFS=','
    e_arr=($emails)
    for email in ${e_arr[@]}; do
        git grep -l "#Add email" | xargs sed -i "s/\(.*\)#Add email/\1- $email\n\1#Add email/g"
    done
fi

$(PERF_SCRIPT)

# get back the changes as is (but now on the master)
git stash apply

