# 用户管理 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 10

# 📦 用户管理 (10 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. GET /api/user/list

**说明**: Get User List


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/user/list'

```


### 返回


```
[{'username': 'testuser', 'name': '测试用户', 'phone': '13800138000', 'is_active': True, 'id': 1, 'create_time': '2025-12-01T12:42:59.467536', 'update_time': '2025-12-01T12:42:59.467538'}, {'username': 'project_test', 'name': '项目测试用户', 'phone': '13800000001', 'is_active': True, 'id': 2, 'create_time': '2025-12-01T12:54:35.409670', 'update_time': '2025-12-02T03:40:42.274930'}, {'username': 'test_user', 'name': 'Test User', 'phone': '13800000000', 'is_active': True, 'id': 3, 'create_time': '2025-12-02
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 2. POST /api/user/login

**说明**: User Login


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/user/login'

```


### 返回


```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "body",
        "username"
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.4/v/missing"
    },
    {
      "type": "missing",
      "loc": [
        "body",
        "password"
      ],
      "msg": "Field required",
      "input": null,
      "url": "https://errors.pydantic.dev/2.4/v/missing"
    }
  ]
}
```



## 3. POST /api/user/create

**说明**: Create User


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/user/create'
 \
  -H 'Content-Type: application/json' \
  -d '{"username": "test123", "password": "pass123"}'

```


### 返回


```json
{
  "username": "test123",
  "name": null,
  "phone": null,
  "is_active": true,
  "id": 4,
  "create_time": "2025-12-02T11:24:13.621851",
  "update_time": "2025-12-02T11:24:13.621853"
}
```



## 4. GET /api/user/me

**说明**: Read Current User


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/user/me'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.630417"
  },
  "data": null
}
```



## 5. POST /api/user/assign_role/{user_id}

**说明**: Assign User Role


**描述**: 为用户分配角色


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/user/assign_role/1'

```


### 返回


```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "role_id"
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

| user_id | integer |  |

| role_id | integer |  |




## 6. DELETE /api/user/revoke_role/{user_id}

**说明**: Revoke User Role


**描述**: 取消用户角色


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/user/revoke_role/1'

```


### 返回


```json
{
  "detail": [
    {
      "type": "missing",
      "loc": [
        "query",
        "role_id"
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

| user_id | integer |  |

| role_id | integer |  |




## 7. GET /api/user/{user_id}/roles

**说明**: Get User Roles List


**描述**: 获取用户的所有角色


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/user/1/roles'

```


### 返回


```json
{
  "user_id": 1,
  "roles": [
    {
      "id": 2,
      "name": "3D建模师",
      "code": "3D_MODELER",
      "permission": "3d_design,render",
      "is_active": true
    },
    {
      "id": 3,
      "name": "项目经理",
      "code": "PROJECT_MANAGER",
      "permission": "manage_all,approve",
      "is_active": true
    }
  ]
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| user_id | integer |  |




## 8. POST /api/user/change-password

**说明**: Change Password


**描述**: 修改当前用户的密码


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/user/change-password'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.659726"
  },
  "data": null
}
```



## 9. POST /api/user/admin/reset-password/{user_id}

**说明**: Admin Reset Password


**描述**: 管理员重置用户密码


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/user/admin/reset-password/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.666288"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| user_id | integer |  |

| new_password | string |  |




## 10. POST /api/user/admin/reset-password-by-username

**说明**: Admin Reset Password By Username


**描述**: 管理员通过用户名重置密码


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/user/admin/reset-password-by-username'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.672442"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| username | string |  |

| new_password | string |  |


