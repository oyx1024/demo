"""日志封装"""
import sys
import logging
from pathlib import Path
from config.config import config


def setup_logger(name: str = "api_test") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))
    logger.handlers.clear()

    # 控制台输出
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s  %(levelname)-5s  %(message)s",
        datefmt="%H:%M:%S"
    )
    console.setFormatter(fmt)
    logger.addHandler(console)

    # 文件输出
    log_dir = Path(__file__).resolve().parent.parent / "reports"
    log_dir.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_dir / "test_run.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s  %(levelname)-5s  %(filename)s:%(lineno)d  %(message)s"
    ))
    logger.addHandler(fh)

    return logger


logger = setup_logger()
