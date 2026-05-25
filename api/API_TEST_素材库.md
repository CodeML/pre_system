# 素材库 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 18

# 📦 素材库 (18 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. POST /api/material/create

**说明**: Create Material


**描述**: 创建素材


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/material/create'
 \
  -H 'Content-Type: application/json' \
  -d '{"name": "测试素材", "type": "icon", "url": "http://example.com/icon.png"}'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.679164"
  },
  "data": null
}
```



## 2. GET /api/material/list

**说明**: List Materials


**描述**: 获取素材列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/list'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.685820"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/material/statistics

**说明**: Get Material Stats


**描述**: 获取素材库统计


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/statistics'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.692513"
  },
  "data": null
}
```



## 4. GET /api/material/filter/popular

**说明**: Get Popular Materials


**描述**: 获取热门素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/popular'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.699410"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| limit | integer |  |




## 5. GET /api/material/filter/reusable

**说明**: Get Reusable Materials


**描述**: 获取可复用素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/reusable'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.705962"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 6. GET /api/material/filter/by-type/{material_type}

**说明**: Get Materials By Type


**描述**: 按类型查询素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/by-type/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.713015"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_type | string |  |

| skip | integer |  |

| limit | integer |  |




## 7. GET /api/material/filter/by-category/{category}

**说明**: Get Materials By Category


**描述**: 按分类查询素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/by-category/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.719218"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category | string |  |

| skip | integer |  |

| limit | integer |  |




## 8. GET /api/material/filter/by-tag/{tag}

**说明**: Get Materials By Tag


**描述**: 按标签查询素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/by-tag/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.725618"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| tag | string |  |

| skip | integer |  |

| limit | integer |  |




## 9. GET /api/material/filter/by-project/{project_id}

**说明**: Get Materials By Project


**描述**: 获取项目关联的素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/by-project/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.732065"
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




## 10. GET /api/material/filter/by-task/{task_id}

**说明**: Get Materials By Task


**描述**: 获取任务关联的素材


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/filter/by-task/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.738500"
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




## 11. GET /api/material/{material_id}

**说明**: Get Material


**描述**: 获取素材详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/material/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.745178"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |




## 12. PUT /api/material/{material_id}

**说明**: Update Material


**描述**: 更新素材


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/material/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.751635"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |




## 13. DELETE /api/material/{material_id}

**说明**: Delete Material


**描述**: 删除素材


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/material/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.758383"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |




## 14. POST /api/material/{material_id}/tasks/{task_id}

**说明**: Add Task To Material


**描述**: 关联素材到任务


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/material/1/tasks/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.765229"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |

| task_id | integer |  |




## 15. DELETE /api/material/{material_id}/tasks/{task_id}

**说明**: Remove Task From Material


**描述**: 移除素材与任务的关联


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/material/1/tasks/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.771776"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |

| task_id | integer |  |




## 16. POST /api/material/{material_id}/tags/{tag}

**说明**: Add Tag To Material


**描述**: 为素材添加标签


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/material/1/tags/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.777976"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |

| tag | string |  |




## 17. DELETE /api/material/{material_id}/tags/{tag}

**说明**: Remove Tag From Material


**描述**: 删除素材标签


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/material/1/tags/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.784385"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |

| tag | string |  |




## 18. POST /api/material/{material_id}/use

**说明**: Increment Material Reuse


**描述**: 记录素材使用次数


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/material/1/use'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.790973"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| material_id | integer |  |


