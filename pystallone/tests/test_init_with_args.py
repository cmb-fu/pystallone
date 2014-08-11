import unittest

class TestInitWithArgs(unittest.TestCase):
    
    def testWithArgsExtendClassPath(self):
        import pystallone
        args = ['-Xms64m', '-Djava.class.path=/dev/null']
        jvm = None
        
        pystallone.startJVM(jvm, args)
        
        a = pystallone.API.doublesNew.array(10)
        
        self.assertEqual(10, a.size())
        