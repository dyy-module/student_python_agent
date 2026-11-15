# ===== day25 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:typed_stats.py | 位置:day25\ | ≤120 行 | 第三方库已解禁(day22),但本日不用任何库、只用标准库 typing
# 【题目·对齐教程】编写 学习产物/第04周/day25/typed_stats.py:带类型提示的数据统计工具(≤120行):定义 3-4 个函数并写**完整**类型提示:
# 如求平均值(参数 List[int]、返回 float)、按条件过滤(参数 List + Callable 谓词、返回 List)、词频统计(参数 List[str]、返回 Dict[str, int])、安全取值(找不到返回 None 故标 Optional);
# 主流程用一组示例数据调用这些函数并 print 结果;额外演示:故意传入类型不符的值,print 说明"程序仍运行"(印证类型提示运行时不强制);所用知识点清单见教程 Day25「当日产出」段
# 【越界→隔离目录】教程 Day25【超前】集中区所列项(TypedDict、Protocol、Generic[T]、from __future__ import annotations)欲用请放 day25/beyond/,放对目录即留痕,
# 不写进交检产物;其余不在教程内的库/写法属清单外,同样进 beyond/ 隔离
# 【教材·只读】精读页见周教程 Day25「教材与章节」段(不在此重列,以教程为唯一出处)
#   ⚠ 教程 Day25 已订正(v1.3):主锚点=官方 typing 页(按需检索词条勿通读),"运行时不强制"概念出处=官方教程 4.9.8 函数注解;廖雪峰无 typing 小节;勿在本日混用 3.9+ list[int] 与 typing.List[int] 两种写法
# 【交检】跑通无报错、每步 print;函数注解要"完整"(每个参数+返回值都标);index.md 末两行自检(①我说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点——Union/Tuple/Set/mypy 若产物未用到,记在第②行;行为对账由助教读产物完成)
# 【加分可选】用 Union[X, Y] 改写一个函数;用 mypy 对本文件跑一次静态检查并贴输出
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from typing import List, Optional, Dict, Any, Callable


def get_average(d: List[int]) -> float:
    '求平均值,保留两位小数'
    return round(sum(d)/len(d), 2)


def filter_list(d: List[Any], filterFunc: Callable[[int], bool]) -> List[Any]:
    '''过滤字符数组'''
    return [r for r in d if filterFunc(r)]


def count_word(d: List[str]) -> Dict[str, int]:
    '''统计词频'''
    result = {}
    for r in d:
        result[r] = result.get(r, 0)+1
    return result


def get_word_count(d: Dict[str, int], key: str) -> Optional[int]:
    '''获取单词词频'''
    return d.get(key)


if __name__ == '__main__':
    test = ['aa', 1, 2, 3, 'bb', 'cc', 'aa']
    print(get_average(range(1, 10)))
    f_s = filter_list(test, lambda r: isinstance(r, str))
    print('过滤结果', f_s)
    count_f = count_word(f_s)
    print(count_f)
    print(get_word_count(count_f, 'aa'))
    print(get_word_count(count_f, 'wq'))
    print('类型不一致，仍能运行', get_word_count(count_f, 1))
