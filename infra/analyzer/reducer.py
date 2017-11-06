import glob
import json
import os
import sys

F = [ f for f in os.listdir('/usr/testguest') if True ]
print >> sys.stderr, "FILES GENERATED: " + str(F)

cases = sorted([f[:-3] for f in os.listdir('./cases') if os.path.isfile("./cases/%s"%f) and f.endswith(".in")])
cases.sort(key=int)

import verifier
wins = 0

# FOR EACH TEST CASE
for case in cases:
    r = None
    g = None
    d = None

    output_file = "/usr/testguest/%s.out" % case
    golden_file = "cases/%s.out" % case
    input_file = "cases/%s.in" % case

    print "-----------------"
    print "Test %s.in" % case

    # Print all files produced by mapper to staff log
    print >> sys.stderr, "TEST CASE :" + case
    with open('/usr/testguest/' + case + '.stdout', 'r') as f:
        print >> sys.stderr, "STDOUT: " + f.read()
    with open('/usr/testguest/' + case + '.stderr', 'r') as f:
        print >> sys.stderr, "STDERR: " + f.read()
    with open('/usr/testguest/' + case + '.json', 'r') as f:
        print >> sys.stderr, "JSON: " + f.read()

    # Read inputs
    if os.path.isfile(output_file):
        with open(output_file, 'r') as f:
            r = json.loads(f.read())
    else:
        print("FAILED: Test \"" + case + ".out\" not produced by test program.")
        continue
    with open(golden_file, 'r') as f:
        g = json.loads(f.read())
    with open(input_file, 'r') as f:
        d = json.loads(f.read())

    print "Description: %s" % d["test"]

    # Verify test output
    ok, message = verifier.verify(r, d, g)

    wins += (1 if ok else 0)
    print (("OK" if ok else "FAILED") + ": Test \"" + case + ".in\"" + (message if message else ("\nyields:    " + str(result) + "\nexpecting: " + str(g))))

# Produce grades
print("Grade: " + str(wins) + "/" + str(len(cases)))
score = (wins * 1.0) / len(cases)
grades = { 'Auto-grader': score }

with open('output', 'w') as scores:
    scores.write(json.dumps(grades))
