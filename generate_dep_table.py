#!/usr/bin/env python3

import sys
from gather_metadata import gather_metadata
from tabulate import tabulate

sys.stdout.reconfigure(encoding='utf-8')

deps = gather_metadata()

table = [['Project', 'Creators']]
special_permissions = []
for project in deps:
    table.append([
        f"[{project['name']}]({project['url']})",
        ', '.join([f"[{member['name']}]({member['url']})" for member in project['members']])
    ])
    if permission_message := project.get('permission_message'):
        special_permissions.append(permission_message)

print(tabulate(table, headers="firstrow", tablefmt="github"))
print()
for permission_message in special_permissions:
    print(f'- {permission_message}')
