#!/usr/bin/python

import json

def new_editors(old_period, new_period):
    # new editors list
    new_editors = []
    # Loading old period json filehandle
    data_old        = json.load(old_period)["result"]["Individual Results"][0]
    # iteration on each user of individual results list
    #       counts editor without edit on old period and add them to new_editors
    for k in data_old.keys():
        if(int(data_old[k]["edits"])==0):
            new_editors.append(k)

    data_new= json.load(new_period)["result"]["Individual Results"][0]
    # new editors that survived
    count_new = 0
    # new editors that survived with more than 1 edit per month
    count_one_epm = 0
    # new editors that survived with more than 10 edits per month
    count_ten_epm = 0
    max_edit_new = 0
    for k in new_editors:
        edits = int(data_new[k]["edits"])
        max_edit_new = max(max_edit_new, edits)
        if(edits>=1):
            count_new = count_new + 1
        if(edits>=6):
            count_one_epm = count_one_epm + 1
        if(edits>=60):
            count_ten_epm = count_ten_epm + 1
    print """New editors that kept editing after WLM2011(Fr): %s
\t%s with more than one edit per month (6 months period)"
\t%s with more than ten edits per month (6 months period)"
\t%s max edits for a new contributors (6 months period)"""\
    % (count_new, count_one_epm, count_ten_epm, max_edit_new)


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
    except:
        getopt_fallback()

if __name__ == "__main__":
    main()
