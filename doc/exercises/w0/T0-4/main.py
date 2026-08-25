"""从同目录 utils 导入并调用。没有 export，用 import。"""

from utils import read_file

if __name__ == "__main__":
    read_file("test.txt")
