import requests
from adabot.lib.common_funcs import list_repos
import json
import os
import sys
import datetime

file = ".github/workflows/build.yml"
text_1 = "Python 3.x"
text_2 = "setup-python@v2"
URL_TEMPLATE = "https://raw.githubusercontent.com/adafruit/{}/main/{}"
RELEASE_TEMPLATE = "https://api.github.com/repos/adafruit/{}/releases/latest"

RESULTS = {
    "file_not_found": [],
    "file_has_none": [],
    "file_has_text_1": [],
    "file_has_text_2": [],
    "file_has_both": [],
}

def delete_multiple_lines(n=1):
    """Delete the last line in the STDOUT."""
    for _ in range(n):
        sys.stdout.write("\x1b[1A")  # cursor up one line
        sys.stdout.write("\x1b[2K")  # delete the last line

try:
    with open('repos.json', 'r') as f:
        date = f.readline().rstrip()
except FileNotFoundError:
    date = ""

print(f"Last run: {date}")
if date != str(datetime.date.today()):
    with open("repos.json", "w") as f:
        print("Fetching Repos List")
        all_repos = list_repos()
        print("Got Repos List")
        f.write(str(datetime.date.today()) + '\n')
        f.write(json.dumps(all_repos))
    
with open("repos.json", "r") as f:
    all_repos = json.loads(f.read().split('\n')[1])

print(f"Repos found: {len(all_repos)}")

"""
for repo in all_repos:
    #print("getting {} for: {}".format(file, repo["name"]))
    response = requests.get(URL_TEMPLATE.format(repo["name"], file))
    release = requests.get(RELEASE_TEMPLATE.format(repo["name"]), auth=(os.environ.get("ADABOT_GITHUB_USER"),os.environ.get("GH_REPO_TOKEN")))
    if response.status_code != 404:
        RESULTS['file_not_found'].append(repo["html_url"])
        if release.status_code != 404:
            if "CPython" not in release.json()["body"]:
                print(f'https://github.com/adafruit/{repo["name"]}/releases/latest')
        #print("File not found")
    if release.status_code == 404:
        print("NO RELEASES")
    else:
        try:
            if "CPython" not in release.json()["body"] and response.status_code != 404:
                print(f'https://github.com/adafruit/{repo["name"]}/releases/latest')
        except:
            print(release.json())

"""
for repo in all_repos:
    getted = "getting {} for: {}".format(file, repo["name"])
    response = requests.get(URL_TEMPLATE.format(repo["name"], file))
    if response.status_code == 404:
        RESULTS['file_not_found'].append(repo["html_url"])
        result = "\033[91mFile not found\033[0m"
    else:
        if text_1 not in response.text and text_2 not in response.text:
            result = "\033[91mfound neither text\033[0m"
            RESULTS['file_has_none'].append(repo["html_url"])
        if text_1 in response.text and text_2 in response.text:
            result = "\033[92mfound both text\033[0m"
            RESULTS['file_has_both'].append(repo["html_url"])
        if text_1 in response.text and text_2 not in response.text:
            result = "\033[93mfound text 1\033[0m"
            RESULTS['file_has_text_1'].append(repo["html_url"])
        if text_1 not in response.text and text_2 in response.text:
            result = "\033[93mfound text 2\033[0m"
            RESULTS['file_has_text_2'].append(repo["html_url"])

    print("┌" + "─" * (len(getted) + 4) + "┐")
    print("│ ", getted, " │")
    print("│ ", result, " " * (len(getted) - (len(result) - 9)), "│")
    print("└" + "─" * (len(getted) + 4) + "┘")
    delete_multiple_lines(4)

print("┌" + "─" * 30 + "┐")
for k, v in RESULTS.items():
    print("│ ", k, len(v), " " * (24 - (len(k) + len(str(len(v))))),  " │")
print("└" + "─" * 30 + "┘")
f = open ("textfinder.json", "w")
F = open ("textfinder.txt", "w")

f.write(json.dumps(RESULTS))
for k, v in RESULTS.items():
    F.write('\n')
    F.write(k + '\n')
    for i in v:
        F.write(i + '\n')

f.close()
F.close()
