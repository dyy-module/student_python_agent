# 超前
class Fib(object):
    def __init__(self):
        self.a = 0
        self.b = 1
    
    def __iter__(self):# 返回可迭代对象
        return self
    
    def __next__(self):# 迭代器调用的方法 next
        self.a, self.b = self.b, self.a + self.b
        if self.a >100:
            raise StopIteration()
        return self.a

    def __getitem__(self, n):# 方法读
        if(isinstance(n,int)):
            a,b = 1,1
            for x in range(n):
                a,b=b,a+b
            return a
        if(isinstance(n,slice)):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
    def __getattr__(self, name):# 如果属性不存在，才会走__getattr__
        if name =='name':
            return '是aa'
        return '访问属性'

if __name__ =='__main__':
    f = Fib()
    f.name ='走这里'
    for i in f:
        print(i)
        
    print(f[5])
    print(f[1:3])
    print(f.name)
    print(f.bb)