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

with open('letters.json', 'r') as letter_file:
    chars = json.load(letter_file)
    for l in chars:
        letter = {
            'type': 'letter',
            'id': l['id'],
            'attributes': l['fields'],
            'roots':[]
        }
        letter['attributes']['char'] = unicodedata.normalize('NFC', letter['attributes']['char'].strip())
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
    'attributes': {
        'number': int(current_page)
    }
}

first_of_page = True
for el in root.iter():
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}page':
        if first_of_page == True:
            page['attributes']['first_root'] = root['id']
            
        pages.append(page)
        current_page = el.attrib['p']
        first_of_page = True
        page = {
            'type':'page',
            'id': int(current_page),
            'attributes': {
                'number': int(current_page)
            }
        }
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
                'attributes': {
                    'root': w.text,
                    'letter': letter_id,
                    'page': current_page
                }
            }
            roots.append(root)
            if first_of_page == True:
                page['attributes']['first_root'] = root['id']
                first_of_page == False

            key += 1
            
os.makedirs(os.path.dirname('dist/'), exist_ok=True)
with open('dist/roots.json', 'w') as outfile:
    json.dump(roots, outfile, indent = 2, ensure_ascii=False)

with open('dist/pages.json', 'w') as outfile:
    json.dump(pages, outfile, indent = 2, ensure_ascii=False)

for letter in letters:
    rs = [r for r in roots if r['attributes']['letter'] == letter['id']]
    letter['attributes']['roots'] = rs

with open('dist/letters.json', 'w') as outfile:
    json.dump({'data':letters}, outfile, indent = 2, ensure_ascii=False)
