# 客户管理 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 8

# 📦 客户管理 (8 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. POST /api/customer/create

**说明**: Create Customer


**描述**: 创建客户（自动关联当前登录用户为创建人）


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/customer/create'
 \
  -H 'Content-Type: application/json' \
  -d '{"name": "测试客户", "platform": "淘宝"}'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.164143"
  },
  "data": null
}
```



## 2. GET /api/customer/list

**说明**: List Customers


**描述**: 获取客户列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer/list'

```


### 返回


```
[{'name': '淘宝店铺A', 'contact': '修改后的联系人', 'phone': '18800188001', 'type': 'company', 'ecommerce_platform': '淘宝', 'remark': '已更新备注信息', 'id': 1, 'creator_id': 1, 'create_time': '2025-12-01T12:45:28.589163', 'update_time': '2025-12-01T12:45:28.608854'}, {'name': '抖音品牌B', 'contact': '李四', 'phone': '13800138002', 'type': 'brand', 'ecommerce_platform': '抖音', 'remark': '新兴美妆品牌', 'id': 2, 'creator_id': 1, 'create_time': '2025-12-01T12:45:28.592610', 'update_time': '2025-12-01T12:45:28.592611'}, {'name': 
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/customer/{customer_id}

**说明**: Get Customer


**描述**: 获取客户详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer/1'

```


### 返回


```json
{
  "name": "淘宝店铺A",
  "contact": "修改后的联系人",
  "phone": "18800188001",
  "type": "company",
  "ecommerce_platform": "淘宝",
  "remark": "已更新备注信息",
  "id": 1,
  "creator_id": 1,
  "create_time": "2025-12-01T12:45:28.589163",
  "update_time": "2025-12-01T12:45:28.608854"
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |




## 4. PUT /api/customer/{customer_id}

**说明**: Update Customer


**描述**: 更新客户信息（仅创建人可编辑）


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/customer/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.185884"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |




## 5. DELETE /api/customer/{customer_id}

**说明**: Delete Customer


**描述**: 删除客户（仅创建人可删除）


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/customer/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.192847"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| customer_id | integer |  |




## 6. GET /api/customer/filter/platform/{platform}

**说明**: Filter By Platform


**描述**: 按电商平台筛选客户（支持：淘宝/抖音/小红书/Amazon等）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer/filter/platform/1'

```


### 返回


```
[]
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| platform | string |  |

| skip | integer |  |

| limit | integer |  |




## 7. GET /api/customer/search/name/{name}

**说明**: Search By Name


**描述**: 按客户名称模糊搜索


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer/search/name/1'

```


### 返回


```
[]
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| name | string |  |

| skip | integer |  |

| limit | integer |  |




## 8. GET /api/customer/creator/{creator_id}

**说明**: Get Customers By Creator


**描述**: 获取特定设计总监的所有客户


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/customer/creator/1'

```


### 返回


```
[{'name': '淘宝店铺A', 'contact': '修改后的联系人', 'phone': '18800188001', 'type': 'company', 'ecommerce_platform': '淘宝', 'remark': '已更新备注信息', 'id': 1, 'creator_id': 1, 'create_time': '2025-12-01T12:45:28.589163', 'update_time': '2025-12-01T12:45:28.608854'}, {'name': '抖音品牌B', 'contact': '李四', 'phone': '13800138002', 'type': 'brand', 'ecommerce_platform': '抖音', 'remark': '新兴美妆品牌', 'id': 2, 'creator_id': 1, 'create_time': '2025-12-01T12:45:28.592610', 'update_time': '2025-12-01T12:45:28.592611'}, {'name': 
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| creator_id | integer |  |

| skip | integer |  |

| limit | integer |  |


