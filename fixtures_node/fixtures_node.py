import xml.etree.ElementTree as ET
import json
import unicodedata
import os
import roman

tree = ET.parse('../BrownDriverBriggs.xml')
root = tree.getroot()

heb = { x: [] for x in range(1, 24) }
ar = { y: [] for y in range(101, 124) }
roots = {**heb, **ar}

letters = []

title = [{
    'id': 'title',
    'section': 'title',
    'emory_page': 1,
    'next': f'/preface-{roman.toRoman(5).lower()}.html',
    'prev': '/'
}]
preface = [{
    'id': roman.toRoman(x).lower(),
    'section': 'preface',
    'emory_page': x - 2,
    'next': f'/preface-{roman.toRoman(x + 1).lower()}.html',
    'prev': f'/preface-{roman.toRoman(x - 1).lower()}.html',
    }
        for x in range(5, 13)]

abbrs = [{
    'id': roman.toRoman(x).lower(), 
    'section': 'abbr',
    'emory_page': x - 2,
    'next': f'/abbr-{roman.toRoman(x + 1).lower()}.html',
    'prev': f'/abbr-{roman.toRoman(x - 1).lower()}.html',
    }
        for x in range(13, 20)]

hebrew = []
aramaic = []

errata = [{
    'id': int(x),
    'section': 'errata',
    'emory_page': x + 18,
    'next': f'/errata-{x + 1}.html',
    'prev': f'/errata-{x - 1}.html',
    }
        for x in range(1119, 1128)]

current_page = 1
language = ''
letter = ''
key = 1

with open('letters.json', 'r') as letter_file:
    chars = json.load(letter_file)
    for l in chars:
        letter = {
    
            'id': l['id']
        }

        letter = { **letter, **l['fields'] }
        letter['char'] = unicodedata.normalize('NFC', letter['char'].strip())
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
    'id': current_page,
    'section': 'hebrew',
    'emory_page': 19,
    'next': '/hebrew-2.html',
    'prev': f'/abbr-{roman.toRoman(20).lower()}.html'
}

first_of_page = True
for el in root.iter():
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}page':
        if first_of_page == True:
            page['first_root'] = root['id']
        
        if current_page > 1077:
            page['section'] = 'aramaic'
            page['next'] = f'/aramaic-{current_page + 1}.html'
            page['prev'] = f'/aramaic-{current_page - 1}.html'
            aramaic.append(page)
        else:
            page['section'] = 'hebrew'
            page['next'] = f'/hebrew-{current_page + 1}.html'
            page['prev'] = f'/hebrew-{current_page - 1}.html'
            hebrew.append(page)
        
        current_page = int(el.attrib['p'])
        first_of_page = True
        page = {
            'id': current_page,
            'emory_page': current_page + 18,
        }
        
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}part':
        language = el.attrib['{http://www.w3.org/XML/1998/namespace}lang']
        letter = el.attrib['title']
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}entry':
        if 'type' in el.attrib and el.attrib['type'] == 'root':
            w = el.find('{http://openscriptures.github.com/morphhb/namespace}w')
            letter_id = get_letter_id(letter, language)
            root = { 
                'id': key,
                'root': w.text,
                'letter': letter_id,
                'page': current_page
            }
            roots[letter_id].append(root)
            if first_of_page == True:
                page['first_root'] = root['id']
                first_of_page == False

            key += 1
aramaic.append({
    'id': 1118,
    'section': 'aramaic',
    'prev': '/aramaic-1117.html',
    'emory_page': 1136,
})
# Link Sections
preface[0]['prev'] = '/'
preface[-1]['next'] = f'/abbr-{roman.toRoman(13).lower()}.html'
abbrs[0]['prev'] = f'/preface-{roman.toRoman(12).lower()}.html'
abbrs[-1]['next'] = f'/hebrew-1.html'
hebrew[0]['prev'] = f'/abbr-{roman.toRoman(19).lower()}.html'
hebrew[-1]['next'] = f'/aramaic-1078.html'
aramaic[0]['prev'] = f'/hebrew-1077.html'
aramaic[-1]['next'] = f'/errata1119.html'
errata[0]['prev'] = f'/aramaic-1118.html'
errata[-1]['next'] = '/'

os.makedirs(os.path.dirname('dist/'), exist_ok=True)
with open('dist/roots.json', 'w') as outfile:
    json.dump(roots, outfile, indent = 2, ensure_ascii=False)

with open('dist/pages.json', 'w') as outfile:
    json.dump(title + preface + abbrs + hebrew + aramaic + errata, outfile, indent = 2, ensure_ascii=False)

with open('dist/letters.json', 'w') as outfile:
    json.dump(letters, outfile, indent = 2, ensure_ascii=False)
