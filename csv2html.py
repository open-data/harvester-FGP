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

    replacements = {'</body>':'', '</html>':'', '<a name="bottom"/>':''}
    lines = []

    # Open/Create the HTML file for output
    with open("harvested_record_errors.html", 'a+') as infile:
        infile.seek(0)

        if len(infile.read(1)) == 0:
            lines = ['<html><head><title>FGP Harvester Errors</title></head><body><h1>FGP Harvester Errors</h1><p>Lastest errors appended to <a href="#bottom">bottom of page</a>. This page is updated everytime the harvester executes (~ every 5min).</p>']
        else:
            infile.seek(0)
            i = 0

            for line in infile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                lines.append(line)

                i += 1

    with open('harvested_record_errors.html', 'w+') as outfile:
        for line in lines:
            outfile.write(line)

        rownum = 0
        html = ''

        html += '<h4>' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '</h4>'
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
            outfile.write(html)

        outfile.write('<a name="bottom"/></body></html>')

    exit(0)
