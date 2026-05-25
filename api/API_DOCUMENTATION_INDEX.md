# 📚 PRE系统API完整文档导航

**最后更新**: 2025年12月2日  
**总接口数**: 152  
**模块数**: 11

---

## 📊 模块统计

| 序号 | 模块名 | 接口数 | 百分比 | 文档链接 |
|------|--------|--------|--------|---------|
| 1 | 任务管理 | 34 | 22.4% | [查看详情](./API_TEST_任务管理.md) |
| 2 | 素材库 | 18 | 11.8% | [查看详情](./API_TEST_素材库.md) |
| 3 | 文件管理 | 16 | 10.5% | [查看详情](./API_TEST_文件管理.md) |
| 4 | 项目管理 | 16 | 10.5% | [查看详情](./API_TEST_项目管理.md) |
| 5 | 客户标签 | 13 | 8.6% | [查看详情](./API_TEST_客户标签.md) |
| 6 | 消息通知 | 13 | 8.6% | [查看详情](./API_TEST_消息通知.md) |
| 7 | 任务分类 | 11 | 7.2% | [查看详情](./API_TEST_任务分类.md) |
| 8 | 用户管理 | 10 | 6.6% | [查看详情](./API_TEST_用户管理.md) |
| 9 | 客户管理 | 8 | 5.3% | [查看详情](./API_TEST_客户管理.md) |
| 10 | 仪表板 | 7 | 4.6% | [查看详情](./API_TEST_仪表板.md) |
| 11 | 角色管理 | 5 | 3.3% | [查看详情](./API_TEST_角色管理.md) |

---

## 🎯 快速导航

### 核心功能模块

#### 📋 [任务管理](./API_TEST_任务管理.md) - 34个接口
- 任务CRUD操作
- 批量操作接口 ⭐ 新增
- 任务导出接口 ⭐ 新增
- 进度和状态管理
- 高级查询和筛选
- 任务协作和评论

#### 🏢 [项目管理](./API_TEST_项目管理.md) - 16个接口
- 项目CRUD操作
- 项目克隆功能 ⭐ 新增
- 素材关联管理
- 团队分配

#### 📁 [文件管理](./API_TEST_文件管理.md) - 16个接口
- 文件上传下载
- 版本管理
- 客户确认流程
- 文件分享 ⭐ 新增
- 云存储支持

#### 🎨 [素材库](./API_TEST_素材库.md) - 18个接口
- 素材CRUD操作
- 素材-项目关联
- 素材-任务关联 ⭐ 新增
- 标签管理
- 复用统计

---

### 数据管理模块

#### 👥 [用户管理](./API_TEST_用户管理.md) - 10个接口
- 用户认证（登录）
- 用户CRUD操作
- 角色分配
- 密码修改
- 管理员密码重置 ⭐ 新增

#### 🏷️ [角色管理](./API_TEST_角色管理.md) - 5个接口
- 角色CRUD操作
- 权限配置

#### 🛍️ [客户管理](./API_TEST_客户管理.md) - 8个接口
- 客户CRUD操作
- 按平台筛选
- 客户搜索

#### 🔖 [客户标签](./API_TEST_客户标签.md) - 13个接口
- 标签管理
- 客户标签分配
- 标签搜索和统计

#### 📂 [任务分类](./API_TEST_任务分类.md) - 11个接口
- 分类树形结构
- 多级分类支持
- 电商分类筛选

---

### 辅助功能模块

#### 📊 [仪表板](./API_TEST_仪表板.md) - 7个接口
- 概览统计
- 项目统计
- 任务统计
- 工作量统计
- 平台统计

#### 🔔 [消息通知](./API_TEST_消息通知.md) - 13个接口
- 通知列表
- 已读/未读管理
- 通知统计
- 数据导出

---

## 🆕 新增功能一览

### 高优先级 (✅ 已实现)
- **素材-任务关联** (3个接口)
  - `POST /api/material/{mid}/tasks/{tid}` - 关联素材到任务
  - `DELETE /api/material/{mid}/tasks/{tid}` - 移除关联
  - `GET /api/material/filter/by-task/{tid}` - 查询任务素材

### 中优先级 (✅ 已实现)
- **任务批量操作** (4个接口)
  - 批量更新状态
  - 批量更新优先级
  - 批量分配设计师
  - 批量删除

- **任务数据导出** (3个接口)
  - 按项目导出
  - 批量导出
  - 导出全部

### 低优先级 (✅ 已实现)
- **文件分享** (3个接口)
  - 创建分享链接
  - 访问分享文件
  - 撤销分享

