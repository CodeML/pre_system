# 项目管理 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 16

# 📦 项目管理 (16 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. POST /api/project/create

**说明**: Create Project


**描述**: 创建新项目


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/project/create'
 \
  -H 'Content-Type: application/json' \
  -d '{"name": "测试项目", "customer_id": 1, "type": "电商"}'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.833405"
  },
  "data": null
}
```



## 2. GET /api/project/list

**说明**: List Projects


**描述**: 获取项目列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/list'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.840128"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/project/{project_id}

**说明**: Get Project


**描述**: 获取项目详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.846747"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |




## 4. PUT /api/project/{project_id}

**说明**: Update Project


**描述**: 更新项目信息


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/project/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.853542"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |




## 5. DELETE /api/project/{project_id}

**说明**: Delete Project


**描述**: 删除项目（软删除）


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/project/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.860416"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |




## 6. POST /api/project/{project_id}/clone

**说明**: Clone Project


**描述**: 克隆项目（包括任务和素材关联）


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/project/1/clone'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.867204"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |

| new_name | string |  |




## 7. GET /api/project/filter/by-customer/{customer_id}

**说明**: Get Projects By Customer


**描述**: 按客户查询项目


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/filter/by-customer/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.874412"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 8. GET /api/project/filter/by-status/{status}

**说明**: Get Projects By Status


**描述**: 按状态查询项目（待启动/设计中/待确认/已交付/已完结）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/filter/by-status/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.881691"
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




## 9. GET /api/project/filter/by-type/{project_type}

**说明**: Get Projects By Type


**描述**: 按项目类型查询（电商详情页/3D建模/摄影）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/filter/by-type/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.888540"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_type | string |  |

| skip | integer |  |

| limit | integer |  |




## 10. GET /api/project/filter/by-platform/{platform}

**说明**: Get Projects By Platform


**描述**: 按电商平台查询（淘宝/抖音/小红书/Amazon等）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/filter/by-platform/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.895346"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| platform | string |  |

| skip | integer |  |

| limit | integer |  |




## 11. GET /api/project/filter/by-designer/{designer_id}

**说明**: Get Projects By Designer


**描述**: 获取设计师相关的项目（主设计师或辅助设计师）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/project/filter/by-designer/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.901949"
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




## 12. POST /api/project/filter/advanced

**说明**: Filter Projects Advanced


**描述**: 高级多条件筛选


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/project/filter/advanced'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.908609"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | string |  |

| status | string |  |

| project_type | string |  |

| platform | string |  |

| designer_id | string |  |

| skip | integer |  |

| limit | integer |  |




## 13. PUT /api/project/{project_id}/status/{new_status}

**说明**: Update Project Status


**描述**: 更新项目状态


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/project/1/status/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.915812"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |

| new_status | string |  |




## 14. POST /api/project/{project_id}/assign-designers

**说明**: Assign Designers


**描述**: 分配项目设计师


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/project/1/assign-designers'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.922558"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |

| main_designer_id | string |  |

| assist_designer_id | string |  |




## 15. POST /api/project/{project_id}/materials/{material_id}

**说明**: Add Material To Project


**描述**: 添加素材到项目


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/project/1/materials/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.929450"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |

| material_id | integer |  |




## 16. DELETE /api/project/{project_id}/materials/{material_id}

**说明**: Remove Material From Project


**描述**: 从项目移除素材


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/project/1/materials/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.935866"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| project_id | integer |  |

| material_id | integer |  |


