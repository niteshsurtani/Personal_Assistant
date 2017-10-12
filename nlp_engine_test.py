import os,unittest


modules_to_test=[]

for root, dirnames, filenames in os.walk('.'):
    for filename in filenames:
        if filename.startswith('test_') and filename.endswith('.py'):
            filename = filename[0:len(filename) - 3]
            module_file = os.path.join(root,filename)
            module_file = module_file[2:]
            modules_to_test.append(module_file)

print modules_to_test

# alltests = unittest.TestSuite()
# for module in map(__import__, modules_to_test):
#     alltests.addTest(unittest.findTestCases(module))
#     return alltests

# if __name__=='__main__':
#     MyTests=Tests()
#     unittest.main(defaultTest='MyTests.suite')

suites = [unittest.defaultTestLoader.loadTestsFromName('test_nlp_preprocessing_engine')]
# suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
#           in modules_to_test]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)

# suite = unittest.TestSuite()

# for t in modules_to_test:
#     try:
#         # If the module defines a suite() function, call it to get the suite.
#         mod = __import__(t, globals(), locals(), ['suite'])
#         suitefn = getattr(mod, 'suite')
#         suite.addTest(suitefn())
#     except (ImportError, AttributeError):
#         # else, just load all the test cases from the module.
#         suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

# unittest.TextTestRunner().run(suite)

