#!/usr/bin/python

import os
import numpy as np
import matplotlib as mpl
# below is critical for running over ssh/ansible
if os.environ.get('DISPLAY','') == '':
    mpl.use('Agg')
import matplotlib.pyplot as plt
import csv
import json
from pprint import pprint
import sys, getopt
from datetime import datetime, timedelta
import random

def read_current_values(rdir, obj, k):
    try:
        with open("%s/%s" % (rdir, k)) as f:
            data = json.load(f)
        obj[k] = data['results']['files-per-sec']
    except:
        obj[k] = 1.0

def plot_graph(ref, cur, plot_label, tags):
    # set width of bar
    barWidth = 1.0 / (2 + len(tags))

    #get nightly dir
    prev_val = {}
    yesterday = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")
    nightly = "/var/tmp/glusterperf/%s-nightly" % yesterday
    # actually get the perf number from the results file.
    for key in plot_label:
        read_current_values(nightly, prev_val, key)

    # Set position of bar on X axis
    r1 = np.arange(len(cur))

    # Make the plot
    plt.bar(r1, [cur[k] for k in plot_label], color='#7f6d5f', width=barWidth, edgecolor='white', label="this")

    # graph with yesterday night run.
    rtag = [x + barWidth for x in r1]
    r = lambda: random.randint(0,255)
    plt.bar(rtag, [prev_val[k] for k in plot_label], color='#%02X%02X%02X' % (r(), r(), r()), width=barWidth, edgecolor='white', label="yesterday")
    print("==== Comparision from Tag: yesterday nightly ====\n")
    for key in plot_label:
        cval = cur[key]
        pval = prev_val[key]
        print ("%-15s %13f -> %13f %11f%%" % (key, pval, cval, ((cval - pval) / pval) * 100))

    prev_rtag = rtag
    for t in tags:
        rtag = [x + barWidth for x in prev_rtag]
        prev_rtag = rtag
        vtag = []
        print("==== Comparision from Tag: %s ====\n" % t)
        for key in plot_label:
            cval = cur[key]
            res = ref[t][key]
            vtag.append(res)
            print ("%-15s %13f -> %13f %11f%%" % (key, res, cval, ((cval - res) / res) * 100))

        # For different colored graph
        r = lambda: random.randint(0,255)
        plt.bar(rtag, vtag, color='#%02X%02X%02X' % (r(), r(), r()), width=barWidth, edgecolor='white', label=t)

    # Add xticks on the middle of the group bars
    plt.xlabel('type of tests', fontweight='bold')
    plt.ylabel('files/sec')

    plt.xticks([r + barWidth for r in range(len(cur))], plot_label, rotation=90)

    # Increase the bottom space
    plt.subplots_adjust(bottom=0.3)

    # Create legend & Show graphic
    plt.legend()
    plt.plot()
    plt.savefig("%s/%s.png" % (result_dir, plot_label[0]))
    #plt.show()
    plt.close()

def load_reference_values(ops, tags):
    global ref_value

    # Read CSV file for reference
    with open(csv_file) as src_file:
        csv_lines = csv.DictReader(src_file)
        line_count = 0
        index_dict = {}
        for row in csv_lines:
            tag = row['TAG']
            ref_value[tag] = {}
            tags.append(tag)
            for key in ops:
                ref_value[tag][key] = float(row[key])

def dump_results(ops, ref, tags):
    cur_res = {}

    # actually get the perf number from the results file.
    for key in ops:
        read_current_values(result_dir, cur_res, key)

    plot_graph(ref, cur_res, ops, tags)

def parse_args(prog, argv):
    global current_tag
    global result_dir
    global csv_file

    try:
        opts, args = getopt.getopt(argv, "hr:t:c:", ["help", "result-dir=","tag=", "csv-file="])
    except getopt.GetoptError:
        print('%s --result-dir DIR [--tag TAG] [--csv-file FILE]' % prog)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            print('%s --result-dir DIR [--tag TAG] [--csv-file FILE]' % prog)
            sys.exit(2)
        elif opt == '-r' or opt == '--result-dir':
            result_dir = arg
        elif opt == '-t' or opt == '--tag':
            current_tag = arg
        elif opt == '-c' or opt == '--csv-file':
            csv_file = arg

    if result_dir == "":
        result_dir = '/var/tmp/glusterperf/' + current_tag


def main(argv):
    global current_tag

    ops = ['create', 'delete', 'append', 'overwrite', 'rename', 'mkdir', 'rmdir', 'symlink', 'setxattr', 'chmod', 'delete-renamed', 'read', 'readdir', 'stat', 'getxattr', 'ls-l' ]
    tags = []

    d = datetime.now()
    current_tag = d.strftime("%Y-%m-%d")
    yesterday = datetime.strftime(d - timedelta(1), "%Y-%m-%d")
    parse_args(argv[0], argv[1:])
    load_reference_values(ops, tags)

    print(d)
    dump_results(ops, ref_value, tags)
    print("==== End of results ====\n")

current_tag = ""
result_dir = ""
csv_file = "data/results.csv"
ref_value = {}

if __name__ == "__main__":
   main(sys.argv)
