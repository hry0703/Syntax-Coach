"""T0-4 模块：工具函数放这里，给 main.py 用。

================================================================
Python 怎么「导出」？（没有 export 关键字）
================================================================
JavaScript / TypeScript：
    export function read_file() { ... }
    import { read_file } from "./utils"

Python：
    这个文件就是一个「模块」（module）。
    写在文件顶层的函数、类、常量，默认都能被别的文件 import。
    不需要 export，写了 `export read_file` 反而是语法错误。

在同目录的 main.py 里这样「导入」：

    from utils import read_file          # 只拿这一个名字
    from utils import read_file, Scene   # 一次拿多个
    import utils                         # 拿整个模块，调用时 utils.read_file(...)

运行方式（要在本目录 T0-4/ 下，或保证该目录在 Python 路径里）：

    python main.py

此时 Python 会找到同目录的 utils.py，执行它，再把 read_file 绑到 main 里。

可选约定：
- __all__ = ["read_file"]  只影响 from utils import * 会带出什么
  不影响 from utils import read_file（显式导入永远可以）
- 名字以 _ 开头（如 _helper）表示「内部用，别当公共 API」
  约定而已，挡不住 from utils import _helper
"""


def read_file(file_path: str) -> None:
    try:
        with open(file_path, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("找不到这个文件，请检查路径是否正确。")
    except Exception as e:
        print("其它错误：", e)
