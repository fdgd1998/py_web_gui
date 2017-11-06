#!/usr/bin/env python2.7

import os, json
import wrapper, verifier

# Enumerate files in ./cases
os.chdir('cases')
cases = sorted([f[:-3] for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".in")])
cases.sort(key=int)

errors = 0

for case in cases:
    d = None
    g = None

    print "-----------------"
    print "Test %s.in" % case

    # Read inputs
    with open(case+'.in', 'r') as f:
        d = json.loads(f.read().replace("\'", '"').replace("(", '[').replace(")", ']'))

    # Run test
    r = wrapper.run_test(d)

    # JSON-encode and decode the result to mimic sandboxed autograder
    try:
        r = json.loads(json.dumps(r))
    except:
        print "WARNING: your return value in this test uses an unsupported type! Stick to dictionaries, objects, arrays, strings, numbers, booleans, and null."

    # Read golden output
    with open(case+'.out', 'r') as f:
        g = json.loads(f.read().replace("\'", '"').replace("(", '[').replace(")", ']'))

    # Verify test output
    ok, message = verifier.verify(r, d, g)

    # Accounting and grading
    errors += 0 if ok else 1
    print (("OK" if ok else "FAILED") + ": Test \"" + case + ".in\" " + (message if message else (" yields \n" + str(result) + "\n, expecting \n" + str(g))))

print "--------------"

if errors == 0:
    print "Yay! Everything looks correct! Good work."
else:
    print "Oh no! " + str(errors) + " tests failed, so you aren't done yet."
