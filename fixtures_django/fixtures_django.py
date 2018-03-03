import xml.etree.ElementTree as ET
import json
import unicodedata

tree = ET.parse('../BrownDriverBriggs.xml')
root = tree.getroot()

roots = []
pages = []

current_page = '1'
language = ''
letter = ''
key = 1

with open('letters.json', 'r') as letter_file:
    chars = json.load(letter_file)
    for l in chars:
        l['fields']['char'] = unicodedata.normalize('NFC', l['fields']['char'].strip())


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
            letter_id = l['pk']
            break
    
    return letter_id

page = {
    'model':'dictionary.page',
    'pk': int(current_page),
    'fields': {
        'number': int(current_page)
    }
}
pages.append(page)

for el in root.iter():
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}page':
        current_page = el.attrib['p']
        page = {
            'model':'dictionary.page',
            'pk': int(current_page),
            'fields': {
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
                'model': 'dictionary.root',
                'pk': key,
                'fields': {
                    'root': w.text,
                    'letter_id': letter_id,
                    'page_id': int(current_page)
                }
            }
            roots.append(root)
            key += 1
            

with open('roots.json', 'w') as outfile:
    json.dump(roots, outfile, indent = 2, ensure_ascii=False)

with open('pages.json', 'w') as outfile:
    json.dump(pages, outfile, indent = 2, ensure_ascii=False)

with open('letters.json', 'w') as outfile:
    json.dump(chars, outfile, indent = 2, ensure_ascii=False)

