# 通过 HTTP Header 传入 Cookie 配置指南

## 概述

蓝湖 MCP 服务器现在支持通过 HTTP Header 传入 Cookie，无需在服务器端配置环境变量。

## 配置优先级

1. **HTTP Header** (最高优先级)
2. **环境变量** (LANHU_COOKIE)
3. **默认值** (需要手动替换)


## 客户端配置方式

### 方式一：Claude Desktop (推荐)

编辑配置文件：
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp?role=Backend&name=John",
      "headers": {
        "X-Lanhu-Cookie": "你的蓝湖cookie值"
      }
    }
  }
}
```

### 方式二：Cursor

在 Cursor 的 MCP 配置中：

```json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp?role=开发&name=张三",
      "headers": {
        "X-Lanhu-Cookie": "你的蓝湖cookie值"
      }
    }
  }
}
```

### 方式三：其他 MCP 客户端

如果客户端不支持 `headers` 字段，可以继续使用环境变量方式：

```bash
# 通过 .env 文件
LANHU_COOKIE="你的蓝湖cookie值"

# 或通过 docker-compose.yml
environment:
  - LANHU_COOKIE=你的蓝湖cookie值
```

## 支持的 Header 名称

以下 Header 名称都可以使用（不区分大小写）：

- `X-Lanhu-Cookie`
- `x-lanhu-cookie`
- `lanhu-cookie`

## 获取蓝湖 Cookie

1. 打开浏览器，访问 [蓝湖官网](https://lanhuapp.com)
2. 登录你的账号
3. 打开浏览器开发者工具（F12）
4. 切换到 Network（网络）标签
5. 刷新页面，选择任意请求
6. 在 Request Headers 中找到 `Cookie` 字段
7. 复制完整的 Cookie 值

详细教程：[GET-COOKIE-TUTORIAL.md](./GET-COOKIE-TUTORIAL.md)

## 安全建议

### ✅ 推荐做法

1. **使用 Header 方式**：敏感信息不会出现在 URL 中
2. **定期更换 Cookie**：建议每月更换一次
3. **不要提交配置文件**：将包含 Cookie 的配置文件添加到 `.gitignore`
4. **使用环境变量**：在 CI/CD 环境中使用环境变量而非硬编码

### ❌ 不推荐做法

1. ~~不要通过 URL 参数传递 Cookie~~（已禁用此方式）
2. 不要将 Cookie 提交到代码仓库
3. 不要在公共场合分享包含 Cookie 的配置

## 示例：完整配置

```json
{
  "mcpServers": {
    "lanhu": {
      "url": "http://localhost:8000/mcp?role=Backend&name=John",
      "headers": {
        "X-Lanhu-Cookie": "sensorsdata2015jssdkcross=...; PHPSESSID=...; acw_tc=..."
      }
    }
  }
}
```

## 故障排查

### 问题：连接失败

**检查项**：

1. 服务器是否正常运行：`docker-compose ps`
2. 端口是否正确：默认 8000
3. Cookie 是否有效：在浏览器中测试

### 问题：认证失败

**解决方案**：

1. 重新获取 Cookie
2. 检查 Cookie 格式是否完整
3. 确认 Cookie 未过期

### 问题：Header 不生效

**可能原因**：

1. 客户端不支持 `headers` 字段
2. Header 名称拼写错误
3. 回退到环境变量方式


## 技术细节

### 实现原理

服务器在处理每个请求时：

1. 尝试从 HTTP Header 读取 Cookie
2. 如果 Header 中没有，则使用环境变量
3. 如果环境变量也没有，则使用默认值（需要手动配置）

### 代码位置

- 函数：`get_cookie_from_request()` (lanhu_mcp_server.py:2152)
- 调用位置：
  - `LanhuClient.__init__()` (lanhu_mcp_server.py:2335)
  - `_fetch_design_json_from_dds()` (lanhu_mcp_server.py:3338)
  - `_resolve_share_url()` (lanhu_mcp_server.py:3820)

## 更新日志

- **2026-05-08**: 新增 HTTP Header 支持，提升安全性
- **2026-05-08**: 禁用 URL 参数传递 Cookie（安全考虑）

## 相关文档

- [部署指南](./DEPLOY.md)
- [获取 Cookie 教程](./GET-COOKIE-TUTORIAL.md)
- [环境变量配置](./config.example.env)
