"""
 Script to convert Professor Richard Pattis' ICS-33 notes into a slightly more readable and/or colorful format.  This is accomplished by converting his text notes into Markdown, and then rendering that Markdown into HTML.  A few bits of raw HTML are also added, too.

 Project structure:
 - main.py - High level function calls
 - pretty.py - Contains the main script for "prettifying" one .txt file
 - pretty_helper.py - Contains all of the functions that do the real work

 Feel free to add and expand this script!  There are at least a few edge cases which it does not yet handle, such as more advanced detection of code blocks and inline code, and some diagrams.

"""

import os
import pretty

note_path = 'notes/'
toc = []
for filename in os.listdir(note_path):
    if filename.endswith(".txt"):
        path = note_path + filename
        print 'Formatting ' + path + ' ...'
        try:
            headers = pretty.pretty(note_path + filename, MAGIC_CODE_RATIO = 0.05, write_md = False, debugging = False)
            toc.append([filename, headers])
        except Exception as e:
            print '\tERROR:', e

print '\nFinished.  Resulting Table of Contents:\n'
for i in range(len(toc)):
    print i, toc[i][0]
    for j in range(len(toc[i][1])):
        print '\t', j, toc[i][1][j]
