import unittest, inspect
from dataactcore.models.baseInterface import BaseInterface
from dataactvalidator.interfaces.interfaceHolder import InterfaceHolder
from jobTests import JobTests
from validatorTests import ValidatorTests
from fileTypeTests import FileTypeTests
import cProfile
import pstats

def runTests():
    runMany = False # True to run the test suite multiple times

    # Connect to databases
    BaseInterface.IS_FLASK = False # Tests are not running within a flask app
    interfaces = InterfaceHolder()

    # Create test suite
    suite = unittest.TestSuite()

    # Get lists of method names
    validatorMethods = ValidatorTests.__dict__.keys()
    jobMethods = JobTests.__dict__.keys()

    #validatorMethods = []
    #jobMethods = ["test_rules"]

    for method in validatorMethods:
        # If test method, add to suite
        if(str(method[0:4]) == "test"):
            test =ValidatorTests(methodName=method)
            suite.addTest(test)

    for method in jobMethods:
        # If test method, add to suite
        if(method[0:4] == "test"):
            test =JobTests(methodName=method,interfaces=interfaces)
            suite.addTest(test)



    #print(str(suite.countTestCases()) + " tests in suite")

    # Run tests and store results
    runner = unittest.TextTestRunner(verbosity=2)
    if(runMany):
        for i in range(0,100):
            result = runner.run(suite)
            if(len(result.errors) > 0 or len(result.failures) > 0):
                raise Exception("Test Failed")
    else:
        result = runner.run(suite)

    fileSuite = unittest.TestSuite()
    fileMethods = FileTypeTests.__dict__.keys()
    #fileMethods = []

    for method in fileMethods:
        # If test method, add to suite
        if(method[0:4] == "test"):
            test =FileTypeTests(methodName=method,interfaces=interfaces)
            fileSuite.addTest(test)

    fileResult = runner.run(fileSuite)
    interfaces.close()

if __name__ == '__main__':
    runTests()
    #cProfile.run("runTests()","stats")
    #stats = pstats.Stats("stats")
    #stats.sort_stats("cumulative").print_stats(100)