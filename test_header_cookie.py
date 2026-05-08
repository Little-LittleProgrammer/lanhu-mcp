#!/usr/bin/env python3
"""
测试 HTTP Header Cookie 功能
"""
import httpx
import json

# 测试配置
SERVER_URL = "http://localhost:8000/mcp"
TEST_COOKIE = "test_cookie_value_12345"

def test_header_cookie():
    """测试通过 Header 传入 Cookie"""
    print("🧪 测试 HTTP Header Cookie 功能\n")

    # 测试 1: 使用 X-Lanhu-Cookie header
    print("📝 测试 1: 使用 X-Lanhu-Cookie header")
    headers = {
        "X-Lanhu-Cookie": TEST_COOKIE,
        "Content-Type": "application/json"
    }

    try:
        response = httpx.get(
            f"{SERVER_URL}?role=Developer&name=TestUser",
            headers=headers,
            timeout=5.0
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 连接成功")
        else:
            print(f"   ❌ 连接失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")

    print()

    # 测试 2: 使用小写 header
    print("📝 测试 2: 使用小写 x-lanhu-cookie header")
    headers = {
        "x-lanhu-cookie": TEST_COOKIE,
        "Content-Type": "application/json"
    }

    try:
        response = httpx.get(
            f"{SERVER_URL}?role=Developer&name=TestUser",
            headers=headers,
            timeout=5.0
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 连接成功")
        else:
            print(f"   ❌ 连接失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")

    print()

    # 测试 3: 不使用 header（应该回退到环境变量）
    print("📝 测试 3: 不使用 header（回退到环境变量）")
    try:
        response = httpx.get(
            f"{SERVER_URL}?role=Developer&name=TestUser",
            timeout=5.0
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 连接成功（使用环境变量）")
        else:
            print(f"   ❌ 连接失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")

    print()
    print("=" * 50)
    print("测试完成！")
    print()
    print("💡 提示：")
    print("   - 如果所有测试都失败，请确保服务器正在运行")
    print("   - 运行服务器: docker-compose up -d")
    print("   - 查看日志: docker-compose logs -f lanhu-mcp")

if __name__ == "__main__":
    test_header_cookie()
