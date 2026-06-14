---
purpose: 鉴权规范
content: JWT 签发、传递与路由守卫约定
source: rules/security.md / build-api-standard
update_method: 认证方案变更时同步更新
---

# 鉴权规范

## 机制

- 协议：JWT（HS256，`APP_SECRET_KEY`）
- 传递：`Authorization: Bearer <access_token>`
- 禁止混用：`token=` query、`sessionId` header 等

## 登录

```http
POST /api/v1/auth/login
Content-Type: application/json

{ "username": "...", "password": "...", "remember_me": false }
```

成功 `data` 含 `access_token`、`token_type`、`expires_in`、`user`。

## 受保护接口

后端使用 `get_current_user` 依赖；前端 Axios 拦截器附加 Bearer。

## 角色

| 角色 | 说明 |
|------|------|
| admin | 系统管理员 |
| employee | 企业内部员工 |
| store_owner | 店主（预留） |

## 错误码

见 `docs/error-codes.md` 2xxxx 段。

## 前端

- 登录态：`features/auth`
- 路由守卫：管理端 `/admin/*` 需已登录
