## 1. 数据库与种子

- [x] 1.1 在 `src/backend/app/db/schema.sql` 新增 `users` 表（id、username、phone、email、password_hash、display_name、role、status、last_login_at、created_at、updated_at）
- [x] 1.2 在 `schema.sql` 预留 `login_logs` 表结构
- [x] 1.3 创建管理员种子脚本（读取 `ADMIN_INITIAL_PASSWORD` 环境变量）
- [x] 1.4 更新 `docs/04-database-design.md` 同步 users/login_logs 表说明

## 2. 后端 Security 与依赖

- [x] 2.1 在 `pyproject.toml` 添加 `passlib[bcrypt]`、`python-jose[cryptography]` 依赖
- [x] 2.2 实现 `src/backend/app/core/security.py`：密码哈希/校验、JWT 编解码
- [x] 2.3 实现 `src/backend/app/core/deps.py`：`get_current_user`、角色校验依赖
- [x] 2.4 在 `src/backend/app/core/config.py` 添加 JWT 密钥、过期时间、ADMIN 种子配置

## 3. 后端 Auth 模块

- [x] 3.1 实现 `src/backend/app/schemas/auth.py`：LoginRequest、LoginResponse、UserProfile、AuthError
- [x] 3.2 实现 `src/backend/app/repositories/user_repository.py`：按 username 查询、更新 last_login_at
- [x] 3.3 实现 `src/backend/app/services/auth_service.py`：登录校验、token 签发、me 查询
- [x] 3.4 实现 `src/backend/app/api/v1/auth.py`：POST login、GET me、POST logout
- [x] 3.5 在 `src/backend/app/api/v1/router.py` 注册 auth 路由
- [x] 3.6 更新 `docs/03-api-index.md` 添加 auth 接口文档

## 4. 后端测试

- [x] 4.1 编写登录成功/失败/禁用用户集成测试
- [x] 4.2 编写 `/auth/me` 有效/无效 token 测试
- [x] 4.3 编写 `/auth/logout` 测试
- [x] 4.4 编写 store_owner 访问管理端 API 被拒绝测试

## 5. 前端 Auth Feature

- [x] 5.1 运行 `./scripts/generate-openapi-client.sh` 生成 auth API 客户端
- [x] 5.2 创建 `src/web/src/features/auth/types/auth.types.ts`
- [x] 5.3 创建 `src/web/src/features/auth/utils/auth-token.ts`（localStorage/sessionStorage 读写）
- [x] 5.4 创建 `src/web/src/features/auth/store/auth-store.ts`（Zustand 状态管理）
- [x] 5.5 创建 `src/web/src/features/auth/hooks/useAuth.ts`
- [x] 5.6 创建 `src/web/src/features/auth/components/PasswordInput.tsx`
- [x] 5.7 创建 `src/web/src/features/auth/components/AuthBrandPanel.tsx`（对齐原型左侧品牌区）
- [x] 5.8 创建 `src/web/src/features/auth/components/LoginForm.tsx`（校验、loading、错误提示）

## 6. 前端登录页与路由

- [x] 6.1 创建 `src/web/src/pages/admin/LoginPage.tsx`（左右分屏布局，对齐原型）
- [x] 6.2 创建 `src/web/src/app/router/ProtectedRoute.tsx`（鉴权 + 角色校验）
- [x] 6.3 配置路由：`/admin/login` 公开、`/admin/*` 受保护
- [x] 6.4 实现已登录访问 `/admin/login` 自动跳转 dashboard
- [x] 6.5 实现无权限页组件（store_owner / 权限不足场景）
- [x] 6.6 在管理端布局添加退出登录入口
- [x] 6.7 实现忘记密码、企业微信占位 Toast「功能建设中」
- [x] 6.8 准备登录页背景图静态资源

## 7. 前端测试

- [x] 7.1 编写 LoginForm 校验与提交测试
- [x] 7.2 编写 ProtectedRoute 未登录/已登录/token 过期测试
- [x] 7.3 编写 auth-store token 持久化测试

## 8. 集成验证与文档

- [x] 8.1 Docker Compose 环境验证：种子 admin → 登录 → dashboard → 退出
- [x] 8.2 验证错误账号、禁用账号、store_owner 拒绝场景
- [x] 8.3 更新 `issues/requirements/REQ-0001-user-login/trace.md` OpenSpec 状态为 in_progress
- [x] 8.4 运行 `python scripts/validate-directory-structure.py` 确认目录合规
