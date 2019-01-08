#!/usr/bin/env python
# -*- coding: utf-8 -*-

min_python_version = (3, 6)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
if sys.version_info < min_python_version:
    print(f"error: python version {min_python_version} is required")
    sys.exit()

import os, io, re, zipfile
from collections import defaultdict
import xml.etree.ElementTree as etree

CSS_RULE_RE = re.compile(r'([\._\-0-9a-zA-Z]+)\s*{([^}]+)}')

def XHTML(name):
    return f"{{http://www.w3.org/1999/xhtml}}{name}"

def NAME(xmlns_name):
    if xmlns_name.startswith('{http://www.w3.org/1999/xhtml}'):
        return xmlns_name[30:]
    else:
        return xmlns_name

def utf8_zip_content(zip, filepath):
    with zip.open(filepath) as rf:
        return rf.read().decode('utf-8')

def read_css(content):
    css = {}
    for match in CSS_RULE_RE.findall(content):
        name = match[0]
        if name in css:
            print(f"warning: css rule conflict on name {name}")
        css[name] = defaultdict(str)
        for x in match[1].split(';'):
            y = [y.strip() for y in x.split(':')]
            if len(y) > 1:
                css[name][y[0]] = ''.join(y[1:])
    return css

def css_combine(css, classes):
    r = defaultdict(str)
    for c in classes:
        if c in css:
            r.update(css[c])
        if 'note-de-bas-de-page' in c:
            r['footnote'] = True
    return r

def css_apply(css, s):
    #TODO: {{{ intertitre, <quote></quote>
    if css['footnote']:
        return f"[[{s}]]"
    if css['text-transform'] == 'uppercase':
        s = s.upper()
    if css['font-style'] == 'italic':
        s = f"{{ {s} }}"
    if css['font-weight'] in ['bold', 'bolder']:
        s = f"{{{{ {s} }}}}"
    if css['text-decoration'] == 'line-through':
        s = f"<del>{s}</del>"
    if css['font-size'].endswith('em'):
        if float(css['font-size'][:-2]) > 1:
            s = f"{{{{{{ {s} }}}}}}"
    return s

def normalize_spaces(s):
    s = re.sub(r'\n', '<br/>', s)
    s = re.sub(r'\s+', ' ', s) # Suppression des espaces multiples
    s = re.sub(r'\s*~+\s*', '~', s) # Suppression des espaces avant/après l'espace insécable
    s = re.sub(r'[~\s]*<br\s*/>[\s~]*', '\n', s)
    s = re.sub(r'}+\n{+', '', s)
    s = re.sub(r'[^}]}}}{{{[^}]', '', s)
    s = re.sub(r'[^}]}}{{[^{]', '', s)
    s = re.sub(r'[^}]}{[^{]', '', s)
    return s

def normalize_ponctuation(s):
    s = re.sub(r'([nN])°', '\\1°~',  s) # Placement d'un espace insécable après n°, N°
    s = re.sub(r'[\s\(]p\.', 'p.~', s) # Placement d'un espace insécable après p.
    s = re.sub(r'([\(\'])\s+', '\\1', s) # Suppression espace après apostrophe, parenthèse ouvrante
    s = re.sub(r'\s+([\)\.,])', '\\1', s) # Suppression espace avant parenthèse fermante, point, virgule
    s = re.sub('([€%«])', '~\\1', s) # Placement d'un espace insécable avant les signes €, % et les guillemets ouvrants
    s = re.sub(r'([?!;:»])', '~\\1', s) # Insertion d'un espace insécable devant les ponctuations doubles et les guillemets fermants
    s = re.sub(r'\s*~+\s*', '~', s) # Suppression des espaces avant/après l'espace insécable inséré par les traitements précédents
    s = re.sub(' - ', ' – ', s) # Espace+trait d'union+espace remplacé par espace+demi-cadratin+espace
    s = re.sub(r' -,', ' –,', s) # Espace+trait d'union+virgule remplacé par espace+demi-cadratin+virgule
    return s

