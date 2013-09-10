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

