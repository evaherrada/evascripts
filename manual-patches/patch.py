from subprocess import check_output
import os
import sys


# Saves list of currently downloaded libraries in case something is messed up halfway through
# a patch we can redownload the libraries that it hasn't been applied to yet
dirlist = (
    check_output("ls /home/dherrada/adafruit/patch/repos/", shell=1)
    .decode("utf-8")
    .split("\n")
)
dirlist.pop()
with open("repos1.txt", "w") as F:
    for d in dirlist:
        F.write(d + "\n")

# Sets the branch to push to
BRANCH = "main"

# Sets the commit message to use
COMMIT_MESSAGE = "Updated docs link, updated python docs link, updated setup.py"

# Variables to turn on and off various parts of the patch script
PATCH = True
COMMIT = False
PUSH = False

# Verifies that patching was intended to be enabled
if PATCH:
    if input("Patching is enabled. Confirm: ").lower() not in ("y", "yes"):
        print("Cancelled")
        sys.exit(1)
else:
    print("Patching is disabled")

# Verifies that committing was intended to be enabled
if COMMIT:
    if input(
        f"Commit message: {COMMIT_MESSAGE}\nCommitting is enabled. Confirm: "
    ).lower() not in ("y", "yes"):
        print("Cancelled")
        sys.exit(1)
else:
    print("Committing is disabled")

# Verifies that pushing was intended to be enabled
if PUSH:
    if input(f"Branch: {BRANCH}\nPushing is enabled. Confirm: ").lower() not in (
        "y",
        "yes",
    ):
        print("Cancelled")
        sys.exit(1)
    if input("Are you sure?: ").lower() not in ("y", "yes"):
        print("Canceled")
        sys.exit(1)
else:
    print("Pushing is disabled")

# Confirms options of what is enabled and disabled
if input(
    f"Patch: {PATCH}, Commit: {COMMIT}, Push: {PUSH}\nIs this all correct? "
).lower() not in ("y", "yes"):
    print("Cancelled")
    sys.exit(1)

# Allows you to run patch on first X number of libraries
NUM = input("How many would you like to run? (leave blank for all): ")
if len(NUM):
    NUM = int(NUM)
else:
    NUM = None

i = 0
for repo in dirlist:
    loc = f"/home/dherrada/adafruit/patch/repos/{repo}/"
    os.chdir(loc)
    print(f"https://github.com/adafruit/{repo}")
    if PATCH:
        # Ensures that the local version is up to date
        os.system("git pull")
        os.system(f"git checkout -b {BRANCH}")

        # Actual patch
        os.system(
            "sed -i 's/circuitpython.readthedocs.io/docs.circuitpython.org/' README.rst"
        )
        os.system(
            "sed -i 's/circuitpython.readthedocs.io/docs.circuitpython.org/' docs/conf.py"
        )
        os.system(
            "sed -i 's/circuitpython.readthedocs.io/docs.circuitpython.org/' docs/index.rst"
        )
        os.system(
            'sed -i \'s/("https:\\/\\/docs.python.org\\/3.4", None)/("https:\\/\\/docs.python.org\\/3", None)/\' docs/conf.py'
        )
        os.system("sed -i '/Programming Language :: Python :: 3.4/d' setup.py")
        os.system("sed -i '/Programming Language :: Python :: 3.5/d' setup.py")

    # Commits the patch
    if COMMIT:
        os.system("git add .")
        os.system(f'git commit -m "{COMMIT_MESSAGE}"')

    # Pushes the patch
    if PUSH:
        # Uncomment all lines below and comment out line directly below if you're pushing to
        # Anything other than main/default branch
        os.system("git push")
        # os.system(f'git push -u origin {BRANCH}')
        os.system("cd ..")
        # os.system('google-chrome https://github.com/adafruit/{repo}/compare/main...adafruit:manual-patch?expand=1')
        # if input('Continue? ').lower in ('n', 'no'):
        #    break
        os.system(f"rm -rf {loc}")

    # Checks to make sure max number of runs hasn't been exceeded
    i += 1
    if i == NUM:
        break

os.chdir("/home/dherrada/adafruit/patch/")
