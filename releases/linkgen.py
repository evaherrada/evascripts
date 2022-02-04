#!/usr/bin/env python3
import urllib.parse
import sys
import requests
import os

ignored_files = [
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "LICENSES/*",
    "*.license",
    "setup.py.disabled",
    ".github/workflows/build.yml",
    ".github/workflows/release.yml",
    ".pre-commit-config.yaml",
    ".pylintrc",
    ".gitignore",
    "CODE_OF_CONDUCT.md",
    "README.rst",
    "pyproject.toml",
]

repo_shortnames = []
with open("repositories.txt", "r") as F:
    total = len(F.readlines())

with open("repositories.txt", "r") as F:
    for i, line in enumerate(F.readlines()):
        i = i + 1
        lib_shortname = line[:-1].split("Adafruit_CircuitPython_")[1]
        lib_pypiname = lib_shortname.replace("_", "-").lower()

        gh_token = os.environ["GH_REPO_TOKEN"]

        r = requests.get(
            f"https://api.github.com/repos/adafruit/adafruit_circuitpython_{lib_shortname.lower()}/releases/latest",
            auth=("dherrada", gh_token),
        )

        current_tag = r.json()["tag_name"]
        split_tag = current_tag.split(".")
        release_tag = (
            split_tag[0] + "." + split_tag[1] + "." + str(int(split_tag[2]) + 1)
        )

        print(f"Latest release tag is: {current_tag}")
        print(f'The last release was created at: {r.json()["created_at"]}')

        r = requests.get(
            f"https://api.github.com/repos/adafruit/adafruit_circuitpython_{lib_shortname.lower()}/compare/{current_tag}...main",
            auth=("dherrada", gh_token),
        )

        json = r.json()
        commits = json["ahead_by"]
        # print(json["commits"])

        print(
                f"\033[0;31m{i}/{total} \033[0;35m{(i/total * 100):.2f}% \033[0;31mRepository: \033[1;35m{lib_shortname}\033[0;31m\tLast Tag: \033[1;35m{current_tag}\033[0;31m\tAhead by: \033[1;35m{commits}\033[0;31m\tNext tag: \033[1;35m{release_tag}\033[0;31m\tFiles Changed: \033[1;35m{len(json['files'])}\033[0m"
        )

        print(f"\033[4;33mCommits\033[0m")
        for i in json["commits"]:
            # print(i)
            print(i["commit"]["message"])

        print(f"\033[4;33mFiles\033[0m")
        for i in json["files"]:
            filename = i["filename"]
            if filename not in ignored_files:
                print(f'\033[1;31m{i["filename"]}\033[0m')
            else:
                print(f'\033[1;32m{i["filename"]}\033[0m')
        filled_template = f"""To use in CircuitPython, simply install the [Adafruit CircuitPython Bundle](https://circuitpython.org/libraries).

To use in CPython, `pip3 install adafruit-circuitpython-{lib_pypiname}`.

Read the [docs](http://circuitpython.readthedocs.io/projects/{lib_pypiname}/en/latest/) for info on how to use it."""

        form_dict = {
            "tag": release_tag,
            "body": filled_template,
            "title": "%s - Updated pylint version, linted" % release_tag,
        }

        qstring = urllib.parse.urlencode(form_dict)
        qstring = qstring.replace("&", "\\&")
        print("")

        os.system(
            f"google-chrome https://github.com/adafruit/Adafruit_CircuitPython_{lib_shortname}/releases/new?{qstring}"
        )
        print(
            f"google-chrome https://github.com/adafruit/Adafruit_CircuitPython_{lib_shortname}/releases/new?{qstring}"
        )
        os.system(
            f"google-chrome https://github.com/adafruit/Adafruit_CircuitPython_{lib_shortname}/compare/{current_tag}...main"
        )
        input()
