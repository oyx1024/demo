"""读取 YAML 配置"""
import yaml
from pathlib import Path


class Config:
    def __init__(self, path: str = None):
        path = path or Path(__file__).parent / "config.yaml"
        with open(path, encoding="utf-8") as f:
            self._data = yaml.safe_load(f) or {}

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"配置项 '{name}' 不存在")

    def get(self, key, default=None):
        return self._data.get(key, default)


config = Config()
