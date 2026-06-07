"""全局变量管理器 — 跨用例共享数据（token、环境信息等）

用法:
    from common.global_vars import GlobalVars as G

    # 存
    G.set("token", "abc123")
    G.set("user_id", 42)

    # 取（带默认值）
    token = G.get("token")
    uid = G.get("user_id", default=0)

    # 快捷属性访问
    G.token = "abc123"
    print(G.token)         # "abc123"

    # 清空 / 检查
    G.contains("token")    # True
    G.clear()
"""
from typing import Any, Optional


class _GlobalVars:
    """全局变量存储（单例）"""

    def __init__(self):
        self._store: dict[str, Any] = {}

    # ── 基础读写 ──────────────────────────────

    def set(self, key: str, value: Any) -> None:
        """设置全局变量"""
        self._store[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """获取全局变量，不存在返回 default"""
        return self._store.get(key, default)

    def pop(self, key: str, default: Optional[Any] = None) -> Any:
        """取出并移除变量"""
        return self._store.pop(key, default)

    def contains(self, key: str) -> bool:
        """检查变量是否存在"""
        return key in self._store

    def clear(self) -> None:
        """清空所有全局变量"""
        self._store.clear()

    def keys(self) -> list[str]:
        """返回所有变量名"""
        return list(self._store.keys())

    def all(self) -> dict[str, Any]:
        """返回全部变量副本"""
        return self._store.copy()

    # ── 属性访问支持 ─────────────────────────

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._store:
            return self._store[name]
        raise AttributeError(f"全局变量 '{name}' 不存在，请先使用 set('{name}', value) 赋值")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._store[name] = value

    def __delattr__(self, name: str) -> None:
        if name in self._store:
            del self._store[name]
        else:
            raise AttributeError(f"全局变量 '{name}' 不存在")

    def __repr__(self) -> str:
        items = ", ".join(f"{k}={v!r}" for k, v in self._store.items())
        return f"GlobalVars({items})"


# 模块级单例 — 整个进程共享同一个实例
GlobalVars = _GlobalVars()
