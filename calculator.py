def add(a, b):
    """加法"""
    return a + b


def subtract(a, b):
    """减法"""
    return a - b


def multiply(a, b):
    """乘法"""
    return a * b


def divide(a, b):
    """除法"""
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b


def calculate(a, op, b):
    """根据运算符执行计算"""
    ops = {
        "+": add,
        "-": subtract,
        "*": multiply,
        "/": divide,
    }
    if op not in ops:
        raise ValueError(f"不支持的运算符: {op}")
    return ops[op](a, b)


if __name__ == "__main__":
    print("=" * 40)
    print("  简易计算器 (支持 +  -  *  /)")
    print("  输入格式: 1 + 2  (空格分隔)")
    print("  输入 q 退出")
    print("=" * 40)

    while True:
        try:
            expr = input("\n请输入算式: ").strip()
            if expr.lower() == "q":
                print("已退出")
                break
            if not expr:
                continue

            parts = expr.split()
            if len(parts) != 3:
                print("格式错误，请输入如: 1 + 2")
                continue

            a, op, b = float(parts[0]), parts[1], float(parts[2])
            result = calculate(a, op, b)
            # 整数形式的结果去掉 .0
            if result == int(result):
                result = int(result)
            print(f"结果: {a} {op} {b} = {result}")

        except ValueError as e:
            print(f"错误: {e}")
        except KeyboardInterrupt:
            print("\n已退出")
            break
