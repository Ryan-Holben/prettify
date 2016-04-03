# Prettify

This code attempts to format the notes for Dr. Richard Pattis' ICS-33 class into something colorful and more easily navigated.  Some links:
* [Course website](https://www.ics.uci.edu/~pattis/ICS-33/)
* [Weekly schedule, HW, notes](https://www.ics.uci.edu/~pattis/ICS-33/lectures.html)
* [Notes in .txt format](https://www.ics.uci.edu/~pattis/ICS-33/lectures/)
* [Brayan Gallardo's winning entry, with handy navigation](http://www.ics.uci.edu/~brgallar/index.html)

## How it works
This project is coded in Python.  The script does the following:
1. The text files are examined, and each line is labeled as code, diagram, list, etc.
1. Depending on the line designations, Markdown formatting is applied.
1. The Markdown is rendered to HTML, and some extra HTML bits are added so that we can use some nice CSS.

## Challenges, and why this is interesting
It turns out that it is easy for a human to recognize a diagram, a code block, or even inline code contained within a sentence, but programming this algorithmically can be quite a challenge!  Can you precisely state how you differentiate between code and natural language?  The solution here works often, but not always, and so there is always room for improvement.  

## The next steps
There are a number of places one could work next:
* Improve the code-recognition algorithms
* Improve the diagram-recognition algorithm
* Combine this code with the winning entry in the original contest to make a nice Table of Contents interface.

## Bugs
This script was developed using _recursion.txt_, and it works pretty well with it!  However, it has mixed results with other text files.  In particular, when applying the script to other files the following things may happen:
* Some diagrams are borked
* This error was found in _decoratorspackages.txt_:

> k = line_starts_with_enumeration(lines[j+1][1])

In short, the original notes are not completely consistent, so we must check against the files for some edge cases.  Overall it works well, however.
