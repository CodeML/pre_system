# 仪表板 模块API测试报告

生成时间: 2025-12-02 19:24:12
总接口数: 7

# 📦 仪表板 (7 个接口)

测试时间: 2025-12-02 19:24:12

---


## 1. GET /api/dashboard/overview

**说明**: Get Dashboard Overview


**描述**: 获取仪表板概览


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/overview'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.719406"
  },
  "data": null
}
```



## 2. GET /api/dashboard/full

**说明**: Get Full Dashboard


**描述**: 获取完整仪表板


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/full'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.727165"
  },
  "data": null
}
```



## 3. GET /api/dashboard/projects

**说明**: Get Project Stats


**描述**: 获取项目统计


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/projects'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.734246"
  },
  "data": null
}
```



## 4. GET /api/dashboard/tasks

**说明**: Get Task Stats


**描述**: 获取任务统计


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/tasks'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.740891"
  },
  "data": null
}
```



## 5. GET /api/dashboard/workload/designer

**说明**: Get Workload By Designer


**描述**: 按设计师统计工作量


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/workload/designer'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.747873"
  },
  "data": null
}
```



## 6. GET /api/dashboard/workload/role

**说明**: Get Workload By Role


**描述**: 按角色统计工作量


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/workload/role'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.754312"
  },
  "data": null
}
```



## 7. GET /api/dashboard/platforms

**说明**: Get Platform Stats


**描述**: 按电商平台统计


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/dashboard/platforms'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.761692"
  },
  "data": null
}
```

