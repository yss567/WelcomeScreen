"""菜单程序：和用户打交道的那一层。

这个文件里没有任何「计算」和「存盘」的逻辑，
它只做三件事：显示菜单、拿到输入、调用 StudentManager。

好处：以后想改成网页版，只需要换掉这个文件，student.py 和 manager.py 原封不动。

运行：python main.py
"""

from manager import StudentManager

MENU = """
========= 学生成绩管理 =========
1. 查看全部（按平均分排序）
2. 添加学生
3. 删除学生
4. 查询某个学生
5. 班级统计
6. 保存到文件
7. 退出
"""


def ask_scores():
    """问用户要成绩，返回分数列表。

    这段是初学者最容易漏掉的部分——处理「用户不按套路输入」：
        90 80 88     -> [90.0, 80.0, 88.0]
        （直接回车）  -> []                        允许先不填
        90 abc 88    -> 提示一句，跳过 abc 继续     不能直接崩
    """
    text = input("输入成绩，用空格隔开（直接回车表示暂无）：").strip()
    if not text:
        return []

    scores = []
    for piece in text.split():      # split() 不传参数 = 按任意空白切分
        try:
            scores.append(float(piece))
        except ValueError:
            # float("abc") 会抛 ValueError。接住它，程序就能继续跑。
            print(f"  「{piece}」不是数字，已跳过")
    return scores


def show_all(manager):
    """打印排名表。"""
    if not manager.students:
        print("名单是空的，先选 2 添加一个吧")
        return

    print("排名  学生情况")
    for i, student in enumerate(manager.ranking(), start=1):
        print(f"{i:<4}  {student}")


def main():
    manager = StudentManager()
    if manager.load():
        print(f"已从 {manager.path.name} 读入 {len(manager.students)} 名学生")

    # while True 是菜单程序的固定写法：靠 break 退出，而不是靠条件为假
    while True:
        print(MENU)
        choice = input("请选择（1-7）：").strip()

        if choice == "1":
            show_all(manager)

        elif choice == "2":
            name = input("姓名：").strip()
            if not name:
                print("姓名不能为空")
                continue        # 跳过本次循环剩下的代码，直接回到菜单
            if manager.find(name):
                print(f"{name} 已经在名单里了")
                continue
            manager.add(name, ask_scores())
            print(f"已添加 {name}")

        elif choice == "3":
            name = input("要删除的姓名：").strip()
            # 三元表达式：把 if/else 压在一行里，适合这种「二选一打印」的场景
            print("已删除" if manager.remove(name) else "名单里没有这个人")

        elif choice == "4":
            name = input("要查询的姓名：").strip()
            student = manager.find(name)
            if student:
                print(student)
                print("各科成绩：", student.scores)
            else:
                print("名单里没有这个人")

        elif choice == "5":
            for key, value in manager.statistics().items():
                print(f"{key}：{value}")

        elif choice == "6":
            print(f"已保存到 {manager.save()}")

        elif choice == "7":
            manager.save()      # 退出前顺手存一下，省得白录半天
            print("已保存，再见")
            break               # 跳出 while，程序结束

        else:
            print("请输入 1-7 之间的数字")


if __name__ == "__main__":
    main()


# ============ 练习 ============
# 1. 加一个菜单项「8. 给某个学生加一门成绩」，调用 student.add_score()。
# 2. 加「9. 按姓名改成绩」，先 find 再直接改 student.scores。
# 3. 现在退出才存盘，中途崩了就全丢了。改成「每次增删之后自动 save()」。
# 4. 加一个「导出 CSV」功能，用 Excel 能打开（提示：open(..., "w", encoding="utf-8-sig")，
#    每行写 "姓名,成绩1,成绩2"，注意 utf-8-sig 是给 Excel 认中文用的）。
