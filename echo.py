#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    try:
        while True:
            user_input = input()
            print(user_input)
    except (EOFError, KeyboardInterrupt):
        pass

if __name__ == "__main__":
    main()
