import tomllib
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def gather_metadata():
    deps = []
    s = requests.Session()

    packwiz_files = Path().glob('**/*.pw.toml')
    for file in packwiz_files:
        with open(file, 'rb') as f:
            data = tomllib.load(f)
            project = {
                'name': data['name'],
                'permission_message': data.get('custom-metadata', {}).get('permission-message', None),
                'members': []
            }
            if 'modrinth' in data.get('update', {}):
                project['mod-id'] = data['update']['modrinth']['mod-id']
                project['url'] = f"https://modrinth.com/project/{data['update']['modrinth']['mod-id']}"
                members_data = s.get(f"https://api.modrinth.com/v2/project/{project['mod-id']}/members", timeout=30).json()
                for member in members_data:
                    project['members'].append({
                        'name': member['user']['username'],
                        'url': f"https://modrinth.com/user/{member['user']['id']}"
                    })
                if not members_data:
                    project_data = s.get(f"https://api.modrinth.com/v2/project/{project['mod-id']}").json()
                    if project_data['organization']:
                        organization_page = s.get(f"https://modrinth.com/organization/{project_data['organization']}").text
                        soup = BeautifulSoup(organization_page, 'html.parser')
                        if soup.title:
                            project['members'].append({
                                'name': soup.title.string,
                                'url': f"https://modrinth.com/organization/{project_data['organization']}",
                            })
            else:
                project['url'] = data['custom-metadata']['project-url']
                for creator in data['custom-metadata']['creators']:
                    project['members'].append({
                        'name': creator['creator-name'],
                        'url': creator['creator-url']
                    })
            deps.append(project)
    return deps