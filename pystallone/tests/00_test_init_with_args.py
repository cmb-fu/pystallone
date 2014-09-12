import unittest2

class TestInitWithArgs(unittest2.TestCase):
    
    def testWithArgsExtendClassPath(self):
        import pystallone
        args = ['-Xms64m']#, '-Djava.class.path=.']
        jvm = None
        
        pystallone.startJVM(jvm, args)
        
        a = pystallone.API.doublesNew.array(10)
        
        self.assertEqual(10, a.size())
        