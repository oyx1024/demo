"""pytest 全局 fixture"""
import pytest
from common.client import ApiClient
from common.logger import logger
from common.global_vars import GlobalVars as G


@pytest.fixture
def api():
    """每个测试用例获取一个 ApiClient 实例"""
    return ApiClient()


@pytest.fixture(scope="session", autouse=True)
def session_setup():
    logger.info("=" * 50)
    logger.info("  接口测试开始")
    logger.info("=" * 50)
    yield
    logger.info("=" * 50)
    logger.info("  接口测试结束")
    logger.info("=" * 50)
    G.clear()


# ── 全局变量 使用示例 ──────────────────────────

@pytest.fixture(scope="session")
def auth_token(api) -> str:
    """模拟登录：获取 token 并存入全局变量"""
    resp = api.post("/post", json={"username": "admin", "password": "123456"})
    token = resp.json().get("token", "mock-token-abc123")

    # 存入全局变量，后续用例可直接读取
    G.set("token", token)
    logger.info(f"🔑 Token 已存入全局变量: {token[:20]}...")
    return token


@pytest.fixture(scope="session", autouse=True)
def load_global_config():
    """将 config.yaml 中的关键配置注入全局变量，方便用例直接引用"""
    from config.config import config
    G.set("base_url", config.base_url)
    G.set("timeout", config.timeout)
    # 环境标识
    if "prod" in config.base_url.lower():
        G.set("env", "production")
    elif "test" in config.base_url.lower() or "httpbin" in config.base_url.lower():
        G.set("env", "testing")
    else:
        G.set("env", "unknown")
    logger.info(f"🌍 环境标识已注入全局变量: env={G.get('env')}")
