#!/usr/bin/env python3
"""测试执行入口"""
import sys
import pytest

if __name__ == "__main__":
    args = [
        "-v",
        "--tb=short",
        "--log-cli-level=INFO",
        *sys.argv[1:],
    ]
    sys.exit(pytest.main(args))
