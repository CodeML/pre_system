# 任务管理 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 34

# 📦 任务管理 (34 个接口)

测试时间: 2025-12-02 19:24:12

---


## 1. POST /api/task/create

**说明**: Create Task


**描述**: 创建新任务


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/create'
 \
  -H 'Content-Type: application/json' \
  -d '{"name": "测试任务", "project_id": 1, "category_id": 1}'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.853934"
  },
  "data": null
}
```



## 2. GET /api/task/list

**说明**: List Tasks


**描述**: 获取任务列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/list'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.860583"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/task/{task_id}

**说明**: Get Task


**描述**: 获取任务详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.867264"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 4. PUT /api/task/{task_id}

**说明**: Update Task


**描述**: 更新任务信息


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/task/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.874179"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 5. DELETE /api/task/{task_id}

**说明**: Delete Task


**描述**: 删除任务（软删除）


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/task/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.881284"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 6. POST /api/task/batch/update-status

**说明**: Batch Update Status


**描述**: 批量更新任务状态


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/batch/update-status'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.887948"
  },
  "data": null
}
```



## 7. POST /api/task/batch/update-priority

**说明**: Batch Update Priority


**描述**: 批量更新任务优先级


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/batch/update-priority'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.894548"
  },
  "data": null
}
```



## 8. POST /api/task/batch/assign-designer

**说明**: Batch Assign Designer


**描述**: 批量分配设计师


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/batch/assign-designer'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.901464"
  },
  "data": null
}
```



## 9. POST /api/task/batch/delete

**说明**: Batch Delete Tasks


**描述**: 批量删除任务


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/batch/delete'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.907894"
  },
  "data": null
}
```



## 10. GET /api/task/export/by-project/{project_id}

**说明**: Export Tasks By Project


**描述**: 导出项目的所有任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/export/by-project/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.914409"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |




## 11. POST /api/task/export/batch

**说明**: Export Tasks Batch


**描述**: 批量导出任务


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/export/batch'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.920973"
  },
  "data": null
}
```



## 12. GET /api/task/export/all

**说明**: Export All Tasks


**描述**: 导出所有任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/export/all'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.928692"
  },
  "data": null
}
```



## 13. PUT /api/task/{task_id}/progress

**说明**: Update Task Progress


**描述**: 更新任务进度


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/task/1/progress'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.935153"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 14. PUT /api/task/{task_id}/status/{new_status}

**说明**: Update Task Status


**描述**: 更新任务状态


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/task/1/status/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.941446"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| new_status | string |  |




## 15. GET /api/task/filter/by-project/{project_id}

**说明**: Get Tasks By Project


**描述**: 按项目查询任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/filter/by-project/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.948152"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 16. GET /api/task/filter/by-category/{category_id}

**说明**: Get Tasks By Category


**描述**: 按分类查询任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/filter/by-category/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.954578"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 17. GET /api/task/filter/by-status/{status}

**说明**: Get Tasks By Status


**描述**: 按状态查询任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/filter/by-status/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.960599"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| status | string |  |

| skip | integer |  |

| limit | integer |  |




## 18. GET /api/task/filter/by-designer/{designer_id}

**说明**: Get Tasks By Designer


**描述**: 按设计师查询任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/filter/by-designer/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.966803"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| designer_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 19. GET /api/task/filter/by-priority/{priority}

**说明**: Get Tasks By Priority


**描述**: 按优先级查询任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/filter/by-priority/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.973185"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| priority | string |  |

| skip | integer |  |

| limit | integer |  |




## 20. GET /api/task/filter/by-role/{role_id}

**说明**: Get Tasks By Role


**描述**: 按角色查询任务（role_ids 包含该角色）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/filter/by-role/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.979562"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| role_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 21. POST /api/task/filter/advanced

**说明**: Filter Tasks Advanced


**描述**: 高级多条件筛选


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/filter/advanced'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.985979"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | string |  |

| category_id | string |  |

| status | string |  |

| priority | string |  |

| designer_id | string |  |

| role_id | string |  |

| skip | integer |  |

| limit | integer |  |




## 22. POST /api/task/{task_id}/assign-designer/{designer_id}

**说明**: Assign Designer


**描述**: 分配设计师


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/1/assign-designer/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.992386"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| designer_id | integer |  |




## 23. POST /api/task/{task_id}/roles/{role_id}

**说明**: Add Role To Task


**描述**: 添加角色到任务


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/1/roles/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.999435"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| role_id | integer |  |




## 24. DELETE /api/task/{task_id}/roles/{role_id}

**说明**: Remove Role From Task


**描述**: 从任务移除角色


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/task/1/roles/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.005883"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| role_id | integer |  |




## 25. PUT /api/task/{task_id}/ecommerce-params

**说明**: Update Ecommerce Params


**描述**: 更新任务电商参数


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/task/1/ecommerce-params'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.013654"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 26. POST /api/task/ecommerce/validate-params

**说明**: Validate Ecommerce Params Endpoint


**描述**: 校验电商参数


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/ecommerce/validate-params'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.020084"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| platform | string | 电商平台 |




## 27. GET /api/task/ecommerce/specs/{platform}

**说明**: Get Ecommerce Specs


**描述**: 获取电商平台规范


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/ecommerce/specs/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.026223"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| platform | string |  |

| image_type | string |  |




## 28. GET /api/task/ecommerce/suggest-params

**说明**: Get Suggested Params


**描述**: 获取推荐参数


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/ecommerce/suggest-params'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.032464"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| platform | string | 电商平台 |

| image_type | string | 图片类型 |




## 29. GET /api/task/special/overdue-tasks

**说明**: Get Overdue Tasks


**描述**: 获取逾期任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/special/overdue-tasks'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.038879"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 30. GET /api/task/special/upcoming-tasks

**说明**: Get Upcoming Tasks


**描述**: 获取即将到期的任务


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/special/upcoming-tasks'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.044929"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| days | integer | 天数 |

| skip | integer |  |

| limit | integer |  |




## 31. GET /api/task/project/{project_id}/progress

**说明**: Get Project Progress


**描述**: 获取项目整体进度


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/project/1/progress'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.051088"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |




## 32. POST /api/task/{task_id}/comments

**说明**: Create Task Comment


**描述**: 创建任务评论


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task/1/comments'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.057636"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 33. GET /api/task/{task_id}/comments

**说明**: List Task Comments


**描述**: 获取任务的评论列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task/1/comments'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.064261"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 34. DELETE /api/task/{task_id}/comments/{comment_id}

**说明**: Delete Task Comment


**描述**: 删除任务评论（作者或管理员）


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/task/1/comments/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.070527"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| comment_id | integer |  |


