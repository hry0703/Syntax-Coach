# #### Day 1～3｜Python 语法手感
# - [ ] **T0-1 函数**：写 `normalize(text: str) -> str`，去掉首尾空白；空串返回 `""`。再写测试：`"  hi  "` → `"hi"`
# - [ ] **T0-2 类**：写 `Scene` 类，字段 `id / title_zh / level`；实现 `__str__` 打印可读一行
# - [ ] **T0-3 异常**：读一个不存在的文件路径，用 `try/except FileNotFoundError` 打印友好中文，不要让进程裸崩
# - [ ] **T0-4 模块**：把上面函数/类拆成 `utils.py` + `main.py`，用 `from utils import ...` 调用

def normalize(text:str)->str:
    while text and text[0] == " " and text[-1] == " ":
        text = text[1:]
    while text and text[-1] == " ":
        text = text[:-1]
    return text

def test_normalize()->None:
    assert normalize("  hi  ") == "hi"
    assert normalize("  ") == ""
    assert normalize("hi") == "hi"
    assert normalize("  hi  ") == "hi"
    assert normalize("  hi  ") == "hi"


if __name__ == "__main__":
   print(test_normalize())