def normalize_urls(s):
    s = re.sub(r'http~:', 'http:', s)
    s = re.sub(r'\.php~\?', '.php?', s)
    s = re.sub(r'\.php3~\?', '.php3?', s)
    s = re.sub(r'\.asp~\?', '.asp?', s)
    s = re.sub(r'\.aspx~\?', '.aspx?', s)
    s = re.sub(r'\.cgi~\?', '.cgi?', s)
    s = re.sub(r'\.ns~\?', '.ns?', s)
    s = re.sub(r'\.search~\?', '.search?', s)
    s = re.sub(r'\.jhtml~\?', '.jhtml?', s)
    s = re.sub(r'\.cfm~\?', '.cfm?', s)
    s = re.sub(r'\.do~\?', '.do?', s)
    return s

def parse_text(node):
    texts = []
    for child in node:
        texts.append(parse_text(child))
    if node.text:
        texts.append(node.text)
    return ''.join(texts)

def parse_node(node, css, classes):
    texts = []
    style = css_combine(css, classes)
    for child in node:
        tag = NAME(child.tag)
        if tag == 'a':
            if 'href' in child.attrib:
                text = parse_text(child)
                link = child.attrib['href']
                texts.append(f"[{text}->{link}]")
        else:
            if 'class' in child.attrib:
                texts.append(parse_node(child, css, classes + [f"{tag}.{c}" for c in child.attrib['class'].split()]))
            else:
                texts.append(parse_node(child, css, classes))
            if tag == 'p':
                texts.append('\n')
    if node.text:
        texts.append(css_apply(style, node.text))
    return ''.join(texts)

def xhtml2spip(content, css):
    parser = etree.XMLParser()
    parser.entity['nbsp'] = '~'

    root = etree.XML(content, parser)
    content = parse_node(root.find(XHTML('body')), css, [])
    content = normalize_spaces(content)
    content = normalize_ponctuation(content)
    content = normalize_urls(content)
    return content

def epub2spip(epub_file, output_dir):
    if not os.path.exists(epub_file):
        print(f"error: {epub_file} does not exist")
        return
    epub_name = os.path.basename(epub_file)[:-5]
    with zipfile.ZipFile(epub_file) as zip:
        zip_files = zip.namelist()
        oebps_files = [f for f in zip_files if f.startswith('OEBPS')]
        css_templates = [f for f in oebps_files if f.endswith('.css')]
        xhtml_files = [f for f in oebps_files if f.endswith('.xhtml')]

        if len(css_templates) != 1:
            print("error: no CSS template found")
            return 0

        print(f"CSS template: {css_templates[0]}")
        css = read_css(utf8_zip_content(zip, css_templates[0]))

        for f in xhtml_files:
            output_name = os.path.basename(f)[:-6]
            output_file = f"{output_dir}/{epub_name}.{output_name}.txt"
            print(f"article: {f} -> {output_file}")
            xhtml = utf8_zip_content(zip, f)
            with open(output_file, 'w', encoding='utf-8') as wh:
                wh.write(xhtml2spip(xhtml, css))

def argparse_filepath(filepath):
    if not os.path.exists(filepath):
        raise argparse.ArgumentTypeError(f"{filepath} does not exist")
    return filepath
                
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', help='epub file to be converted to spip', type=argparse_filepath)
    parser.add_argument('-o', '--output-dir', help="output directory", metavar='DIR')
    args = parser.parse_args()

    if args.output_dir:
        try:
            if not os.path.exists(args.output_dir):
                os.mkdir(args.output_dir)
        except FileExistsError:
            print(f"error: impossible to create {args.output_dir} directory")
            sys.exit()
    else:
        args.output_dir = os.path.dirname(args.FILE)
        if not args.output_dir:
            args.output_dir = '.'

    epub2spip(args.FILE, args.output_dir)
