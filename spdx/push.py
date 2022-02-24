import os
import time

branches =['spdx-44', 'spdx-45',
           'spdx-46', 'spdx-47', 'spdx-48',
           'spdx-49', 'spdx-50', 'spdx-51',
           'spdx-52']

os.chdir('./Adafruit_Learning_System_Guides/')

for branch in branches:
    os.system(f"git checkout {branch}")
    os.system(f"git push -u origin {branch}")
    if branch == 'spdx-52':
        os.system(f'hub pull-request -m "Added SPDX to 19 more files - {branch}"')
    else:
        os.system(f'hub pull-request -m "Added SPDX to 30 more files - {branch}"')
    time.sleep(1800)
