class TestCase:

    def __init__(self, testName):
        self.testName = testName

    def setUp(self):
        pass

    def run(self, result):
        self.setUp()
        result.testStarted()
        try:
            method = getattr(self, self.testName)
            method()
        except:
            result.testFailed()
        self.tearDown()

    def tearDown(self):
        pass

class WasRun(TestCase):

    def __init__(self, testName):
        self.log = ""
        TestCase.__init__(self, testName) 

    def setUp(self):
        self.log = self.log + "setUp "

    def testMethod(self):
        self.log = self.log + "testMethod "

    def testBroken(self):
        raise Exception 

    def tearDown(self):
        self.log = self.log + "tearDown"

class TestResult:

    def __init__(self):
        self.runCount = 0
        self.errorCount = 0
    
    def testStarted(self):
        self.runCount = self.runCount + 1

    def testFailed(self):
        self.errorCount = self.errorCount + 1

    def summary(self):
        return "%d run, %d failed" % (self.runCount, self.errorCount)

class TestSuite(TestCase):

    def __init__(self):
        self.tests = []

    def setUp(self):
        pass

    def add(self, test):
        self.tests.append(test)

    def run(self, result):
        for test in self.tests:
            test.run(result)

    def tearDown(self):
        pass

class TestCaseTest(TestCase):

    def __init__(self, testName):
        TestCase.__init__(self, testName) 

    def setUp(self):
        self.result = TestResult() 

    def testTemplateMethod(self):
        print "testTemplateMethod invoked"
        test = WasRun("testMethod")
        test.run(self.result)
        assert test.log == "setUp testMethod tearDown"

    def testResult(self):
        print "testResult invoked"
        test = WasRun("testMethod")
        test.run(self.result)
        assert self.result.summary() == "1 run, 0 failed"

    def testFailedResult(self):
        print "testFailedResult invoked"
        test = WasRun("testBroken")
        test.run(self.result)
        assert self.result.summary() == "1 run, 1 failed"
    
    def testResultFormatting(self):
        print "testResultFormatting invoked"
        self.result.testStarted()
        self.result.testFailed()
        assert self.result.summary() == "1 run, 1 failed"

    def testSuite(self):
        print "testSuite invoked"
        suite = TestSuite()
        suite.add(WasRun("testMethod"))
        suite.add(WasRun("testBroken"))
        suite.run(self.result)
        assert self.result.summary() == "2 run, 1 failed"

    def tearDown(self):
        pass

result = TestResult()
suite = TestSuite()
suite.add(TestCaseTest("testTemplateMethod"))
suite.add(TestCaseTest("testResult"))
suite.add(TestCaseTest("testFailedResult"))
suite.add(TestCaseTest("testResultFormatting"))
suite.add(TestCaseTest("testSuite"))
suite.run(result)
print result.summary()

