#!/usr/bin/python

import json

DEFAULT_LEVELS="1, 6, 60"

def new_editors(old_period, new_period, levels=DEFAULT_LEVELS):
    # new editors list
    new_editors = []
    # Loading old period json filehandle
    json_old = json.load(old_period)
    data_old = json_old["result"]["Individual Results"][0]
    # iteration on each user of individual results list
    #       counts editor without edit on old period and add them to new_editors
    for k in data_old.keys():
        if(int(data_old[k]["edits"])==0):
            new_editors.append(k)

    json_new= json.load(new_period)
    data_new= json_new["result"]["Individual Results"][0]
    level = levels.split(",")
    # count of surviving editors by level
    new_counts = dict()
    for k in new_editors:
        edits = int(data_new[k]["edits"])
        for l in level:
            if edits>=int(l):
                if int(l) in new_counts.keys():
                    new_counts[int(l)] = new_counts[int(l)]+1
                else:
                    new_counts[int(l)] = 1
    print "%s - %s" % (json_new["parameters"]["start_date"], json_new["parameters"]["end_date"])
    for k in sorted(new_counts.keys()):
        print "\tnew editors with more than %d edits:\t %d" % (k, new_counts[k])


def getopt_fallback():
    """Fallback on getopt if your system don't have ArgumentParser."""
    import getopt, sys
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "o:n:", ["--old=", "--new="])
    except getopt.GetoptError:                               
        sys.exit(2)
    new = ""
    old = ""
    for opt, arg in opts:
        if opt in ("-o", "--old"):
            old = arg
        if opt in ("-n", "--new"):
            new = arg
    if(new != "" and old != ""):
        old_period = open(old)
        new_period = open(new)
        new_editors(old_period, new_period)
        old_period.close()
        new_period.close()

def main():
    """Main method, entry point of the script."""
    try:
        from argparse import ArgumentParser
        description = "Computes new editor numbers based on WikiMetrics data"
        parser = ArgumentParser(description=description)

        parser.add_argument("-o", "--old",
                            type=file,
                            dest="old_period",
                            metavar="old_period.json",
                            required=True,
                            help="The old period data, as a JSON file")

        parser.add_argument("-n", "--new",
                            type=file,
                            dest="new_period",
                            metavar="new_period.json",
                            required=True,
                            help="The new period data, as a JSON file")
        args = parser.parse_args()

        new_editors(args.old_period, args.new_period)
    except ImportError:
        getopt_fallback()

if __name__ == "__main__":
    main()
