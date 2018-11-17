import util.timing

# Useful strings
latex_header = '''
\\documentclass{article}
\\usepackage[a4paper,margin=1.5cm]{geometry}
\\usepackage{microtype}
\\usepackage{multirow}
\\begin{document}
\\thispagestyle{empty}
'''

latex_table_start = '''
\\small
\\renewcommand{\\arraystretch}{4.2}
\\noindent\\begin{tabular}{|p{0.9cm}|p{2.9cm}|p{2.9cm}|p{2.9cm}|p{2.9cm}|p{2.9cm}|}
\\hline
\\textbf{Time} & Monday & Tuesday & Wednesday & Thursday & Friday \\\\
\\hline
'''

# Format timetable with escape codes, for command line
def format_escape(timetable, week=None):
    present_day, present_time = None, None
    if not week:
        week = util.timing.get_week(timetable["term_start"], timetable["term_end"])
        if week == -1:
            week = 1
        else:
            present_day, present_time = util.timing.get_day_time()

    ret = '\033[32mTIMETABLE FOR WEEK ' + str(week) + '\033[0m\n'
    ret += 'Time Monday       Tuesday      Wednesday    Thursday     Friday\n'

    for hour in range(9, 21):
        if hour == 9:
            ret += ' '
        ret += str(hour) + '00 '
        for day in range(1, 6):
            if day == present_day and hour == present_time:
                ret += '\033[34m\033[7m'
            cls = util.timing.extract_class(timetable, week, day, hour)
            if cls:
                ret += cls["course"] + ' ' + cls["type"][:3]
            else:
                ret += '. . . . . . '
            ret += ' \033[0m'
        ret += '\n'
    
    return ret

# Format timetable in HTML, for CGI script use
def format_html(timetable, week=None):
    present_day, present_time = None, None
    if not week:
        week = util.timing.get_week(timetable["term_start"], timetable["term_end"])
        if week == -1:
            week = 1
        else:
            present_day, present_time = util.timing.get_day_time()

    ret = '<h2>Timetable for week ' + str(week) + '</h2>\n'
    ret += '''
<table>
<tr><th>Time</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th>
'''
    
    for hour in range(9, 21):
        ret += '<tr><td>' + str(hour) + '00</td>'
        for day in range(1, 6):
            if day == present_day and hour == present_time:
                ret += '<td class=\'current\'>'
            else:
                ret += '<td>'
            cls = util.timing.extract_class(timetable, week, day, hour)
            if cls:
                ret += cls["course"] + ' ' + cls["type"][:3]
            ret += '</td>'
        ret += '</tr>\n'

    ret += '</table>\n'
    return ret

# Format timetable in LaTeX, for printing
def format_latex(timetable, week=None):
    if not week:
        week = util.timing.get_week(timetable["term_start"], timetable["term_end"])
        if week == -1:
            week = 1

    ret = latex_header
    ret += '\\begin{center}\\Large Timetable for Week ' + str(week) + '\\end{center}\n'
    ret += latex_table_start

    for hour in range(9, 21):
        ret += '  ' + str(hour) + '00 & '
        lines = list(range(1, 7))
        for day in range(1, 6):
            cls = util.timing.extract_class(timetable, week, day, hour)    
            if cls and cls["is_start"]:
                if cls["duration"] > 1:
                    ret += '\\multirow[t]{' + str(cls["duration"]) + '}{*}{'
                    lines.remove(day+1)
                ret += '\\shortstack[l]{\\textbf{' + cls["course"] + '} \\\\ ' + cls["type"] + ' \\\\ ' + cls["location"] + '}'
                if cls["duration"] > 1:
                    ret += '}'
            if day != 5:
                ret += '& '
        ret += ' \\\\ '
        for c in lines:
            ret += '\\cline{' + str(c) + '-' + str(c) + '}'
        ret += '\n'

    ret += '\\end{tabular}\n\\end{document}\n'
    return ret
