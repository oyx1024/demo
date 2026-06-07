#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    # 这个脚本实现一个简单的回显功能，读取用户输入并原样输出
    try:
        while True:
            print("请输入内容（Ctrl+D 或 Ctrl+C 退出）：", end="")
            user_input = input()
            print(f'你输入的内容是: {user_input}')
    except (EOFError, KeyboardInterrupt):
        pass

if __name__ == "__main__":
    main()
