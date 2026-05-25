# 文件管理 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 16

# 📦 文件管理 (16 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. POST /api/file/create

**说明**: Create File


**描述**: 创建文件记录


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/file/create'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.225546"
  },
  "data": null
}
```



## 2. GET /api/file/list

**说明**: List Files


**描述**: 获取文件列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/list'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.232501"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/file/{file_id}

**说明**: Get File


**描述**: 获取文件详情


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.239532"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |




## 4. DELETE /api/file/{file_id}

**说明**: Delete File


**描述**: 删除文件


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/file/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.246545"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |




## 5. GET /api/file/filter/by-task/{task_id}

**说明**: Get Files By Task


**描述**: 按任务查询文件


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/filter/by-task/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.253038"
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




## 6. GET /api/file/filter/by-type/{file_type}

**说明**: Get Files By Type


**描述**: 按文件类型查询


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/filter/by-type/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.259347"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_type | string |  |

| skip | integer |  |

| limit | integer |  |




## 7. POST /api/file/{task_id}/new-version

**说明**: Create New Version


**描述**: 创建新版本


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/file/1/new-version'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.265749"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 8. GET /api/file/{task_id}/versions

**说明**: Get File Versions


**描述**: 获取文件版本历史


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/1/versions'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.272493"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |

| name | string | 文件名称 |




## 9. PUT /api/file/{file_id}/confirm

**说明**: Confirm File


**描述**: 确认文件


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/file/1/confirm'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.278701"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |




## 10. GET /api/file/{task_id}/stats

**说明**: Get File Stats


**描述**: 获取任务文件统计


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/1/stats'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.285300"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | integer |  |




## 11. POST /api/file/upload

**说明**: Upload File


**描述**: 上传文件到云存储

支持多种存储类型 (local/s3)


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/file/upload'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.291810"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| task_id | string |  |

| material_id | string |  |

| storage_type | string |  |




## 12. GET /api/file/{file_id}/download

**说明**: Download File


**描述**: 下载文件

支持多种存储类型，自动识别并调用相应的下载方法


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/1/download'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.298587"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |




## 13. GET /api/file/{file_id}/info

**说明**: Get File Info


**描述**: 获取文件详细信息及下载 URL


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/1/info'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.305009"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |




## 14. POST /api/file/{file_id}/share

**说明**: Create Share Link


**描述**: 创建文件分享链接


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/file/1/share'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.311241"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |

| expiry_hours | integer |  |




## 15. DELETE /api/file/{file_id}/share

**说明**: Revoke Share Link


**描述**: 撤销文件分享链接


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/file/1/share'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.317755"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| file_id | integer |  |




## 16. GET /api/file/share/{share_token}

**说明**: Access Shared File


**描述**: 通过分享令牌访问文件


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/file/share/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "(sqlite3.OperationalError) no such column: files.storage_type\n[SQL: SELECT files.task_id AS files_task_id, files.material_id AS files_material_id, files.uploader_id AS files_uploader_id, files.name AS files_name, files.description AS files_description, files.url AS files_url, files.file_type AS files_file_type, files.file_format AS files_file_format, files.size AS files_size, files.storage_type AS files_storage_type, files.storage_key AS files_storage_key, files.version AS files_version, files.is_latest AS files_is_latest, files.is_confirm AS files_is_confirm, files.confirm_user_id AS files_confirm_user_id, files.confirm_time AS files_confirm_time, files.confirm_remark AS files_confirm_remark, files.share_token AS files_share_token, files.share_expiry AS files_share_expiry, files.is_shared AS files_is_shared, files.upload_time AS files_upload_time, files.is_active AS files_is_active, files.id AS files_id, files.create_time AS files_create_time, files.update_time AS files_update_time \nFROM files \nWHERE files.share_token = ? AND files.is_active = 1\n LIMIT ? OFFSET ?]\n[parameters: ('1', 1, 0)]\n(Background on this error at: https://sqlalche.me/e/20/e3q8)",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.326205"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| share_token | string |  |


