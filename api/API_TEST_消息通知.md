# 消息通知 模块API测试报告

生成时间: 2025-12-02 19:24:13
总接口数: 13

# 📦 消息通知 (13 个接口)

测试时间: 2025-12-02 19:24:13

---


## 1. GET /api/notification/list

**说明**: Get Notifications


**描述**: 获取当前用户的通知列表


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/list'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.333769"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 2. GET /api/notification/unread

**说明**: Get Unread Notifications


**描述**: 获取未读通知


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/unread'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.340525"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| skip | integer |  |

| limit | integer |  |




## 3. GET /api/notification/unread-count

**说明**: Get Unread Count


**描述**: 获取未读通知数


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/unread-count'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.347362"
  },
  "data": null
}
```



## 4. PUT /api/notification/{notification_id}/read

**说明**: Mark Notification As Read


**描述**: 标记通知为已读


### 请求


```bash
curl -X PUT 'http://127.0.0.1:8000/api/notification/1/read'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.353993"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| notification_id | integer |  |




## 5. POST /api/notification/read-all

**说明**: Mark All As Read


**描述**: 标记所有通知为已读


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/notification/read-all'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.360551"
  },
  "data": null
}
```



## 6. GET /api/notification/filter/by-type/{notification_type}

**说明**: Get Notifications By Type


**描述**: 按类型查询通知


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/filter/by-type/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.367137"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| notification_type | string |  |

| skip | integer |  |

| limit | integer |  |




## 7. GET /api/notification/filter/by-priority/{priority}

**说明**: Get Notifications By Priority


**描述**: 按优先级查询通知


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/filter/by-priority/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.373813"
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




## 8. GET /api/notification/statistics

**说明**: Get Notification Statistics


**描述**: 获取通知统计


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/statistics'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.380416"
  },
  "data": null
}
```



## 9. DELETE /api/notification/{notification_id}

**说明**: Delete Notification


**描述**: 删除通知（软删除）


### 请求


```bash
curl -X DELETE 'http://127.0.0.1:8000/api/notification/1'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.387166"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| notification_id | integer |  |




## 10. POST /api/notification/cleanup

**说明**: Cleanup Old Notifications


**描述**: 清理旧通知


### 请求


```bash
curl -X POST 'http://127.0.0.1:8000/api/notification/cleanup'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.393383"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| days | integer |  |




## 11. GET /api/notification/statistics/by-date-range

**说明**: Get Statistics By Date Range


**描述**: 按日期范围获取统计（时间序列聚合）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/statistics/by-date-range'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.399898"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| start_date | string | 开始日期 (YYYY-MM-DD) |

| end_date | string | 结束日期 (YYYY-MM-DD) |




## 12. GET /api/notification/statistics/by-source

**说明**: Get Statistics By Source


**描述**: 按来源分组统计（任务/系统通知）


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/statistics/by-source'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.406711"
  },
  "data": null
}
```



## 13. GET /api/notification/export/csv

**说明**: Export Notifications Csv


**描述**: 导出通知为 CSV 文件


### 请求


```bash
curl -X GET 'http://127.0.0.1:8000/api/notification/export/csv'

```


### 返回


```json
{
  "success": false,
  "error": {
    "code": "HTTP_ERROR",
    "message": "Not authenticated",
    "details": {},
    "timestamp": "2025-12-02T11:24:13.413983"
  },
  "data": null
}
```


### 参数


| 参数名 | 类型 | 说明 |

|--------|------|------|

| include_content | boolean | 是否包含完整内容 |


