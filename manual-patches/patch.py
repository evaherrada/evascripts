from subprocess import check_output
import os
import signal
import time


def storeData(F, db):
    # Stores data in db file
    dbfile = open(F, 'wb')
    pickle.dump(db, dbfile)
    dbfile.close()


def loadData(F):
    # Loads data from db file
    dbfile = open(F, 'rb')
    db = pickle.load(dbfile)
    return db

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        exit(1)
 
signal.signal(signal.SIGINT, handler)

dirlist = check_output('ls /home/dherrada/adafruit/patch/repos/', shell=1).decode('utf-8').split('\n')
dirlist.pop()
with open('repos1.txt', 'w') as F:
    for d in dirlist:
        F.write(d + '\n')

branch = 'main'

commit_message = "Updated docs link, updated python docs link, updated setup.py"

patch = False
commit = False
push = True

if patch:
    if input(f'Patching is enabled. Confirm: ').lower() not in ("y", "yes"): 
        print("Cancelled")
        exit(1)
else:
    print("Patching is disabled")

if commit:
    if input(f'Commit message: {commit_message}\nCommitting is enabled. Confirm: ').lower() not in ("y", "yes"): 
        print("Cancelled")
        exit(1)
else:
    print("Committing is disabled")

if push:
    if input(f'Branch: {branch}\nPushing is enabled. Confirm: ').lower() not in ("y", "yes"): 
        print("Cancelled")
        exit(1)
    if input(f'Are you sure?: ').lower() not in ("y", "yes"):
        print("Canceled")
        exit(1)
else:
    print("Pushing is disabled")

if input(f'Patch: {patch}, Commit: {commit}, Push: {push}\nIs this all correct? ').lower() not in ("y", "yes"):
    print("Cancelled")
    exit(1)

num = input("How many would you like to run? (leave blank for all): ")
if len(num):
    num = int(num)
else:
    num = None

i = 0
for repo in dirlist:
    loc = '/home/dherrada/adafruit/patch/repos/{}/'.format(repo)
    os.chdir(loc)
    print('https://github.com/adafruit/{}'.format(repo))
    if patch:
        os.system('git pull')
        os.system(f'git checkout -b {branch}')
        #os.system('git pull')

        os.system("sed -i 's/circuitpython.readthedocs.io/docs.circuitpython.org/' README.rst")
        os.system("sed -i 's/circuitpython.readthedocs.io/docs.circuitpython.org/' docs/conf.py")
        os.system("sed -i 's/circuitpython.readthedocs.io/docs.circuitpython.org/' docs/index.rst")
        os.system("sed -i 's/(\"https:\\/\\/docs.python.org\\/3.4\", None)/(\"https:\\/\\/docs.python.org\\/3\", None)/' docs/conf.py")
        os.system("sed -i '/Programming Language :: Python :: 3.4/d' setup.py")
        os.system("sed -i '/Programming Language :: Python :: 3.5/d' setup.py")

    if commit:
        os.system('git add .')
        os.system(f'git commit -m "{commit_message}"')

    if push:
        os.system('git push')
        #os.system(f'git push -u origin {branch}')
        os.system('cd ..')
        #os.system('google-chrome https://github.com/adafruit/{repo}/compare/main...adafruit:manual-patch?expand=1')
        """
        if input('Continue? ').lower in ('n', 'no'):
            break
        """
        os.system(f'rm -rf {loc}')
        

    i += 1
    if i == num:
        break

os.chdir('/home/dherrada/adafruit/patch/')
