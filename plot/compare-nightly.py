#!/usr/bin/python

import os
import csv
import json
from pprint import pprint
import sys, getopt
from datetime import datetime, timedelta

def read_current_values(rdir, obj, k):
    try:
        for d in os.listdir(rdir):
            if d not in obj:
                obj[d] = {}

            try:
                with open("%s/%s/smallfile/%s" % (rdir, d, k)) as f:
                    data = json.load(f)
                obj[d][k] = data['results']['files-per-sec']
            except:
                obj[d][k] = 1.0
    except:
	obj[k] = 1.0
    return

def dump_results(ops):
    cur_res = {}
    global result_dir

    for key in ops:
        read_current_values(result_dir, cur_res, key)

    prev_val = {}
    yesterday = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")
    nightly = "/var/tmp/glusterperf/%s/nightly" % yesterday

    # actually get the perf number from the results file.
    for key in ops:
        read_current_values(nightly, prev_val, key)

    # graph with yesterday night run.
    # actually get the perf number from the results file.
    print("==== Comparision from Tag: yesterday night master ====")
    try:
        for d in os.listdir(result_dir):
            print (d)
            for key in ops:
                cval = cur_res[d][key]
                pval = prev_val[d][key]
	        if pval is None:
		    pval = 1.0
                print ("%-15s %13f -> %13f %11f%%" % (key, pval, cval, ((cval - pval) / pval) * 100))
            print ("==========")
    except:
        print("Some error consult: gluster-devel@gluster.org");

    return

def parse_args(prog, argv):
    global current_tag
    global result_dir

    try:
        opts, args = getopt.getopt(argv, "hr:t:", ["help", "result-dir=","tag="])
    except getopt.GetoptError:
        print('%s --result-dir DIR [--tag TAG]' % prog)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('%s --result-dir DIR [--tag TAG]' % prog)
            sys.exit(2)
        elif opt == '-r' or opt == '--result-dir':
            result_dir = arg
        elif opt == '-t' or opt == '--tag':
            current_tag = arg

    d = datetime.now()
    if result_dir == "":
        result_dir = '/var/tmp/glusterperf/' + d.strftime("%Y-%m-%d") + "/" + current_tag
    else:
	result_dir = "%s/%s" % (result_dir, current_tag)
    return

def main(argv):
    global current_tag

    ops = ['create', 'delete', 'append', 'overwrite', 'rename', 'mkdir', 'rmdir', 'symlink', 'setxattr', 'chmod', 'delete-renamed', 'read', 'readdir', 'stat', 'getxattr', 'ls-l' ]

    d = datetime.now()
    current_tag = d.strftime("%Y-%m-%d")
    yesterday = datetime.strftime(d - timedelta(1), "%Y-%m-%d")
    parse_args(argv[0], argv[1:])

    print(d)
    dump_results(ops)
    print("==== End of results ====\n")

    return

current_tag = ""
result_dir = ""

if __name__ == "__main__":
   main(sys.argv)
