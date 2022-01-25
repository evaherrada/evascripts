from subprocess import check_output
import os


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
branch = "main"

# Sets the commit message to use
commit_message = "Updated docs link, updated python docs link, updated setup.py"

# Variables to turn on and off various parts of the patch script
patch = True
commit = False
push = False

# Verifies that patching was intended to be enabled
if patch:
    if input(f"Patching is enabled. Confirm: ").lower() not in ("y", "yes"):
        print("Cancelled")
        exit(1)
else:
    print("Patching is disabled")

# Verifies that committing was intended to be enabled
if commit:
    if input(
        f"Commit message: {commit_message}\nCommitting is enabled. Confirm: "
    ).lower() not in ("y", "yes"):
        print("Cancelled")
        exit(1)
else:
    print("Committing is disabled")

# Verifies that pushing was intended to be enabled
if push:
    if input(f"Branch: {branch}\nPushing is enabled. Confirm: ").lower() not in (
        "y",
        "yes",
    ):
        print("Cancelled")
        exit(1)
    if input(f"Are you sure?: ").lower() not in ("y", "yes"):
        print("Canceled")
        exit(1)
else:
    print("Pushing is disabled")

# Confirms options of what is enabled and disabled
if input(
    f"Patch: {patch}, Commit: {commit}, Push: {push}\nIs this all correct? "
).lower() not in ("y", "yes"):
    print("Cancelled")
    exit(1)

# Allows you to run patch on first X number of libraries
num = input("How many would you like to run? (leave blank for all): ")
if len(num):
    num = int(num)
else:
    num = None

i = 0
for repo in dirlist:
    loc = "/home/dherrada/adafruit/patch/repos/{}/".format(repo)
    os.chdir(loc)
    print("https://github.com/adafruit/{}".format(repo))
    if patch:
        # Ensures that the local version is up to date
        os.system("git pull")
        os.system(f"git checkout -b {branch}")

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
    if commit:
        os.system("git add .")
        os.system(f'git commit -m "{commit_message}"')

    # Pushes the patch
    if push:
        # Uncomment all lines below and comment out line directly below if you're pushing to
        # Anything other than main/default branch
        os.system("git push")
        # os.system(f'git push -u origin {branch}')
        os.system("cd ..")
        # os.system('google-chrome https://github.com/adafruit/{repo}/compare/main...adafruit:manual-patch?expand=1')
        # if input('Continue? ').lower in ('n', 'no'):
        #    break
        os.system(f"rm -rf {loc}")

    # Checks to make sure max number of runs hasn't been exceeded
    i += 1
    if i == num:
        break

os.chdir("/home/dherrada/adafruit/patch/")
