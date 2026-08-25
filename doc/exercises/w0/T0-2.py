"""T0-2 类：Scene，字段 id / title_zh / level；__str__ 打印可读一行。

对应产品：场景选择器里每一项；数据形状接近 backend/data/scenes.json。

================================================================
一、类 vs 实例
================================================================
- 类（class Scene）：图纸，描述「场景」有哪些数据、哪些行为。
- 实例（Scene(...)）：按图纸造出来的一个具体场景。
  产品里会有很多场景（咖啡店、面试、问路），所以用类，而不是三个散变量。

================================================================
二、字段 / 属性：标注 ≠ 存储
================================================================
    class Scene:
        id: int          # 这只是类型标注（告诉读代码的人 / 检查器）
        title_zh: str    # 不会在创建对象时自动带上这三个值
        level: str

真正把值存到「这个对象」上，要在 __init__ 里：
    self.id = id     # 实例属性：每个对象自己有一份

- 类身上的 id: int     → 注解，不是已赋值的数据
- 实例身上的 self.id   → 真正能 scene.id 读到的数据

本题三个字段是实例属性。真实数据里 id 更像 "coffee_shop"（str），
不一定是 int；练习里写成 int 也可以。

注意：id 是 Python 内置函数名。当参数名完全可以，但会暂时挡住内置 id()。
正式代码里更常见 scene_id。

================================================================
三、__init__：实例化时自动调用
================================================================
Scene(...) 括号里写的，会进到 __init__（self 后面的参数）。

过程：
1. Python 先造一个空的 Scene 对象
2. 自动调用 __init__，第一个参数 self 不用你传
   （解释器把「刚造出来的那个对象」塞进去）
3. 你传入的 id / title_zh / level 赋给 self.xxx

    Scene(id=1, title_zh="Test", level="Test")
            ↓
    __init__(self, id=1, title_zh="Test", level="Test")
              ↑ 自动传入，调用时不要自己写 self

self.id = id 的意思：左边是实例属性，右边是参数（局部变量），名字可以相同。

================================================================
四、参数怎么传（和普通函数一样）
================================================================

1) 位置参数（positional）：顺序必须和 __init__ 里 self 后面一致
       Scene(1, "Test", "Test")
       #      id  title_zh  level

2) 关键字参数（keyword）：名字对上即可，顺序可变
       Scene(id=1, title_zh="Test", level="Test")
       Scene(title_zh="Test", level="Test", id=1)  # 也可以

3) 混用：位置必须在前，关键字在后
       Scene(1, title_zh="Test", level="Test")   # 可以
       # Scene(id=1, "Test", "Test")             # 语法错误

4) 默认参数（default）：定义时 = 后面的值，调用时可省略
       def __init__(self, id: int = 0, title_zh: str = "", level: str = ""):
       Scene()                    # 全用默认：0, "", ""
       Scene(id=1)                # 其余用默认
       没有默认值的参数，实例化时必须给，否则 TypeError: missing ... argument
       规则：有默认值的参数必须写在没有默认值的后面。

5) 位置专用 / 关键字专用（了解即可，本题不用）
       def f(a, /, b, *, c):
           # a 只能位置传；c 只能关键字传；b 两种都行
       def f(*args, **kwargs):
           # args 收多余的位置参数（元组）；kwargs 收多余的关键字（字典）

================================================================
五、类型提示 Type Hints（T0-5 会再练，这里先认脸）
================================================================
    id: int
    title_zh: str
    def __init__(self, id: int = 0, ...) -> None:   # -> None 表示无返回值

- 只是标注，运行时默认不强制（乱传字符串给 int 参数，Python 仍会跑）
- 给人和检查器（如 Pyright）看；后面 Pydantic 才会在运行时真正校验
- 常见写法：list[str]、dict[str, str]、str | None（可选）

================================================================
六、__str__：规定 print 时长什么样
================================================================
print(obj) / str(obj) 会调用 __str__，要用它的 return 值。

没写 __str__ 时默认类似：
    <__main__.Scene object at 0x104a1c4d0>

可读一行 = 返回单行、人能看懂的字符串（不要在 __str__ 里自己 print）。
__repr__ 是给开发者/调试看的，本题只要求 __str__。

================================================================
七、if __name__ == "__main__"
================================================================
直接 python T0-2.py 时这段会执行；被 import 时不会跑（避免一导入就打印）。
T0-4 拆模块时会再用到。
"""


class Scene:
    id: int
    title_zh: str
    level: str

    def __init__(self, id: int = 0, title_zh: str = "", level: str = ""):
        self.id = id
        self.title_zh = title_zh
        self.level = level

    def __str__(self):
        return f"Scene(id={self.id}, title_zh={self.title_zh}, level={self.level})"


if __name__ == "__main__":
    scene = Scene(id=1, title_zh="Test", level="Test")
    print(scene)
