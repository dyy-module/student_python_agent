class FooParent(object):
	def __init__(self):
		self.parent = "I'm the parent."
		print('Parent')
	def bar(self, message):
		print("%s from Parent" % message)
class FooChild(FooParent):
	def __init__(self):
		super().__init__()
		print('Child')
	def bar(self, message):
		super().bar(message)
		print('Child bar function')
		print(self.parent)
fooChild = FooChild()
fooChild.bar('Hello')

# 定义一个 类 FooParent，
# __init__ ，self 挂载属性 parent = "I'm the parent."
# 实例时打印 Parent
# FooParent 定义一个公共方法bar，接收一个参数message，打印 {message} from  Parent
#
#定义一个类，FooChild 继承FooParent，
# 定义__init,实例时，super调用父类__init__ 方法，slef 挂载parent = "I'm the parent.",打印Child
# 定义一个类方法bar，覆盖了继承自FooParent 的bar 方法,接收一个参数message。
# bar方法super调用了父类方法 bar,传入message。
# 打印Child bar function 
# 打印self.parent，既初始化时的"I'm the parent."
#
# fooChild = FooChild() 实例化类FooChild，此时FooChild 调用__init__, 故调用super().__init__()，self 挂在属性parent = "I'm the parent."，打印Parent，然后打印Child
# fooChild.bar('Hello') 调用了类FooChild 的方法bar, super().bar(message) 调用了FooParent 的bar，打印 Hello from Parent,然后打印Child bar function，然后打印self挂在的属性parent，既I'm the parent.