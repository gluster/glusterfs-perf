#!/usr/bin/python

# has dependency of installing on fedora 'python3-matplotlib'
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
import datetime

def plot_graph(bars1, bars2, plot_label, target_file, b1_label, b2_label):
    # set width of bar
    barWidth = 0.25
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))

    # Make the plot
    plt.bar(r1, bars1, color='#7f6d5f', width=barWidth, edgecolor='white', label=b1_label)

    r2 = [x + barWidth for x in r1]
    plt.bar(r2, bars2, color='#557f2d', width=barWidth, edgecolor='white', label=b2_label)

    # Add xticks on the middle of the group bars
    plt.xlabel('group', fontweight='bold')

    plt.xticks([r + barWidth for r in range(len(bars1))], plot_label)

    # Create legend & Show graphic
    plt.legend()
    plt.plot()
    plt.savefig(target_file)
    #plt.show()
    plt.close()

def load_reference_values(wops, rops, tags):
    # Read CSV file for reference
    with open(csv_file) as src_file:
        csv_lines = csv.DictReader(src_file)
        line_count = 0
        index_dict = {}
        for row in csv_lines:
            tag = row['TAG']
            ref_read_value[tag] = {}
            ref_write_value[tag] = {}
            tags.append(tag)
            for key in wops:
                ref_write_value[tag][key] = float(row[key])
            for key in rops:
                ref_read_value[tag][key] = float(row[key])


def read_current_values(obj, k):
    with open("%s/%s" % (result_dir, k)) as f:
        data = json.load(f)
    obj[k] = data['results']['files-per-sec']


def dump_results(ops, ref, t):
    cur_res = {}
    b1 = []
    b2 = []
    op = []

    for key in ops:
        # actually get the perf number from the results file.
        read_current_values(cur_res, key)
        res = ref[t][key]
        cur = cur_res[key]
        b1.append(res)
        b2.append(cur)
        op.append(key)
        print ("%s: %f -> %f (%f%%)" % (key, res, cur, ((cur - res) / res) * 100))

    plot_graph(b1,b2, op, "%s/%s-%s.png" % (result_dir, t, ops[0]), t, current_tag)


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

    write_ops = ['create', 'delete', 'append', 'overwrite', 'rename', 'mkdir', 'rmdir', 'symlink', 'setxattr', 'chmod', 'delete-renamed' ]
    read_ops = [ 'read', 'readdir', 'stat', 'getxattr', 'ls-l' ]
    tags = []

    d = datetime.datetime.now()
    current_tag = d.strftime("%Y-%m-%d")

    parse_args(argv[0], argv[1:])
    load_reference_values(write_ops, read_ops, tags)

    # Output the results
    print(d)
    for t in tags:
        print("==== Comparision from Tag: %s to %s ====\n" % (t, current_tag))
        dump_results(write_ops, ref_write_value, t)
        dump_results(read_ops, ref_read_value, t)
        print("==== End of results ====\n")


current_tag = ""
result_dir = ""
csv_file = "data/results.csv"
ref_write_value = {}
ref_read_value = {}

if __name__ == "__main__":
   main(sys.argv)
