# 角色管理 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 5

# 📦 角色管理 (5 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. POST /api/role/create

**说明**: Create Role


**描述**: 创建角色


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/role/create'

```


### 返回


```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body"
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.4/v/missing"
    }
  ]
}
```



## 2. GET /api/role/list

**说明**: List Roles


**描述**: 获取角色列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/role/list'

```


### 返回


```
[{'name': '电商设计师', 'code': 'ECOMMERCE_DESIGNER', 'permission': 'design,manage_projects', 'is_active': True, 'id': 1}, {'name': '3D建模师', 'code': '3D_MODELER', 'permission': '3d_design,render', 'is_active': True, 'id': 2}, {'name': '项目经理', 'code': 'PROJECT_MANAGER', 'permission': 'manage_all,approve', 'is_active': True, 'id': 3}, {'name': '管理员', 'code': 'ADMIN', 'permission': 'system_admin', 'is_active': True, 'id': 4}]
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/role/{role_id}

**说明**: Get Role


**描述**: 获取角色详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/role/1'

```


### 返回


```json
{
  "name": "电商设计师",
  "code": "ECOMMERCE_DESIGNER",
  "permission": "design,manage_projects",
  "is_active": true,
  "id": 1
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| role_id | integer |  |




## 4. PUT /api/role/{role_id}

**说明**: Update Role


**描述**: 更新角色


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/role/1'

```


### 返回


```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body"
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.4/v/missing"
    }
  ]
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| role_id | integer |  |




## 5. DELETE /api/role/{role_id}

**说明**: Delete Role


**描述**: 删除角色


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/role/1'

```


### 返回


```json
{
  "message": "角色删除成功"
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| role_id | integer |  |


