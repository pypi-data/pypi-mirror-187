import unittest


class TestMethodNotAllowed(unittest.TestCase):
    def test_method_not_allowed(self):
        from dryco.decorators import method_not_allowed

        class Dog:

            @method_not_allowed
            def meow(self):
                pass

            @method_not_allowed
            def meow_1(self, arg):
                pass

            @method_not_allowed
            def meow_2(self, arg, kwarg):
                pass

            @method_not_allowed(exception=ConnectionResetError(1))
            def meow_3(self, arg, kwarg):
                pass

            @method_not_allowed(exception=ConnectionResetError(1))
            def meow_4(self, arg, kwarg):
                pass

            @method_not_allowed(exception=ConnectionResetError(1))
            def meow_5(self, arg, kwarg):
                pass

        a_dog = Dog()

        self.assertRaises(Exception, a_dog.meow)
        self.assertRaises(Exception, a_dog.meow_1)
        self.assertRaises(Exception, a_dog.meow_2)
        self.assertRaises(ConnectionResetError, a_dog.meow_3)
        self.assertRaises(ConnectionResetError, a_dog.meow_4)
        self.assertRaises(ConnectionResetError, a_dog.meow_5)


if __name__ == '__main__':
    unittest.main()
