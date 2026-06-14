---
purpose: 接口文档
content: API索引和接口维护规则
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# API接口索引


## 1. API分组

| 分组 | 路径前缀 | 说明 |
|---|---|---|
| 认证 | `/api/v1/auth` | 登录、当前用户、退出 |
| 瓷砖信息 | `/api/v1/tiles` | 瓷砖列表、详情、维护 |
| 媒体资源 | `/api/v1/media` | 图片、视频上传和查询 |
| 管理端 | `/api/v1/admin` | 管理端维护接口 |

## 2. 认证接口

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/v1/auth/login` | 账号密码登录，返回 JWT 与用户信息 |
| GET | `/api/v1/auth/me` | 获取当前登录用户（需 Bearer Token） |
| POST | `/api/v1/auth/logout` | 退出登录（需 Bearer Token） |

### 登录请求示例

```json
{
  "username": "admin",
  "password": "********",
  "remember_me": true
}
```

### 登录成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "access_token": "string",
    "token_type": "Bearer",
    "expires_in": 7200,
    "user": {
      "id": "uuid",
      "username": "admin",
      "display_name": "系统管理员",
      "role": "admin",
      "status": "active"
    }
  }
}
```

### 错误码

| HTTP | code | 场景 |
|---|---|---|
| 400 | 40001 | 参数无效 |
| 401 | 40101 | 账号或密码错误 |
| 401 | 40102 | 未登录或 token 无效 |
| 403 | 40301 | 用户被禁用 |
| 403 | 40302 | 无权限访问 |

## 3. OpenAPI

FastAPI 自动生成 OpenAPI：

```text
/openapi.json
/docs
```

前端通过 Orval 生成类型和接口调用代码。