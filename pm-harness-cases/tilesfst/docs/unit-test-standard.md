---
purpose: 单元测试标准
content: Service/Repository/工具层测试要求与示例
source: build-test-framework
update_method: 单元测试规范变更时同步更新
---

# 单元测试标准

## 必须测试

- Service 业务逻辑
- Repository 数据访问（可用内存 SQLite）
- Utility / 算法
- 错误码与常量

## 禁止

- 仅测 Router 而不测 Service
- 无断言的 smoke 占位长期保留

## 覆盖

每个函数至少：正常路径、异常路径、边界条件。

## 示例

```python
def test_tile_repository_list_published_empty(db_session):
    repo = TileRepository(db_session)
    items, total = repo.list_published()
    assert total == 0
    assert items == []
```

## 位置

- 根目录：`tests/unit/`
- 后端就近：`src/backend/tests/`