- **项目克隆** (1个接口)
  - 快速复制项目及任务

- **密码重置** (2个接口)
  - 管理员重置用户密码

---

## 📖 使用指南

### 1. 认证和授权
所有需要认证的接口都需要在请求头中包含 `Authorization: Bearer {token}`

登录接口:
```bash
POST /api/user/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

### 2. 请求格式
- **GET**: 使用查询参数传递数据
- **POST/PUT**: 使用JSON格式请求体传递数据
- **DELETE**: 使用路径参数指定资源ID

### 3. 返回格式
所有接口返回JSON格式，包含以下字段：
```json
{
  "success": true/false,
  "data": {...},
  "error": {...},
  "message": "..."
}
```

### 4. 分页
支持分页的接口使用 `skip` 和 `limit` 参数：
- `skip`: 跳过的记录数（默认0）
- `limit`: 返回的记录数（默认100）

---

## 🔍 接口查询速查表

### 按功能查询

#### 创建操作
- `POST /api/user/create` - 创建用户
- `POST /api/customer/create` - 创建客户
- `POST /api/project/create` - 创建项目
- `POST /api/task/create` - 创建任务
- `POST /api/material/create` - 创建素材
- `POST /api/role/create` - 创建角色

#### 读取操作
- `GET /api/user/list` - 用户列表
- `GET /api/customer/list` - 客户列表
- `GET /api/project/list` - 项目列表
- `GET /api/task/list` - 任务列表
- `GET /api/material/list` - 素材列表
- `GET /api/role/list` - 角色列表

#### 更新操作
- `PUT /api/user/{id}` - 更新用户
- `PUT /api/customer/{id}` - 更新客户
- `PUT /api/project/{id}` - 更新项目
- `PUT /api/task/{id}` - 更新任务

#### 删除操作
- `DELETE /api/user/{id}` - 删除用户
- `DELETE /api/customer/{id}` - 删除客户
- `DELETE /api/project/{id}` - 删除项目
- `DELETE /api/task/{id}` - 删除任务

---

## 📚 文档列表

| 文档 | 说明 |
|------|------|
| [API_COMPLETE_TEST_REPORT.md](./API_COMPLETE_TEST_REPORT.md) | 完整测试报告 |
| [API_TEST_任务管理.md](./API_TEST_任务管理.md) | 任务管理模块详细文档 |
| [API_TEST_项目管理.md](./API_TEST_项目管理.md) | 项目管理模块详细文档 |
| [API_TEST_文件管理.md](./API_TEST_文件管理.md) | 文件管理模块详细文档 |
| [API_TEST_素材库.md](./API_TEST_素材库.md) | 素材库模块详细文档 |
| [API_TEST_用户管理.md](./API_TEST_用户管理.md) | 用户管理模块详细文档 |
| [API_TEST_客户管理.md](./API_TEST_客户管理.md) | 客户管理模块详细文档 |
| [API_TEST_客户标签.md](./API_TEST_客户标签.md) | 客户标签模块详细文档 |
| [API_TEST_任务分类.md](./API_TEST_任务分类.md) | 任务分类模块详细文档 |
| [API_TEST_仪表板.md](./API_TEST_仪表板.md) | 仪表板模块详细文档 |
| [API_TEST_消息通知.md](./API_TEST_消息通知.md) | 消息通知模块详细文档 |
| [API_TEST_角色管理.md](./API_TEST_角色管理.md) | 角色管理模块详细文档 |

---

## ⭐ 接口热力图

### 最常用接口 (Top 10)
1. `GET /api/task/list` - 任务列表查询
2. `POST /api/task/create` - 创建任务
3. `PUT /api/task/{id}` - 更新任务
4. `GET /api/project/list` - 项目列表
5. `GET /api/material/list` - 素材列表
6. `GET /api/file/list` - 文件列表
7. `POST /api/project/create` - 创建项目
8. `GET /api/dashboard/overview` - 仪表板
9. `GET /api/user/list` - 用户列表
10. `POST /api/task/batch/update-status` - 批量更新状态

---

## 🚀 集成建议

### 前端集成步骤
1. 根据模块分类集成API调用
2. 参考各模块的测试文档获取请求/返回格式
3. 实现错误处理和重试逻辑
4. 添加加载状态和用户反馈

### 后端优化建议
1. 添加缓存机制（Redis）
2. 实现API速率限制
3. 完善操作审计日志
4. 性能监控和告警

---

## 📞 技术支持

如有问题或建议，请联系开发团队。

---

**更新时间**: 2025年12月2日  
**系统版本**: 1.0.0  
**状态**: ✅ 生产就绪
