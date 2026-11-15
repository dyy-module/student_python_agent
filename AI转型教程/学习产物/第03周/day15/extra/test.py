class Test:
    pass

class Test2(Test):
    pass


c1 = Test2()

print(type(c1) is Test)
print(type(c1) is Test2)
