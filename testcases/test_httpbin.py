"""示范用例 — 使用 httpbin.org 作为测试目标"""
import pytest
from common.global_vars import GlobalVars as G


class TestHttpBin:

    def test_get(self, api):
        """GET 请求 — 演示从全局变量读取环境信息"""
        # 从全局变量获取信息
        env = G.get("env", "unknown")
        base = G.get("base_url", "https://httpbin.org")
        print(f"\n  当前环境: {env}, base_url: {base}")

        resp = api.get("/get", params={"name": "tester"})
        assert resp.status_code == 200
        args = resp.json()["args"]
        assert args["name"] == "tester"

    def test_post_json(self, api):
        """POST JSON body"""
        payload = {"key": "value"}
        resp = api.post("/post", json=payload)
        assert resp.status_code == 200
        assert resp.json()["json"] == payload

    @pytest.mark.parametrize("code", [200, 201, 404, 500])
    def test_status_code(self, api, code):
        """测试不同状态码"""
        resp = api.get(f"/status/{code}")
        assert resp.status_code == code

    def test_headers(self, api):
        """请求头回显"""
        resp = api.get("/headers")
        assert resp.status_code == 200

    def test_delay(self, api):
        """模拟延时接口（设置超时小于延时，验证超时捕获）"""
        try:
            api.get("/delay/3", timeout=2)
        except Exception as e:
            assert "Timeout" in str(type(e).__name__) or "timeout" in str(e).lower()

    def test_global_vars_demo(self):
        """演示 GlobalVars 的完整用法"""
        # 1. set / get（存 / 取）
        G.set("user_id", 1001)
        G.set("role", "admin")
        assert G.get("user_id") == 1001
        assert G.get("role") == "admin"

        # 2. 属性读写
        G.order_id = "ORD-20240301-001"
        assert G.order_id == "ORD-20240301-001"

        # 3. contains / keys / all
        assert G.contains("user_id")
        assert "role" in G.keys()
        all_vars = G.all()
        assert all_vars["user_id"] == 1001

        # 4. pop 取出即删
        val = G.pop("role")
        assert val == "admin"
        assert not G.contains("role")

        # 5. 跨用例传递 — 其他用例也能读到
        G.set("shared_data", {"created": True, "count": 99})
        print(f"\n  GlobalVars 当前内容: {G}")

    def test_read_shared_vars(self):
        """读取其他用例存入的全局变量"""
        # 如果 test_global_vars_demo 先执行，这里能读到 shared_data
        shared = G.get("shared_data", None)
        if shared:
            print(f"\n  读到跨用例数据: {shared}")
        else:
            print("\n  shared_data 尚未设置（可能执行顺序不同）")

        # 读取 fixture 注入的变量
        env = G.get("env", "unknown")
        assert env in ("testing", "production", "unknown")
        print(f"  当前环境: {env}")
