# Prettify

This code attempts to format the notes for Dr. Richard Pattis' ICS-33 class into something colorful and more easily navigated.  The website for his course is found [here](https://www.ics.uci.edu/~pattis/ICS-33/), the weekly schedule with notes is found [here](https://www.ics.uci.edu/~pattis/ICS-33/), and the raw text files are found [here](https://www.ics.uci.edu/~pattis/ICS-33/lectures/).

## How it works
This project is coded in Python.  The script does the following:
* The text files are examined, and each line is labeled as code, diagram, list, etc.
* Depending on the line designations, Markdown formatting is applied.
* The Markdown is rendered to HTML, and some extra HTML bits are added so that we can use some nice CSS.

## Challenges, and why this is interesting
It turns out that it is easy for a human to recognize a diagram, a code block, and inline code within a sentence, but programming this algorithmically can be quite a challenge!  The solution here works often, but not always, and so there is always room for improvement.  

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
