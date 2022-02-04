import datetime
import inspect
import json

from adabot import pypi_requests as pypi
from adabot.lib import circuitpython_library_validators as cpy_vals
from adabot.lib import common_funcs
from adabot.lib.common_funcs import list_repos

default_validators = [
    vals[1]
    for vals in inspect.getmembers(cpy_vals.LibraryValidator)
    if vals[0].startswith("validate")
]
print(default_validators)
bundle_submodules = common_funcs.get_bundle_submodules()

latest_pylint = ""
pylint_info = pypi.get("/pypi/pylint/json")
if pylint_info and pylint_info.ok:
    latest_pylint = pylint_info.json()["info"]["version"]

validator = cpy_vals.LibraryValidator(
    default_validators,
    bundle_submodules,
    latest_pylint,
)

try:
    with open("repos.json", "r") as f:
        date = f.readline().rstrip()
except FileNotFoundError:
    date = ""

print(f"Last run: {date}")
if date != str(datetime.date.today()):
    with open("repos.json", "w") as f:
        print("Fetching Repos List")
        all_repos = list_repos()
        print("Got Repos List")
        f.write(str(datetime.date.today()) + "\n")
        f.write(json.dumps(all_repos))

with open("repos.json", "r") as f:
    all_repos = json.loads(f.read().split("\n")[1])

results = {}

for repo in all_repos:
    val = validator.validate_release_state(repo)
    if val and type(val[0]) == tuple:
        print(repo["name"])
        print(val)
        results[repo["name"]] = val[0]

f = open("adabot_run.txt", "w")
for i in results:
    f.write(i + "\n")
f.close
