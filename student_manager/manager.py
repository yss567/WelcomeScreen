"""StudentManager：管理一「组」学生，负责增删查改、统计和存盘。

三个文件的分工，一眼看清：

    student.py —— 一个学生自己会算什么（总分、等级）
    manager.py —— 一群学生怎么组织（查找、排序、统计、存盘）  ← 本文件
    main.py    —— 怎么和用户打交道（菜单、输入、打印）

新手最常见的毛病是把这三件事揉进一个文件，越写越长越改不动。
拆开之后每个文件都短，要改哪块就动哪个文件。

直接运行本文件可以看演示：python manager.py
"""

import json
from pathlib import Path

from student import Student


class StudentManager:
    """学生名单。内部用一个列表装 Student 对象。"""

    def __init__(self, filename="data.json"):
        self.students = []      # 列表里装的是 Student 对象，不是字典
        # 用 __file__ 定位文件，保证不管从哪个目录运行，读写的都是同一个文件。
        # 如果写成 "data.json"，在 PyCharm 里点运行和在终端里运行会落到两个不同目录。
        self.path = Path(__file__).with_name(filename)

    # ---------- 增、删、查 ----------

    def add(self, name, scores=None):
        """添加学生。返回新建的 Student，方便调用方接着用。"""
        student = Student(name, scores)
        self.students.append(student)
        return student

    def find(self, name):
        """按姓名查找：找到返回 Student，找不到返回 None。

        返回 None 而不是直接报错，是 Python 里表示「没找到」的惯例，
        调用方用 if student: 判断一下就行。
        """
        for student in self.students:
            if student.name == name:
                return student
        return None

    def remove(self, name):
        """删除学生：删掉了返回 True，本来就没人返回 False。"""
        student = self.find(name)
        if student is None:
            return False
        self.students.remove(student)
        return True

    # ---------- 统计 ----------

    def ranking(self):
        """按平均分从高到低排序，返回一个新列表。

        sorted() 不改动原列表（想原地改就用 self.students.sort()）。
        key= 告诉 Python「拿什么来比大小」。因为要比的是「对象的平均分」而不是对象本身，
        所以得给一个小函数，lambda 就是「没名字的临时函数」，等价于：

            def key_of(s):
                return s.average()

        reverse=True 表示从大到小。
        """
        return sorted(self.students, key=lambda s: s.average(), reverse=True)

    def statistics(self):
        """班级整体情况，返回一个字典。"""
        if not self.students:       # 空名单先挡掉，否则下面要除以 0
            return {"人数": 0, "班级平均分": 0, "最高分": 0, "最低分": 0, "及格率": "0%"}

        # 列表推导式：把 for 循环 + append 压缩成一行，读作「对每个学生取他的平均分」
        averages = [s.average() for s in self.students]
        passed = [s for s in self.students if s.is_pass()]      # 带 if 的筛选

        return {
            "人数": len(self.students),
            "班级平均分": round(sum(averages) / len(averages), 2),
            "最高分": round(max(averages), 2),
            "最低分": round(min(averages), 2),
            "及格率": f"{len(passed) / len(self.students):.0%}",   # :.0% 自动转成百分比
        }

    # ---------- 存盘 / 读盘 ----------

    def save(self):
        """把所有学生写进 JSON 文件，返回文件路径。"""
        data = [s.to_dict() for s in self.students]     # 对象列表 -> 字典列表

        # ensure_ascii=False 才能把中文原样写进去，否则会变成 小明 这种东西。
        # indent=2 让文件带缩进，方便直接用编辑器打开看。
        self.path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return self.path

    def load(self):
        """从 JSON 文件读回学生名单。成功返回 True。

        两种情况都不让程序崩：
          - 文件不存在：第一次运行，很正常
          - 文件内容坏了：用户手改过，提示一下就行，不该连程序都打不开
        """
        if not self.path.exists():
            return False

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # 只接住「JSON 解析失败」这一种错误。
            # 别写 except: 把所有错误一起吞掉，那样真正的 bug 会被藏起来，很难查。
            print(f"[警告] {self.path.name} 内容不是合法 JSON，已忽略，从空名单开始")
            return False

        self.students = [Student.from_dict(item) for item in data]
        return True


if __name__ == "__main__":
    # 演示用 demo.json，不碰真正的 data.json
    manager = StudentManager("demo.json")
    manager.add("小明", [90, 75, 88])
    manager.add("小红", [95, 92, 88])
    manager.add("小刚", [50, 60, 55])

    print("--- 按平均分排名 ---")
    for i, student in enumerate(manager.ranking(), start=1):    # enumerate 从 1 开始编号
        print(i, student)

    print("--- 班级统计 ---")
    for key, value in manager.statistics().items():     # 遍历字典的键值对
        print(f"{key}：{value}")

    print("--- 存盘再读回来 ---")
    print("已写入", manager.save())
    fresh = StudentManager("demo.json")
    fresh.load()
    print("读回", len(fresh.students), "名学生")


# ============ 练习 ============
# 1. 加一个 top(n) 方法，返回平均分最高的 n 个学生（提示：切片 ranking()[:n]）。
# 2. 加一个 filter_by_level(level) 方法，比如筛出所有「优秀」的学生。
# 3. statistics() 里再加一项「中位数」（提示：先 sorted()，再取中间那个；
#    偶数个取中间两个的平均值）。
# 4. 现在 save() 会直接覆盖整个文件。想一个「每次保存留一个备份」的做法。
