"""T0-6：用 json.load 读仓库 backend/data/scenes.json（只读，别改文件）。

对应前端：fetchScenes() 拿到的场景列表；这里用脚本直接读同一个 JSON。

================================================================
一、两条「当前在哪」不要混
================================================================
1) 进程工作目录 cwd
   你在终端里处在哪个文件夹，os.getcwd() 就是哪。
   相对路径 "backend/data/scenes.json" 是相对 cwd 的。
   从仓库根运行 python doc/exercises/w0/T0-6.py 能碰巧找到；
   从 w0/ 运行 python T0-6.py 就找不到。所以练习里不要靠 cwd。

2) 当前脚本所在目录 __file__
   __file__ 是这个 .py 文件的路径，不随你在哪执行而变。
   读「和代码一起放的数据」应用它来定位，而不是写死绝对路径。

================================================================
二、Path 常用操作（pathlib）
================================================================
    from pathlib import Path

    Path(__file__)                 # 本文件：.../w0/T0-6.py
    Path(__file__).resolve()       # 变成绝对路径，并解开 .. 和符号链接
    p.parent                       # 上一级目录（T0-6.py 的 parent 是 w0/）
    p.parents[n]                   # 往上第 n+1 层（见下表）
    p / "backend" / "data"         # 拼接路径，自动处理 / 与 \\
    p.exists()                     # 文件或目录在不在
    p.read_text(encoding="utf-8")  # 直接读成字符串（本例用 open + json.load 也行）

/ 是 Path 的拼接运算符，不要和除法搞混。不要用字符串 + 拼路径
（Windows 是反斜杠，自己拼容易错）。

老写法 os.path 对照：
    os.path.dirname(__file__)     ≈  Path(__file__).parent
    os.path.join(a, b, c)         ≈  Path(a) / b / c
    os.path.abspath(...)          ≈  Path(...).resolve()

================================================================
三、从本文件爬到仓库根
================================================================
本文件：  syntaxCoach/doc/exercises/w0/T0-6.py
目标：    syntaxCoach/backend/data/scenes.json

    Path(__file__)
      .parent          # [0] w0
      .parent          # [1] exercises
      .parent          # [2] doc
      .parent          # [3] syntaxCoach  ← 仓库根

    Path(__file__).resolve().parents[3] / "backend" / "data" / "scenes.json"

注意：.parent 写 3 次只到 doc/，还要再一次才到仓库根。
parents[3] 等价于连续 4 次 .parent（从 0 数到 3）。

================================================================
四、打开文件
================================================================
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

- encoding="utf-8"：scenes.json 有中文，不写可能在部分系统乱码
- json.load(f) 读文件对象；json.loads(字符串) 读内存里的 JSON 文本
- with 结束会自动关文件

题目返回类型：list[dict[str, str]]
  JSON 最外层是数组 → list
  每个场景是对象，值都是字符串 → dict[str, str]
  （这是简化标注；若以后有数字字段，应写成 dict[str, Any]）
"""

import json
from pathlib import Path


def load_scenes(path: str) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    data_file = Path(__file__).resolve().parents[3] / "backend" / "data" / "scenes.json"
    scenes = load_scenes(str(data_file))
    print(scenes)
