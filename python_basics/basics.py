"""Python 基础语法，用一个类跑完。

运行方式：点 __main__ 旁边的绿色三角，或终端执行 python basics.py

为什么用类：把「数据」和「操作数据的函数」放在一起。
这里 name / score 是属性，5 个小节是方法，run() 依次调用它们。
"""


class PythonBasics:
    """基础语法演示。属性存数据，方法做演示。"""

    def __init__(self, name="小明", score=78):
        # 属性：属于这个对象的数据，所有方法都能用 self 访问
        self.name = name
        self.score = score
        self.fruits = ["苹果", "香蕉", "橘子"]
        self.numbers = [90, 75, 88]

    # ============ 1. 变量和类型 ============
    def section1_variables(self):
        print("--- 1. 变量和类型 ---")

        # Python 不用声明类型，直接写 名字 = 值
        age = 18             # int   整数
        height = 1.75        # float 小数
        is_student = True    # bool  布尔值，只有 True / False

        print(self.name, age, height, is_student)             # 属性也能直接打印
        print(f"{self.name}今年 {age} 岁，身高 {height} 米")    # f-string：花括号里能写变量

        # 常用运算
        print(7 + 2, 7 - 2, 7 * 2, 7 / 2, 7 // 2, 7 % 2)
        print("↑ 依次是：加、减、乘、除（得小数）、整除（丢小数）、取余")

        # 类型转换：input() 拿到的永远是字符串，要算数得先转换
        text = "42"
        print(int(text) + 1)        # 43
        print(float("3.5") * 2)     # 7.0
        print(str(100) + "分")       # 100分

    # ============ 2. 判断 ============
    def section2_condition(self):
        print("--- 2. 判断 ---")

        if self.score >= 90:
            level = "优秀"
        elif self.score >= 60:
            level = "及格"
        else:
            level = "不及格"
        print(f"{self.score} 分 -> {level}")
        # 条件从上往下判断，命中一个就结束
        # 缩进就是语法，同一个块里必须对齐（统一用 4 个空格）

        # 组合条件：and 两个都要满足，or 满足一个，not 取反
        age = 20
        has_ticket = True
        print(age >= 18 and has_ticket)     # True

    # ============ 3. 循环 ============
    def section3_loops(self):
        print("--- 3. 循环 ---")

        # for：次数已知，或者要遍历一堆东西
        for i in range(3):          # 依次得到 0、1、2
            print("第", i, "次")

        for fruit in self.fruits:
            print("我喜欢吃", fruit)

        # while：次数不确定，靠条件停下来
        countdown = 3
        while countdown > 0:
            print("倒计时", countdown)
            countdown -= 1          # 少了这行就变成死循环

        # break 直接跳出循环，continue 跳过本次进入下一次
        for n in range(1, 10):
            if n == 4:
                continue
            if n == 6:
                break
            print(n)

    # ============ 4. 列表和字典 ============
    def section4_collections(self):
        print("--- 4. 列表和字典 ---")

        # 列表：有顺序，能增删改
        print("初始列表:", self.numbers)

        self.numbers.append(100)              # 末尾加一个
        print("append(100) 后:", self.numbers)

        self.numbers[0] = 95                  # 改写第一个
        print("把第一个改成 95 后:", self.numbers)

        print("长度", len(self.numbers), "最大", max(self.numbers), "求和", sum(self.numbers))
        print("第一个", self.numbers[0], "最后一个", self.numbers[-1])
        print("前两个", self.numbers[:2])      # 切片左闭右开，不含下标 2

        # 字典：按键取值
        student = {"name": "小红", "age": 19}
        print(student["name"])                # 取值
        student["city"] = "北京"               # key 不存在就是新增
        print(student.get("phone", "没填"))    # 取不到时用默认值，不会报错

        # 列表里装字典：实际工作中最常见的组合
        people = [
            {"name": "小明", "score": 90},
            {"name": "小红", "score": 85},
        ]
        for person in people:
            print(person["name"], person["score"])

    # ============ 5. 函数 ============
    def section5_functions(self):
        print("--- 5. 函数（在类里叫方法） ---")

        print(self.greet("小明"))
        print(self.greet("小红", "早上好"))    # 第二个参数可以自己指定
        print(self.average([90, 75, 88]))
        print(self.average([]))               # 0，没有崩溃
        print("4 是偶数吗", self.is_even(4), "；7 是偶数吗", self.is_even(7))

        # 返回两个值：调用方可以一次接住，也可以当元组整体使用
        # 这里的 self.numbers 是第 4 节改过的那个列表 [95, 75, 88, 100]
        total, avg = self.total_score(self.numbers)
        print(f"总分 {total}，平均分 {avg:.2f}")
        print("空列表也不会崩：", self.total_score([]))

    # ---------- 下面三个用不到对象的数据，标成 @staticmethod ----------
    @staticmethod
    def greet(who, greeting="你好"):
        """打招呼。greeting 有默认值，不传就用它。"""
        return f"{greeting}，{who}！"

    @staticmethod
    def average(numbers):
        """求平均值。一个函数尽量只做一件事。"""
        if not numbers:         # 先把空列表挡掉，避免除以 0
            return 0
        return sum(numbers) / len(numbers)

    def total_score(self, numbers):
        """返回总分和平均分两个值。

        多个返回值其实是返回了一个元组，调用方可以用 a, b = ... 一次接住。
        这里复用了上面的 average()，不用把求平均的逻辑再写一遍。
        """
        return sum(numbers), self.average(numbers)

    @staticmethod
    def is_even(n):
        """判断是不是偶数。"""
        return n % 2 == 0
    

    def run(self):
        """依次执行所有小结。"""
        self.section1_variables()
        print()
        self.section2_condition()
        print()
        self.section3_loops()
        print()
        self.section4_collections()
        print()
        self.section5_functions()


if __name__ == "__main__":
    # 直接运行这个文件才会执行；被别人 import 时不会
    PythonBasics().run()


# ============ 练习 ============
# 1. PythonBasics(score=55).run()，看第 2 节输出怎么变。
# 2. 给类加一个属性 city，在第 1 节里打印出来。
# 3. 加一个方法 section6_xxx()，写你自己的练习，再挂到 run() 里。
# 4. 把 total_score 改成返回字典 {"total": 总分, "average": 平均分}。
