"""Student：一个对象 = 一条学生记录。

basics.py 里的 PythonBasics 是「语法演示大杂烩」，一个类塞了 5 个知识点。
从这个项目开始换思路：一个类只负责一件事。

Student 只操心「一个学生」——他的姓名、成绩、平均分够不够格。
至于「怎么管理一群学生」，那是 manager.py 里 StudentManager 的事。

直接运行本文件可以看演示：python student.py
"""


class Student:
    """一个学生：姓名 + 一组成绩。"""

    def __init__(self, name, scores=None):
        # 注意是 scores=None，而不是 scores=[]，原因见文件末尾「一个经典的坑」
        self.name = name
        self.scores = list(scores) if scores else []

    # ---------- 计算类方法：问这个学生一个问题 ----------

    def total(self):
        """总分。"""
        return sum(self.scores)

    def average(self):
        """平均分。没有成绩时返回 0，避免除以 0 崩溃。"""
        if not self.scores:
            return 0
        return self.total() / len(self.scores)

    def level(self):
        """等级。判断逻辑和 basics.py 第 2 节一样，只是数据换成了自己的。"""
        if not self.scores:
            return "未录入"
        avg = self.average()
        if avg >= 90:
            return "优秀"
        elif avg >= 80:
            return "良好"
        elif avg >= 60:
            return "及格"
        else:
            return "不及格"

    def is_pass(self):
        """是否及格。统计及格率时会用到。"""
        # 没有成绩不算及格，所以这里要先判断 scores 非空
        return bool(self.scores) and self.average() >= 60

    # ---------- 修改类方法：改变自己的数据 ----------

    def add_score(self, score):
        """加一门成绩。方法直接改 self.scores，不需要返回值。"""
        self.scores.append(score)

    # ---------- 和文件打交道的两个方法 ----------
    # JSON 只认识字典/列表/数字/字符串，不认识 Student 对象。
    # 所以要有一个来回「翻译」：对象 -> 字典（存盘），字典 -> 对象（读盘）。

    def to_dict(self):
        """转成能存进 JSON 的字典。"""
        return {"name": self.name, "scores": self.scores}

    @classmethod
    def from_dict(cls, data):
        """从字典还原成 Student。

        cls 就是 Student 本身。写 cls(...) 而不是 Student(...)，
        以后如果有了子类，这里一行都不用改。这是 classmethod 最常见的用法。
        """
        return cls(data["name"], data.get("scores"))

    # ---------- 让 print 好看一点 ----------

    def __str__(self):
        """print(student) 时自动调用，返回给人看的文本。

        前后各两个下划线的是「魔术方法」，Python 会在特定时机自动调用，
        不需要你手动写 student.__str__()。
        """
        return f"{self.name}：平均 {self.average():.2f} 分，{self.level()}"


if __name__ == "__main__":
    s = Student("小明", [90, 75, 88])
    print(s)                        # 靠 __str__ 自动格式化
    print("总分", s.total())

    s.add_score(100)
    print("加分后", s)

    # 没成绩的新生也不会崩
    print(Student("转学生"))

    # 存盘 / 读盘的来回
    data = s.to_dict()
    print("字典形式", data)
    print("还原回来", Student.from_dict(data))


# ============ 一个经典的坑 ============
# 为什么 __init__ 写的是 scores=None，而不是 scores=[]？
# 默认值只在「函数定义的那一刻」算一次，所以写成 [] 的话，所有学生共用同一个列表：
#
#     def __init__(self, name, scores=[]):    # 错误示范
#         self.scores = scores
#
#     a = Student("A")
#     b = Student("B")
#     a.add_score(100)
#     print(b.scores)      # 结果是 [100] —— b 莫名其妙多了个成绩
#
# 记住：默认值不要用列表、字典这种「可变对象」，写 None，再在函数体里新建。

# ============ 练习 ============
# 1. 加一个 highest() 方法，返回最高分；没有成绩时返回 0。
# 2. 加一个 drop_score(index) 方法，删掉第 index 门成绩，注意下标越界的情况。
# 3. 给 Student 加一个属性 student_id，并同步改 to_dict / from_dict。
# 4. level() 现在按平均分算。改成「任意一门不及格就算不及格」试试，想想哪种更合理。
