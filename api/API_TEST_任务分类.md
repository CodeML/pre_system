# 任务分类 模块API测试报告

生成时间: 2025-12-02 19:24:12
总接口数: 11

# 📦 任务分类 (11 个接口)

测试时间: 2025-12-02 19:24:12

---


## 1. POST /api/task-category/create

**说明**: Create Task Category


**描述**: 创建任务分类


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/task-category/create'
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
    "timestamp": "2025-12-02T11:24:12.769308"
  },
  "data": null
}
```



## 2. GET /api/task-category/list

**说明**: List Task Categories


**描述**: 获取所有任务分类


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/list'

```


### 返回


```
[{'parent_id': None, 'name': '电商设计', 'role_ids': [1], 'is_ecommerce': True, 'params': None, 'description': '更新后的分类描述', 'is_active': True, 'id': 1, 'create_time': '2025-12-01T12:50:55.127411', 'update_time': '2025-12-01T12:50:55.164423'}, {'parent_id': None, 'name': '3D设计', 'role_ids': [2], 'is_ecommerce': False, 'params': None, 'description': '3D建模和渲染任务', 'is_active': True, 'id': 2, 'create_time': '2025-12-01T12:50:55.131057', 'update_time': '2025-12-01T12:50:55.131058'}, {'parent_id': None, 'na
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/task-category/tree

**说明**: Get Category Tree


**描述**: 获取分类树结构（多级）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/tree'

```


### 返回


```
[{'id': 1, 'name': '电商设计', 'is_ecommerce': True, 'description': '更新后的分类描述', 'children': [{'id': 4, 'name': '主图设计', 'is_ecommerce': False, 'description': '商品主图设计', 'children': []}, {'id': 5, 'name': '详情页设计', 'is_ecommerce': False, 'description': '商品详情页设计', 'children': []}, {'id': 6, 'name': '海报设计', 'is_ecommerce': False, 'description': '营销海报设计', 'children': []}]}, {'id': 2, 'name': '3D设计', 'is_ecommerce': False, 'description': '3D建模和渲染任务', 'children': [{'id': 7, 'name': '产品建模', 'is_ecommerce': Fa
```



## 4. GET /api/task-category/{category_id}

**说明**: Get Task Category


**描述**: 获取分类详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/1'

```


### 返回


```json
{
  "parent_id": null,
  "name": "电商设计",
  "role_ids": [
    1
  ],
  "is_ecommerce": true,
  "params": null,
  "description": "更新后的分类描述",
  "is_active": true,
  "id": 1,
  "create_time": "2025-12-01T12:50:55.127411",
  "update_time": "2025-12-01T12:50:55.164423"
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category_id | integer |  |




## 5. PUT /api/task-category/{category_id}

**说明**: Update Task Category


**描述**: 更新任务分类


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/task-category/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.799022"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category_id | integer |  |




## 6. DELETE /api/task-category/{category_id}

**说明**: Delete Task Category


**描述**: 删除任务分类


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/task-category/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.808197"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category_id | integer |  |




## 7. GET /api/task-category/{category_id}/subcategories

**说明**: Get Subcategories


**描述**: 获取某个分类的所有子分类


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/1/subcategories'

```


### 返回


```
[{'parent_id': 1, 'name': '主图设计', 'role_ids': None, 'is_ecommerce': False, 'params': None, 'description': '商品主图设计', 'is_active': True, 'id': 4, 'create_time': '2025-12-01T12:50:55.136179', 'update_time': '2025-12-01T12:50:55.136180'}, {'parent_id': 1, 'name': '详情页设计', 'role_ids': None, 'is_ecommerce': False, 'params': None, 'description': '商品详情页设计', 'is_active': True, 'id': 5, 'create_time': '2025-12-01T12:50:55.139587', 'update_time': '2025-12-01T12:50:55.139588'}, {'parent_id': 1, 'name': '海报设
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category_id | integer |  |

| skip | integer |  |

| limit | integer |  |




## 8. GET /api/task-category/{category_id}/parents

**说明**: Get Parent Categories


**描述**: 获取分类的所有父分类（祖先链）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/1/parents'

```


### 返回


```
[]
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| category_id | integer |  |




## 9. GET /api/task-category/filter/ecommerce

**说明**: Filter Ecommerce Categories


**描述**: 获取所有电商设计分类


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/filter/ecommerce'

```


### 返回


```
[{'parent_id': None, 'name': '电商设计', 'role_ids': [1], 'is_ecommerce': True, 'params': None, 'description': '更新后的分类描述', 'is_active': True, 'id': 1, 'create_time': '2025-12-01T12:50:55.127411', 'update_time': '2025-12-01T12:50:55.164423'}]
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 10. GET /api/task-category/filter/my-accessible

**说明**: Get Accessible Categories


**描述**: 获取当前用户可操作的分类（按角色筛选）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/filter/my-accessible'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:12.839069"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 11. GET /api/task-category/level/{parent_id}

**说明**: Get Categories By Level


**描述**: 获取某一级的所有分类


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/task-category/level/1'

```


### 返回


```
[{'parent_id': 1, 'name': '主图设计', 'role_ids': None, 'is_ecommerce': False, 'params': None, 'description': '商品主图设计', 'is_active': True, 'id': 4, 'create_time': '2025-12-01T12:50:55.136179', 'update_time': '2025-12-01T12:50:55.136180'}, {'parent_id': 1, 'name': '详情页设计', 'role_ids': None, 'is_ecommerce': False, 'params': None, 'description': '商品详情页设计', 'is_active': True, 'id': 5, 'create_time': '2025-12-01T12:50:55.139587', 'update_time': '2025-12-01T12:50:55.139588'}, {'parent_id': 1, 'name': '海报设
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| parent_id | string |  |

| skip | integer |  |

| limit | integer |  |


