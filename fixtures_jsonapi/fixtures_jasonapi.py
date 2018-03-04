import xml.etree.ElementTree as ET
import json
import unicodedata
import os

tree = ET.parse('../BrownDriverBriggs.xml')
root = tree.getroot()

roots = []
pages = []
letters = []

current_page = '1'
language = ''
letter = ''
key = 1

with open('../letters.json', 'r') as letter_file:
    chars = json.load(letter_file)
    for l in chars:
        letter = {
            'type': 'letter',
            'id': l['id'],
            'data': l['fields'],
            'relationships': {
                'roots':[]
            }
        }
        letter['data']['char'] = unicodedata.normalize('NFC', letter['data']['char'].strip())
        letters.append(letter)

def get_letter_id(letter, language):
    letter = unicodedata.normalize('NFC', letter)
    letter_id = ''
    if language == 'heb':
        scoped_letters = [x for x in chars if x['fields']['language'] == 'hebrew']
    elif language == 'arc':
        scoped_letters = [x for x in chars if x['fields']['language'] == 'aramaic']
    else:
        print("ERROR")

    for l in scoped_letters:
        if l['fields']['char'] == letter:
            letter_id = l['id']
            break
    
    return letter_id

page = {
    'type':'page',
    'id': int(current_page),
    'data': {
        'number': int(current_page)
    }
}
pages.append(page)

for el in root.iter():
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}page':
        current_page = el.attrib['p']
        page = {
            'type':'page',
            'id': int(current_page),
            'data': {
                'number': int(current_page)
            }
        }
        pages.append(page)
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}part':
        language = el.attrib['{http://www.w3.org/XML/1998/namespace}lang']
        letter = el.attrib['title']
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}entry':
        if 'type' in el.attrib and el.attrib['type'] == 'root':
            w = el.find('{http://openscriptures.github.com/morphhb/namespace}w')
            letter_id = get_letter_id(letter, language)
            root = { 
                'type': 'root',
                'id': key,
                'data': {
                    'root': w.text,
                },
                'relationships': {
                    'letter':{
                        'data': { 'type':'letter' ,'id': letter_id }
                    },
                    'page':{
                        'data': { 'type':'page', 'id': current_page }
                    }
                }
            }
            roots.append(root)

            

            key += 1
            
os.makedirs(os.path.dirname('dist/roots/'), exist_ok=True)
with open('dist/roots/index.json', 'w') as outfile:
    json.dump(roots, outfile, indent = 2, ensure_ascii=False)

for root in roots:
    filename = f"dist/roots/{root['id']}/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as outfile:
        json.dump(root, outfile, indent = 2, ensure_ascii=False)

os.makedirs(os.path.dirname('dist/pages/'), exist_ok=True)
with open('dist/pages/index.json', 'w') as outfile:
    json.dump(pages, outfile, indent = 2, ensure_ascii=False)

for page in pages:
    filename = f"dist/pages/{page['id']}/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as outfile:
        json.dump(page, outfile, indent = 2, ensure_ascii=False)

for letter in letters:
    rs = [r for r in roots if r['relationships']['letter']['data']['id'] == letter['id']]

    for r in rs:
        rt = {
            'type': r['type'],
            'id': r['id']
        }
        letter['relationships']['roots'].append(rt)
    
    filename = f"dist/letters/{letter['id']}/index.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as outfile:
        json.dump(letter, outfile, indent = 2, ensure_ascii=False)

letters_full = {
    'data': letters,
    'included': roots
}
with open('dist/letters/index.json', 'w') as outfile:
    json.dump(letters, outfile, indent = 2, ensure_ascii=False)
