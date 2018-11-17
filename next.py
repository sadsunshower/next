#!/usr/bin/python3

import sys, json

import util.formatting
import util.timing

flags = ''
ttpath = '~/timetable.json'
selected_week = None

# Process command line arguments
for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-p':
        ttpath = sys.argv[i+1]
    elif sys.argv[i] == '-t':
        selected_week = int(sys.argv[i+1])
    elif sys.argv[i][0] == '-':
        flags = sys.argv[i][1:]

# Display help information, if requested
if '?' in flags: 
    print('''Nick\'s timetabler v2.0
Usage: next.py [-flhw?] [-p (file)] [-t (week)] 
Command line flags:
  ? : Show this help information and exit
  f : Get the directory for the current class
  l : Print timetable as LaTeX
  h : Print timetable as HTML
  w : Get the current week only
  p : Use the timetable file at the given path (defaults to ~/timetable.json)
  t : Give the timetable of a specific week (defaults to current week / week 1 if outside term)
No arguments will show the timetable in the terminal''')
    sys.exit(0)

# Load timetable object from JSON
timetable = None
with open(ttpath) as f:
    timetable = json.loads(f.read())

if 'f' in flags:
    week = util.timing.get_week(timetable["term_start"], timetable["term_end"])
    day, time = util.timing.get_day_time()

    cls = util.timing.extract_class(timetable, week, day, time)
    if not cls:
        # Default to home directory
        print('~')
    else:
        try:
            print(timetable["course_folders"][cls.course])
        except e:
            print('~')

    sys.exit(0)

if 'l' in flags:
    if selected_week:
        print(util.formatting.format_latex(timetable, selected_week))
    else:
        print(util.formatting.format_latex(timetable))
    sys.exit(0)

if 'h' in flags:
    if len(sys.argv) > 3:
        print(util.formatting.format_html(timetable, selected_week))
    else:
        print(util.formatting.format_html(timetable))
    sys.exit(0)

if 'w' in flags:
    try:
        week = util.timing.get_week(timetable["term_start"], timetable["term_end"])
        if week == -1:
            print('Not in term')
        else:
            print('Week ' + week)
    except e:
        print('Error getting week')
    sys.exit(0)

if selected_week:
    print(util.formatting.format_escape(timetable, selected_week))
else:
    print(util.formatting.format_escape(timetable))
