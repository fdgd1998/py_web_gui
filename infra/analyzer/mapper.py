import os
import shutil
import sys
import json

# Move student code and test case to the container
shutil.move('/usr/testhost/resources/', './resources')
os.chmod('./resources', 0o777)

os.rename('/usr/testhost/wrapper.py', './wrapper.py')
os.chmod('./wrapper.py', 0o777)

os.rename('/usr/testhost/cases/' + os.environ['ITEM'] + '.in', './input')
os.environ['ITEM'] = '0'
os.environ['ITEMS'] = '0'
os.chmod('./input', 0o777)

os.rename('./code.py', './[[ module_name ]].py')
os.chmod('./[[ module_name ]].py', 0o777)

os.setgid(65534)
os.setuid(65534)
sys.path.insert(0, os.getcwd())

# DO NOT MOVE THE IMPORT STATEMENT TO THE TOP OF THE FILE!
import wrapper

# Read inputs
d = None
with open('input', 'r') as f:
    d = json.loads(f.read())

# Run test
r = wrapper.run_test(d)

# Save result
with open('output', 'w') as f:
    json.dump(r, f)
