"""T0-3 异常：读不存在的文件，用 try/except 接住，不要让进程裸崩。

================================================================
try / except 知识点（对照本文件底部的示例代码）
================================================================

1. 没有 try 时会发生什么
   open("不存在.txt", "r") 在文件不存在时会 raise FileNotFoundError。
   没人接住的话：打印一整段 Traceback，进程以非 0 状态退出。
   这就是题目说的「裸崩」。

2. 基本结构
   try:
       # 可能出错的代码
   except 某种错误:
       # 只在这种错误发生时执行

   执行顺序：
   - 先跑 try 里的语句。
   - 没有异常 → except 整段跳过。
   - 有异常 → 立刻离开 try（后面的行不再执行），去匹配 except。
   - 匹配成功 → 跑对应 except，然后程序继续往下（默认不会再崩）。
   - 一个都匹配不上 → 异常继续往外传，还是可能崩。

3. 要捕获「哪一种」错误（越具体越好）
   FileNotFoundError  → 路径不存在（本题点名要接这个）
   PermissionError    → 没权限读
   IsADirectoryError  → 路径是个目录
   Exception          → 几乎所有普通错误的基类（很大一网）

   多个 except 从上往下匹配：先写窄的，再写宽的。
   若把 except Exception 写在最上面，FileNotFoundError 永远进不去
   （因为它也是 Exception 的一种）。

   except Exception as e 里的 e 是异常对象，print(e) 一般是英文短消息。
   题目要的是「友好中文」，针对「找不到文件」自己写一句即可。

4. 不要写成「吞掉一切」
   except:          # 连键盘中断都可能被吃掉，练习里别用
       pass
   except Exception:
       pass         # 出错了但什么都不说，排障会很痛苦

   T0-3 标准做法：只接 FileNotFoundError，打印一句友好中文。

5. else 和 finally（了解即可，这题不必写）
   else:    try 完全成功、没异常时才走
   finally: 无论成功还是失败都会走（关资源、打日志）
   本例用了 with open，文件关闭由 with 负责，一般不必再为关文件写 finally。

6. with open 和 try/except 的关系
   with         → 管资源（用完关掉文件）
   try/except   → 管「打开失败怎么办」
   两者常叠在一起。open 失败发生在进入 with 之前，不会留下没关上的文件。
"""

if __name__ == "__main__":
    try:
        with open("test.txt", "r") as f:
            print(f.read())
    except FileNotFoundError:
        print("找不到这个文件，请检查路径是否正确。")
    except Exception as e:
        print("其它错误：", e)
