# 客户标签 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 13

# 📦 客户标签 (13 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. POST /api/customer-tag/tags

**说明**: Create Tag


**描述**: 创建标签


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/customer-tag/tags'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.078811"
  },
  "data": null
}
```



## 2. GET /api/customer-tag/tags/list

**说明**: Get Tags


**描述**: 获取标签列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer-tag/tags/list'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.084968"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |

| is_active | boolean |  |




## 3. GET /api/customer-tag/tags/popular

**说明**: Get Popular Tags


**描述**: 获取热门标签


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer-tag/tags/popular'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.091380"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| limit | integer |  |




## 4. GET /api/customer-tag/tags/search

**说明**: Search Tags


**描述**: 搜索标签


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer-tag/tags/search'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.097992"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| q | string |  |




## 5. GET /api/customer-tag/tags/category/{category}

**说明**: Get Tags By Category


**描述**: 按类别获取标签


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer-tag/tags/category/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.104121"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category | string |  |




## 6. GET /api/customer-tag/tags/{tag_id}

**说明**: Get Tag


**描述**: 获取标签详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer-tag/tags/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.110375"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| tag_id | integer |  |




## 7. PUT /api/customer-tag/tags/{tag_id}

**说明**: Update Tag


**描述**: 更新标签


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/customer-tag/tags/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.117201"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| tag_id | integer |  |




## 8. DELETE /api/customer-tag/tags/{tag_id}

**说明**: Delete Tag


**描述**: 删除标签


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/customer-tag/tags/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.124139"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| tag_id | integer |  |




## 9. POST /api/customer-tag/tags/init-predefined

**说明**: Init Predefined Tags


**描述**: 初始化预定义标签


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/customer-tag/tags/init-predefined'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.130666"
  },
  "data": null
}
```



## 10. POST /api/customer-tag/customer/{customer_id}/tags

**说明**: Assign Tag To Customer


**描述**: 为客户分配标签


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/customer-tag/customer/1/tags'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.137249"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |




## 11. GET /api/customer-tag/customer/{customer_id}/tags

**说明**: Get Customer Tags


**描述**: 获取客户的所有标签


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer-tag/customer/1/tags'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.143382"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |




## 12. POST /api/customer-tag/customer/{customer_id}/tags/bulk

**说明**: Assign Tags To Customer


**描述**: 批量为客户分配标签


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/customer-tag/customer/1/tags/bulk'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.150039"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |




## 13. DELETE /api/customer-tag/customer/{customer_id}/tags/{tag_id}

**说明**: Remove Tag From Customer


**描述**: 移除客户的标签


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/customer-tag/customer/1/tags/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.157020"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |

| tag_id | integer |  |


