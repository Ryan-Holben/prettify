"""

pretty.py

Contains the main function pretty( ) which takes in the name of a raw text file, and outputs an HTML file.  Optionally, also outputs the MD file used, and also optionally a file which is useful for debugging.  Takes the parameter MAGIC_CODE_RATIO which can be tweaked to change how aggressively we detect code.

"""

from markdown import markdown
import pretty_helper as fmt

def pretty(filename, MAGIC_CODE_RATIO = 0.05, write_md = False, debugging = False):
    """Reads in a text file, writes an .html file and a .md file.

    Note: MAGIC_CODE_RATIO is the % of characters in a line that are allowed to be 'special' (such as parenthesis, brackets, etc.) before we suspect that line is part of a code block.  This is fairly hacky.  May want to adjust it on a per-file basis until you get the behavior you want."""

    with open(filename, 'rb') as textfile:
        lines = textfile.read().split('\r\n')    # Split into lines, trim away newlines
        # Temporarily label each line as one containing text.
        # Later we'll change some lines' labels to be things such as:
        #   ['text', 'header', 'pagebreak' 'code', 'code-start', ... ]
        # This isn't terribly efficient, but it should make for more manageable code.
        lines = [['text', l] for l in lines]


    # Search for special lines and label them
    lines = fmt.find_headers(lines)
    lines = fmt.find_lists(lines)
    lines = fmt.find_code(lines, MAGIC_CODE_RATIO)
    lines = fmt.find_diagrams(lines)

    # Protect _ and *, otherwise Markdown will interpret them as italics or boldface
    lines = fmt.protect_special_chars(lines)

    # Finally, actually do the formatting, based on the labels we applied above.
    lines, headers = fmt.apply_line_formatting(lines)

    # CSS files for overall prettiness, as well as syntax highlighting for code.
    # For code highlighting use either codehilite.css, codehilitepastie.css (light themes) or codehilitezenburn.css (dark theme).
    css = """<head>\n<link rel="stylesheet" href="css/rpoole.css">
<link rel="stylesheet" href="css/rhyde.css">
<link id="syntaxhighlightingCSS" rel="stylesheet" href="css/codehilitepastie.css">"""

    # Include a script to let the user swap between light and dark code syntax highlighting.
    # If this feels like overkill, simply omit the fancy_syntax_highlighting string when the "html" variable is defined below
    fancy_syntax_highlighting = """\n
<script>
function swapCSS(sheet){
	document.getElementById('syntaxhighlightingCSS').setAttribute('href', sheet);
}
</script>
</head>\n
<body>
<div id="syntaxbuttons" align=center style="position:fixed; bottom:10; right:10;">
Syntax<br>
<button onclick="swapCSS('css/codehilitepastie.css')">Light</button>
<button onclick="swapCSS('css/codehilitezenburn.css')">Dark</button>
</div>\n
    """

    # Combine the lines into a single string of Markdown (with bits of HTML)
    md = fmt.to_text([l[1] for l in lines])

    # Create an HTML file by rendering Markdown to HTML, and prepending the result with our CSS references.  Includes calls for code highlighting (fenced code is required for this).
    html = css + fancy_syntax_highlighting + markdown(md, smart_emphasis = False, extensions = ['fenced_code', 'codehilite'], ouput_format = 'html5') + '\n</html>'

    filename = filename[:-4]    # Remove the "".txt"

    # Write the .html file
    with open(filename+'.html', 'wb') as htmlfile:
        # htmlfile.write(markdown(text, smart_emphasis = False))
        htmlfile.write(html)

    # Write the .md file (optional)
    if write_md:
        with open(filename+'.md', 'wb') as mdfile:
            # mdfile.write(md)
            mdfile.write(md)

    # Debugging mode: write the .md file with each line prepended with the label our script decided upon.
    if debugging:
        with open(filename+'-debug.md', 'wb') as debugfile:
            # mdfile.write(md)
            for l in lines:
                debugfile.write(l[0] + ' - ' + l[1] + '\n')

    # We return the headers created for this document.  This can be used to create a table of contents.
    return headers
