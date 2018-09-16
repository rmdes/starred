#!/usr/bin/env python3

import argparse
import sys

import jinja2
import markdown
import re

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <link href="https://azlux.fr/bootstrap-combined.min.css" rel="stylesheet">
    <meta http-equiv="cache-control" content="max-age=0" />
    <meta http-equiv="cache-control" content="no-cache" />
    <meta http-equiv="expires" content="0" />
    <meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />
    <meta http-equiv="pragma" content="no-cache" />

    <style>
        body {
            font-family: sans-serif;
            background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%);
            color: #dadada;
        }
        code, pre {
            font-family: monospace;
        }
        h1 code,
        h2 code,
        h3 code,
        h4 code,
        h5 code,
        h6 code {
            font-size: inherit;
        }
    </style>
</head>
<body>
<div class="container">
{{content}}
</div>
</body>
</html>
"""

def upper_repl(match):
    return '<h2 id="' + match.group(1).lower().replace(' ','-') +'">' +  match.group(1) + '</h2>'

def parse_args(args=None):
    d = 'Make a complete, styled HTML document from a Markdown file.'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('mdfile', type=argparse.FileType('r'), nargs='?',
                        default=sys.stdin,
                        help='File to convert. Defaults to stdin.')
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output file name. Defaults to stdout.')
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    md = args.mdfile.read()
    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    doc = jinja2.Template(TEMPLATE).render(content=html)
    doc = re.sub(r'<h2>(.*)</h2>', upper_repl ,doc, flags=re.IGNORECASE)
    doc = doc.replace('http://','https://')
    args.out.write(doc)


if __name__ == '__main__':
    sys.exit(main())
