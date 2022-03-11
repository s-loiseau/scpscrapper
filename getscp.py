#!/usr/bin/env python3

from bs4 import BeautifulSoup as bs
import requests
import sys
import random
import textwrap
import os

def wraptext():
    output = []
    start = False
    # skip last line << SCPXXX SCPXXX SCPXXX >>
    for p in paraf[:-1]:
        if not start:
            #if "Objet no" not in p.text:
            if "Description" not in p.text:
                continue
            else:
                start= True
                output += textwrap.wrap(p.text, width=80)
        else:
            output += textwrap.wrap(p.text, width=80)

    with open(f"""scp{scpid}.txt""",'w') as fh:
        fh.writelines('\n'.join(output))

def easytotts():
    start = False
    with open('totts.txt','w') as fh:
        # skip last line << SCPXXX SCPXXX SCPXXX >>
        for p in paraf[:-1]:
            if not start:
                #if "Objet no" not in p.text:
                if "Description" not in p.text:
                    continue
                else:
                    start= True
                    fh.write(p.text.replace('-',''))
            else:
                fh.write(p.text.replace('-',''))

scpid = "003"
scpid = random.randint(1,999)
scpid = str(scpid).zfill(3)
# read arg
if len(sys.argv) > 1:
    scpid=sys.argv[1]

print(scpid)
audio = False
if len(sys.argv) > 2:
    if sys.argv[2] == "-a":
        audio = True

rooturl = f"""http://fondationscp.wikidot.com/scp-{scpid}"""

data = requests.get(rooturl).content.decode('utf-8')
soup = bs(data, 'html.parser')
paraf = soup.find_all('p')


if audio:
    easytotts()
    os.system('cat totts.txt | gtts-cli -l fr - | mpv --speed=1.4 - ')

