#!/usr/bin/env python3

from gather_metadata import gather_metadata
import os

creators = set()
if os.path.exists('credits.txt'):
    with open('credits.txt', 'r') as f:
        for line in f:
            creators.add(line.strip())

deps = gather_metadata()
for project in deps:
    for member in project['members']:
        creators.add(member['name'])

with open('credits.txt', 'w') as f:
    for creator in sorted(creators, key=str.casefold):
        f.write(creator + '\n')
