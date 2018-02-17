import xml.etree.ElementTree as ET
import json

tree = ET.parse('BrownDriverBriggs.xml')
root = tree.getroot()

dictionary = []
current_page = '1'
language = ''
letter = ''

for el in root.iter():
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}page':
        current_page = el.attrib['p']
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}part':
        language = el.attrib['{http://www.w3.org/XML/1998/namespace}lang']
        letter = el.attrib['title']
    if el.tag == '{http://openscriptures.github.com/morphhb/namespace}entry':
        if 'type' in el.attrib and el.attrib['type'] == 'root':
            w = el.find('{http://openscriptures.github.com/morphhb/namespace}w')
            root = {
                'letter': letter,
                'lang': language,
                'word': w.text,
                'page': current_page
            }
            
            dictionary.append(root)


with open('roots.json', 'w') as outfile:
    json.dump(dictionary, outfile, indent = 2, ensure_ascii=False)