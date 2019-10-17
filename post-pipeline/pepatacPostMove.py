#!/usr/bin/env python
#Ben Keith
#pepatacPostMove.py
#The script is intended to be a simple way to move all PEPATAC outputs from scratch space to the data directory. The script requires a curated stats output, generated from PEPATAC through "looper summarize [config]", or any tsv that contains a column with full path pointers to the raw fastqs used for PEPATAC (one sample per row).
#
# USAGE: python pepatacPostMove.py -i [PEPATAC RUN]_stats_summary.tsv -r readCol
#
#Like with pepatac, the script assumes that it will be run in the sample place as the pepatac project (the directory containing the config and annotation file)
# 
#By default, the 'mkdir' and 'cp' command will be printed. These commands can be copied and executed, or the flag '--run' can be added. I indended this to be a sanity check before initiating a potential multi TB copy.

from __future__ import print_function
import sys
import csv
import os
from optparse import OptionParser, OptionGroup
from subprocess import call

#### OPTIONS ####
# read options from command line
usage = "example usage: %prog [options] -i '*_stats_summary.tsv' -r 'read1'"
opts = OptionParser(usage=usage)
opts.add_option("-i", help="<summary CSV> 'PEPATAC summary csv. e.g. '*_stats_summary.tsv'", metavar="INPUT")
opts.add_option("-r", help="<TSV col> Name of a column that provides a path to sample fastqs. e.g. 'read1'", metavar="COL")
opts.add_option("--sample",default="sample_name", help="Name of the column that points to samples. Defaults to name used in example files in /proj/fureylab/pipelines/ATAC/pepatac/submission*")
opts.add_option("--run", action="store_true", default=False, help="Add this flag for the script to initiate the copying. Script defaults to printing move statements.")

group = OptionGroup(opts, "Notes",
                    "By default, the 'mkdir' and 'cp' command will be printed. These commands can be copied "
                    "and executed, or the flag '--run' can be added. I indended this to be a sanity check "
                    "before initiating a potential multi TB copy")
opts.add_option_group(group)

options, arguments = opts.parse_args()

# return usage information if no argvs given
if len(sys.argv)==1:
    os.system(sys.argv[0]+" --help")
    sys.exit()


#### SCRIPT ####
with open(options.i, 'r') as tsvFile:
    reader = csv.DictReader(tsvFile, dialect='excel-tab')
    for row in reader:
        readPath = row[options.r]
        samplePath = readPath.split("fastq")[0]
        finalOutPath = samplePath + "pepatac/out"
        finalSubPath = samplePath + "pepatac/sub"
        sample = row[options.sample]

        mkdirArgs = "mkdir -p %s; mkdir -p %s" % (finalSubPath, finalOutPath)
        outMoveArg = "cp -rp results_pipeline/%s/* %s" % (sample, finalOutPath)
        subMoveArg = "cp -r submission/%s.yaml %s; cp -r submission/pepatac.py_%s.sub %s;" \
                     " cp -r submission/pepatac.py_%s.log %s" \
                     % (sample, finalSubPath, sample, finalSubPath, sample, finalSubPath)

        if options.run:
            call(mkdirArgs, shell=True)
            call(outMoveArg, shell=True)
            call(subMoveArg, shell=True)
        else:
            print(mkdirArgs)
            print(outMoveArg)
            print(subMoveArg)

tsvFile.close()


