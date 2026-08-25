"""T0-5：给 T0-1～T0-2 补全 Type Hints（参数、返回值）。

对应前端：TypeScript 的 `text: string` / `: string`；Python 写法很像，
但默认只给人和检查器看，运行时不会因为类型写错就拒绝执行。

================================================================
一、Type Hints 是什么
================================================================
在函数/方法上标注「参数是什么类型、返回什么类型」：

    def normalize(text: str) -> str:
        ...

读法：text 应该是 str；箭头后面表示返回值是 str。

没有返回值（只做事、或只 print）写成 -> None：

    def test_normalize() -> None:
        assert ...

类方法同样：__init__ 约定返回 None；__str__ 返回 str。
self 一般不写类型（解释器已经知道它是当前类的实例）。

================================================================
二、和 TypeScript 的对照
================================================================
    TS:  function normalize(text: string): string
    Py:  def normalize(text: str) -> str

    TS:  function f(): void
    Py:  def f() -> None

    TS:  title?: string | null
    Py:  title: str | None = None     # T0-7 会用到

    TS:  scenes: Record<string, string>[]
    Py:  list[dict[str, str]]         # T0-6 会用到

常见内置名：str / int / float / bool / None / list / dict / tuple / set

================================================================
三、运行时不强制（这是和 TS / Pydantic 最大的差别）
================================================================
    def add(x: int, y: int) -> int:
        return x + y

    add("a", "b")   # 类型写的是 int，但运行仍可能成功，得到 "ab"

检查器（Pyright / mypy）会报警；裸 Python 默认不管。
本仓库后端 FastAPI + Pydantic 才会在请求进来时真正校验类型。
学习计划段末那句：Type Hints ≈ TS 类型，但运行时默认不强制。

================================================================
四、要标哪里（本题范围）
================================================================
1) 函数参数：  text: str
2) 函数返回值：-> str  或  -> None
3) 类字段注解：id: int（仍只是注解，真正赋值还在 __init__）
4) __init__ 参数 + -> None
5) __str__ -> str

还没要求标：局部变量（可写 x: str = "hi"，一般省略）。

================================================================
五、容器与可选（先认脸，T0-6 / T0-7 再用）
================================================================
    list[str]                 # 字符串列表
    dict[str, str]            # 键值都是字符串的字典
    tuple[int, str]           # 两个元素、类型固定的元组
    str | None                # 要么 str，要么 None（可选）
    list[dict[str, str]]      # 字典组成的列表（load_scenes 的返回值）

Python 3.9 以前要写 from typing import List, Optional
    List[str]、Optional[str]  等价于  list[str]、str | None
本仓库 Python 够新，直接用 list[] 和 | 即可。

================================================================
六、类上的两种标注
================================================================
    class Scene:
        id: int                    # 类体上的注解（给检查器看字段）
        def __init__(self, id: int = 0) -> None:
            self.id = id           # 运行时真正存值

两者建议一致：注解写 int，赋值也给 int。
"""


def normalize(text: str) -> str:
    while text and text[0] == " " and text[-1] == " ":
        text = text[1:]
    while text and text[-1] == " ":
        text = text[:-1]
    return text


def test_normalize() -> None:
    assert normalize("  hi  ") == "hi"
    assert normalize("  ") == ""
    assert normalize("hi") == "hi"


class Scene:
    id: int
    title_zh: str
    level: str

    def __init__(self, id: int = 0, title_zh: str = "", level: str = "") -> None:
        self.id = id
        self.title_zh = title_zh
        self.level = level

    def __str__(self) -> str:
        return f"Scene(id={self.id}, title_zh={self.title_zh}, level={self.level})"


if __name__ == "__main__":
    test_normalize()
    scene: Scene = Scene(id=1, title_zh="咖啡店点单", level="B1")
    print(normalize("  hi  "))
    print(scene)
