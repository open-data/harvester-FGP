#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Usage: csv2html.py [-f csv_file_path]

Create HTML table from CSV

Options:
    -f CSV file_path
"""

import sys
import csv

from datetime import datetime

if len(sys.argv) < 3:
    print "Usage: csv2html.py -f csv_file_path"
    exit(1)

if sys.argv[1] == "-f" and len(sys.argv[2]) > 0:

    # Open the CSV file for reading
    reader = csv.reader(open(sys.argv[2]))

    # Create the HTML file for output
    with open("harvested_record_errors.html", 'w+') as f:

        rownum = 0
        html = ''

        # Generate html
        f.write('<html><head><title>FGP Harvester Errors</title></head><body><h1>FGP Harvester Errors</h1><h4>Created: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '</h4>')

        # Generate table contents
        # - assuming first row in csv contains column names
        # if numrecords < 2:
        #     f.write('<p>No errors found!</p>')

        # else:

        html += '<table border="1" cellspacing="0" cellpadding="5" frame="box" rules="all">'
        for row in reader:

            # write header row. assumes first row in csv contains column names
            if rownum == 0:
                html += '<tr>'
                html += '<th>&nbsp;</th>'
                for column in row:
                    html += '<th>' + column + '</th>'
                html += '</tr>'

            # write all other rows
            else:
                html += '<tr>'
                html += '<td>' + str(rownum) + '.</td>'
                colnum = 0
                for column in row:
                    if colnum < 2:
                        html += '<td nowrap>' + column + '</td>'
                    else:
                        html += '<td>' + column + '</td>'
                    colnum += 1
                html += '</tr>'

            rownum += 1

        html += '</table>'

        # Write out the table html if there are rows
        if rownum > 0:
            f.write(html)
        else:
            f.write('<p>No errors found!</p>')

        f.write('</body></html>')

    exit(0)
