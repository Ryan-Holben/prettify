"""

pretty_helper.py

Contains all of the functions that do the actual analyzing and formatting of the lines of a text file.

"""

import re

def to_text(lines):
    """Re-joins the lines into a single newline-separated string."""
    return '\n'.join(lines)

def search_backwards(lines, i):
    """Search backwards until a blank line is found."""
    for j in range(i-1, -1, -1):
        if lines[j][1] == '':
            return j

def search_forwards(lines, i):
    """Search forwards until a blank line is found."""
    for k in range(i+1, len(lines), 1):
        if lines[k][1] == '':
            return k
    return k

def line_looks_like_code(line, code_symbol_ratio):
    """Sloppy.  We just check if the line is short and has symbols.  Should be followed up by checking if it is preceded and prepended by a blank line."""
    code_chars = ['#', '[', ']', '=', '==', '<', '>']
    count = 0
    if len(line) > 0:
        if line[-1] == '.' or '. ' in line:
            return False
        for match in code_chars:
            if match in line:
                count += 1
        if '(' in line: # Only count '(' if there is a matching ')'
            if ')' in line[line.index('(')+1:]:
                count += 1
        tempstr = ' '.join(line.split())
        if len(tempstr) == 0:
            return False
        else:
            ratio = 1.0 * count / len(tempstr)
            if ratio > code_symbol_ratio:
                return True
    return False

def line_starts_with_enumeration(line):
    try:
        # Check if the line begins with (#), #), or #.
        m = re.finditer('\(*\d+\)|\d+\.', line).next()
        if m.start(0) == 0:
            return m.end(0)
    except Exception as e:
        # Otherwise, nothing found
        pass
    return False

def find_headers(lines):
    """Identify headers and line breaks."""
    for i in range(len(lines)):
        if lines[i][1] == '-'*78:
            lines[i][0] = 'pagebreak'
            lines[i+2][0] = 'header'
        i += 3
    return lines

def find_code(lines, MAGIC_CODE_RATIO):
    """Identify code blocks in a limited fashion.  Does not identify inline code."""
    i = 0
    while i < len(lines):
        # If a line isn't 'text', then it's already been labeled as something else. Skip it.
        if lines[i][0] == 'text':
            # Most code blocks start with a function defintition.
            if lines[i][1][:4] == 'def ':
                # Occasionally there might be an import line or something similar prior to the 'def', so we look back until we find a blank line, as well as ahead to find the end.
                block_start = search_backwards(lines, i)
                block_end = search_forwards(lines, i)
                for j in range(block_start+2, block_end):
                    lines[j][0] = 'code'
                lines[block_start+1][0] = 'code-start'
                lines[block_end][0] = 'code-end'
                i = block_end + 1
            # Some don't!
            elif line_looks_like_code(lines[i][1], MAGIC_CODE_RATIO):
                if lines[i-1][0] in ['text', 'code-end'] and lines[i-1][1] == '':
                    block_end = search_forwards(lines, i)
                    if lines[i-1][0] == 'code-end':
                        lines[i-1][0] = 'code'
                        lines[i][0] = 'code'
                    else:
                        lines[i][0] = 'code-start'
                    lines[block_end][0] = 'code-end'
                    for j in range(i+1, block_end-1):
                        lines[j][0] = 'code'
                    i = block_end + 1
                else:
                    i += 1
            else:
                i += 1
        else:
            i += 1
    return lines

