# ===== day25 跟练任务说明 v3.1(extra/extra_typed_funcs.py,实现由你本人盲写) =====
# 文件:extra_typed_funcs.py | 位置:day25\extra\ | ≤120 行 | 本日不用任何第三方库,只用标准库 typing
# 【题目·对齐教程】extra_typed_funcs.py:写 3 个函数并加完整类型提示——一个返回 Optional、一个参数含 Callable、一个用 Dict/List 容器标注;
# 调用并 print,验证类型注解不影响运行结果。(逐字取自周教程 Day25「跟练清单(放extra/)」)
# 【越界→隔离目录】教程 Day25【超前】集中区所列项(TypedDict、Protocol、Generic[T] 等)欲用请放 day25/beyond/,
# 放对目录即留痕;清单外库/写法同样进 beyond/
# 【教材·只读】精读页见周教程 Day25「教材与章节」段(不在此重列,以教程为唯一出处)
# 【交检】跑通无报错、每步 print;extra 与固定产物分离,只放本 extra/ 目录;index.md 末两行自检照旧
# 【加分可选】同一函数分别用 typing.Optional 与 Union 标两种写法,print 说明二者关系
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from typing import Optional, Callable, List, Dict, Tuple, Any


def get_even(data: List[int]) -> List[int]:
    '''获取偶数'''
    return [r for r in data if int(r) % 2 == 0]


def find(user: Dict[str, str], key: str) -> Optional[str]:
    '''获取属性'''
    return user.get(key)


def count_func(func: Callable[..., Any]) -> Callable[..., Any]:
    '''给函数计数'''
    count = 0

    def apply_func(*args):
        '''调用'''
        nonlocal count
        count += 1
        return func(*args, count)

    return apply_func


if __name__ == '__main__':
    print(get_even(range(1, 10)))
    print(get_even(['1', '2', '4']))
    print(find({}, 'test'))

    def test(a: int, n: int) -> Tuple[int, int]:
        return a, n
    f_1 = count_func(test)
    a, n = f_1(3)
    print('结果', a, 'count', n)
