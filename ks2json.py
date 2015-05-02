import sys
import re

def parse(h1, h2, body):
    # Remove leading '#'
    h1[0] = h1[0][1:]
    h2[0] = h2[0][1:]

    chunk = {'data': [], 'header': {}}
    chunk['header']['id'] = h1[0]
    chunk['header']['???'] = h1[1]
    chunk['header']['aID_c'] = h1[2]
    chunk['header']['bID_c'] = h1[3]
    chunk['header']['direction'] = h1[4]
    chunk['header']['count'] = h1[5]
    chunk['header']['meanKs'] = h1[6]
    chunk['header']['meanKn'] = h1[7]
    
    # Until we figure out whats going on, we are just cutting some pieces out
    # here...
    h2.pop(26) # GEVO_LINK
    for element in body: 
        # ... and here
        element.pop(22) # Mystery field 2
        element.pop(10) # Mystery field 1
        obj = {}
        for i, key in enumerate(h2):
            obj[key] = element[i]
        chunk['data'].append(obj)

    return chunk

data = []
body = None
header1 = None
header2 = None
for i, line in enumerate(sys.stdin):
    
    # Skip the first 3 lines -- they explain the headers
    if i <= 2:
        continue

    if line[0] == '#':
        if body:
            data.append(parse(header1, header2, body))
        body = []
        if line[1].isdigit():
            header1 = line.strip().replace('||', '\t')
            header1 = header1.replace('  ', '\t').split('\t')
            header1 = [x.strip() for x in header1]
        else:
            header2 = line.strip().replace('||', '\t').split('\t')
        continue

    body.append(line.strip().replace('||', '\t').split('\t'))

data.append(parse(header1, header2, body))
    
#import pprint
#pp = pprint.PrettyPrinter()
#pp.pprint(data)
import json
print(json.dumps(data))