def find_lists(lines):
    """Identify all numbered lists."""
    i = 0
    while i < len(lines): #i in range(len(lines)):
        # If a line isn't 'text', then it's already been labeled as something else. Skip it.
        if lines[i][0] == 'text':
            k = line_starts_with_enumeration(lines[i][1])
            if k:
                # Let's keep track of each line # where a list item occurs, and where in that line the numbering ends (and thus where the actual content of the line begins)
                list_items = [(i, k)]
                # If we're in this list block, we're within a list.
                # We'll assume our code is perfect, and not search backwards for previous list items-- our perfect code surely has already found them!
                # However, we should search forwards.  Key info: Dr. Pattis' list items are separated by blank lines.
                j = i
                while j < len(lines):
                    # Find the next blank line, and look at the line which follows it
                    j = search_forwards(lines, j)
                    # Have we found another list item?
                    k = line_starts_with_enumeration(lines[j+1][1])
                    if k:
                        list_items.append((j+1, k))  # The list continues
                    else:
                        break   # The list terminated
                for k in range(i+1, j):
                    lines[k][0] = 'list'
                for item in list_items:
                    # Label the items, and remove the original numbering (Markdown will supply its own numbering)
                    lines[item[0]][0] = 'list-item'
                    lines[item[0]][1] = lines[item[0]][1][item[1]:]
                i = j + 1
            else:
                i += 1
        else:
            i += 1
    return lines

def find_diagrams(lines):
    """Identify all diagrams."""
    i = 0
    while i < len(lines):
        # If a line isn't 'text', then it's already been labeled as something else. Skip it.
        if lines[i][0] == 'text':
            # Assume diagram lines usually start with a tab.
            if lines[i][1][0:2] == '  ':
                # Search forward for a blank line.
                break_flag = False
                block_end = search_forwards(lines, i)
                if block_end == i+1:
                    break_flag = True
                # for k in range(i, block_end):
                #     if lines[k][0] != 'text':
                #         i = block_end+1
                if not break_flag:
                    for j in range(i+1, block_end-1):
                        lines[j][0] = 'diagram'
                    lines[i][0] = 'diagram-start'
                    lines[block_end-1][0] = 'diagram-end'
                i = block_end + 1
            else:
                i += 1
        else:
            i += 1
    return lines

def protect_special_chars(lines):
    """Add \ in front of * or _ so that Markdown doesn't interpret them."""
    for i in range(len(lines)):
        if lines[i][0] in ['text', 'list', 'list-item']:
            protectedline = []
            for c in lines[i][1]:
                if c in '_*':
                    protectedline.append('\\' + c)
                else:
                    protectedline.append(c)
            lines[i][1] = ''.join(protectedline)

    return lines

def apply_line_formatting(lines):
    """Here is where we apply Markdown formatting (and insert lines, as necessary), based on the line labels that we have created.  This should be called after all find_[foo]() functions have been applied."""
    i = 1
    lines[0][1] = '# <div align=center>' + lines[0][1] + '</div>'
    lines.insert(1, ['added', '***'])
    headers = []
    while i < len(lines):
        if lines[i][0] == 'text':
            pass
        elif lines[i][0] == 'pagebreak':
            lines[i][1] = '***'
        elif lines[i][0] == 'header':
            if lines[i][1][-1] == ':':  # Remove colons which occasionally appear at the end of headers
                lines[i][1] = lines[i][1][:-1]
            headers.append(lines[i][1])
            lines[i][1] = '## <a name=\"anchor-' + str(len(headers)) + '\"></a>' + headers[-1]
            lines.insert(i+1, ['added', '\[[top](#top)\]'])
            i += 1
        elif lines[i][0] == 'code-start':
            lines.insert(i, ['added', '```python'])
            i += 1
        elif lines[i][0] == 'code-end':
            lines.insert(i+1, ['added', '```'])
            i += 1
        elif lines[i][0] == 'list-item':
            lines[i][1] = '1. ' + lines[i][1]
        elif lines[i][0] in ['diagram', 'diagram-start', 'diagram-end']:
            lines[i][1] = '\t' + lines[i][1]
            pass
        i += 1

    # Build the table of contents using headers[]
    lines.insert(2, ['added', '## <a name=\"top\"></a> Table of Contents'])
    for n in range(len(headers)):
        lines.insert(3+n, ['added', '1.  [' + headers[n] + '](#anchor-' + str(n+1) + ')'])
    lines.insert(3+len(headers), ['added', '***'])

    return lines, headers
