# 第03周 · Day16 学习笔记

> 说明:本文件由学习者本人在完成当天学习后填写,须覆盖当日全部学习内容。口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段允许,但须单独成块并标注语言。末尾须做行为-知识点自证表(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
class 继承语法
class 方法重新 override
super().__init__()调用父类构造
多态:同一接口不同实现
issubclass() 判断类继承关系

## 知识点小结
```python
class Ami(object): #Ami 继承 内置对象object
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(self.name)
        return self.name

class Smi(Ami): # Smi 继承Ami 类
    def __init__(self, name):
        super().__init__(name) # super()调用 父类__init__ 进行初始化
    
    def speak(self):#复写父类 speak方法
        super().speak() #这里可以调用父类方法
        print(f'复写方法名，可以做其他操作') # 可以做其他操作

class Qaa(Ami):
    def __init__(self, name):
        super().__init__(name)
    
    def speak(self):
        print(f'不同子类，相同的方法有不同的写法，这种不同就是多态') 

print(issubclass(Qaa,Ami)) # true ,issubclass 用来检测类是不是继承关系。
print(issubclass(Qaa,Smi)) # false
print(issubclass(Qaa,Qaa)) # true ,类是自身的继承

```

```javascript
class Ami{ // 创建一个类
    constructor(name){ // 初始化方法，
        this.name = name // 设置实例name
    }

    speak(){
        console.log(this.name) // 打印实例name
    }
}

class Smi extends Ami{ // extends 继承类
    constructor(...args){ // 可以不写，会默认加上 constructor 初始化
    // super() 必须在子类构造器的首行调用，即必须在 this 之前使用，否则会报错
        super(...args)
    }
    speak(){ // 覆盖 speak 方法
        super.speak() // 调用父类 speak 方法
        console.log('复写方法名，可以做其他操作') // 作额外的操作
    }
}

console.log(typeof Ami) // function, js的typeof 打印的是字符串类型
console.log(Smi.prototype instanceof Ami) // true
smi = new Smi('smi')
console.log(smi instanceof Ami) // true
```
## JS→Python 对照
js 继承 extends 关键字 -> python 把类当参数传入class
js 方法重写，覆盖方法名 -> Python 和js 相似，覆盖方法名，但python方法第一个参数得传self
js 类构造器 constructor(X,Y,...) -> python 构造器 __init__(self,X,Y,...) 方法， 第一个参数必须是self
js 构造器内调用父类， super(参数) -> python super().__init__(参数)
js 判断继承方法，没有类似issubclass的方法，可以通过 Smi.prototype instanceof Ami 看Ami 是否在Smi 的原型链上 -> python issubclass 可以直接对比 Smi 是不是继承 Ami
js instanceof  和python  isinstance 类似。 可以对比实例。写法不同。 smi instanceof Ami -> python isinstance(smi, Ami)


## 卡点与解决(非必填) 
暂无

## 行为-知识点自证表(行=产物里的一个行为)
AI转型教程\学习产物\第03周\day16\employee.py

| 行为 | 用到的知识点 | 其中我说不出出处的 |
| class Manager 继承 Employee | class 入参继承 | ------------------ |
| __init__ 中调用 super().__init__ |  继承构造函数初始化     |                    |
| Developer salary |  覆盖继承类方法，复写并增加新功能，按级别在基础薪资上加工资，每级500     |                    |
| print(qqa.intro()) |  调用来自父类方法，并打印    |                    |
|  print(isinstance(qqa, Employee)) |  isinstance 对比实例是不是 Employee 的继承    |                    |
|  print(issubclass(Employee, Employee))|  issubclass 自己是自己的继承    |                    |
|  print(issubclass(Manager, Employee))|  issubclass 对比Manager类是不是 Employee 的继承，自己是自己的继承    |                    |


表外一行·当日学了但没落进任何行为的知识点:无
闭卷一问(extra_animal)的答案:
问题：子类自己不写 speak() 时,调用会发生什么?说清属性在哪一层被找到、按什么顺序往下找。
Bear 调用的时候，因为本身定义了speak，所以调用的就是本身
Hamster 调用的时候，因为本身没有speak,所以调用会查原型Animal，Animal上有这个方法，就会调用继承来的speak,如果没有会报错

