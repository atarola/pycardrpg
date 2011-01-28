#!/usr/bin/env python

import os
import sys
import re
import unittest

#
# Run all the unit tests in one shot
#

def create_suite():
    suites = []
    
    for test in find_files(os.path.dirname(os.path.abspath(__file__))):
        if not test.endswith("_test"):
            continue
        
        path, target = os.path.split(test)
        path = re.sub('[\\|/]', ".", path)
        
        __import__(path, globals(), locals(), [target])
        module = sys.modules[path + "." + target]
        
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        suites.append(suite)
        
    suite = unittest.TestSuite()
    suite.addTests(suites)
    return suite

def find_files(dirname, prefix=''):
    tests = []
    
    for fname in os.listdir(dirname):
        filename = os.path.join(dirname, fname)
        if os.path.isfile(filename) and re.match('^[^_]{1,1}.*\.py$', fname):
            tests.append(prefix + fname[:-3])
        elif os.path.isdir(filename):
            tests.extend(find_files(filename, prefix=prefix+fname+'/'))
            
    return tests

if __name__ == "__main__":
    suite = create_suite()
    runner = unittest.TextTestRunner()
    runner.run(suite)

