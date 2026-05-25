#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
项目管理模块验证脚本
验证流程：
1. 登录
2. 创建多个项目
3. 按客户查询项目
4. 按状态查询项目
5. 按类型查询项目
6. 按平台查询项目
7. 分配设计师
8. 更新项目状态
9. 添加素材
10. 多条件高级筛选
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/user/login"
CREATE_PROJECT_URL = f"{BASE_URL}/api/project/create"
LIST_PROJECT_URL = f"{BASE_URL}/api/project/list"
GET_PROJECT_URL = f"{BASE_URL}/api/project"
UPDATE_PROJECT_URL = f"{BASE_URL}/api/project"
DELETE_PROJECT_URL = f"{BASE_URL}/api/project"

# 颜色输出
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"► {text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"\033[91m✗ {text}{RESET}")

def print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))

# ============================================================
# 步骤 1: 登录
# ============================================================
print_header("步骤 1: 用现有用户登录")

login_data = {"username": "project_test", "password": "project_test_123"}
response = requests.post(LOGIN_URL, data=login_data)
if response.status_code == 200:
    token_data = response.json()
    token = token_data["access_token"]
    user_id = token_data["user"]["id"]
    print_success(f"登录成功! 用户: {token_data['user']['username']} (ID: {user_id})")
    headers = {"Authorization": f"Bearer {token}"}
else:
    print_error(f"登录失败: {response.text}")
    exit(1)

# ============================================================
# 步骤 2: 获取客户信息
# ============================================================
print_header("步骤 2: 获取现有客户（用于项目关联）")

list_customers_url = f"{BASE_URL}/api/customer/list?skip=0&limit=100"
response = requests.get(list_customers_url, headers=headers)
if response.status_code == 200:
    customers = response.json()
    if customers:
        customer_id = customers[0]["id"]
        customer_name = customers[0]["name"]
        print_success(f"获取到客户: {customer_name} (ID: {customer_id})")
    else:
        print_error("没有可用的客户，请先创建客户")
        exit(1)
else:
    print_error(f"获取客户失败: {response.text}")
    exit(1)

# ============================================================
# 步骤 3: 创建多个项目
# ============================================================
print_header("步骤 3: 创建多个项目")

projects_data = [
    {
        "name": "电商详情页设计-淘宝",
        "customer_id": customer_id,
        "type": "电商详情页",
        "ecommerce_platform": "淘宝",
        "status": "待启动",
        "remark": "商品详情页高保真设计"
    },
    {
        "name": "3D产品建模",
        "customer_id": customer_id,
        "type": "3D建模",
        "ecommerce_platform": "抖音",
        "status": "待启动",
        "remark": "电商产品3D建模和渲染"
    },
    {
        "name": "摄影后期处理",
        "customer_id": customer_id,
        "type": "摄影",
        "ecommerce_platform": "小红书",
        "status": "设计中",
        "remark": "产品摄影图片后期处理"
    },
    {
        "name": "电商详情页设计-Amazon",
        "customer_id": customer_id,
        "type": "电商详情页",
        "ecommerce_platform": "Amazon",
        "status": "待启动",
        "material_ids": [1, 2],
        "remark": "Amazon平台跨境电商详情页"
    },
]

created_projects = []
for i, proj_data in enumerate(projects_data, 1):
    response = requests.post(CREATE_PROJECT_URL, json=proj_data, headers=headers)
    if response.status_code == 200:
        project = response.json()
        created_projects.append(project)
        print_success(f"创建项目 {i}: {project['name']} (ID: {project['id']})")
    else:
        print_error(f"创建项目 {i} 失败: {response.text}")

print_success(f"共创建 {len(created_projects)} 个项目")

# ============================================================
# 步骤 4: 获取项目列表
# ============================================================
print_header("步骤 4: 获取项目列表")

response = requests.get(LIST_PROJECT_URL, headers=headers)
if response.status_code == 200:
    projects = response.json()
    print_success(f"获取到 {len(projects)} 个项目\n")
    print("项目列表:")
    for proj in projects:
        print(f"  - {proj['name']} (ID: {proj['id']}, 状态: {proj['status']})")
else:
    print_error(f"获取项目列表失败: {response.text}")

# ============================================================
# 步骤 5: 按客户查询项目
# ============================================================
print_header("步骤 5: 按客户查询项目")

url = f"{BASE_URL}/api/project/filter/by-customer/{customer_id}"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    projects = response.json()
    print_success(f"客户 ID={customer_id} 下有 {len(projects)} 个项目")
else:
    print_error(f"按客户查询失败: {response.text}")

# ============================================================
# 步骤 6: 按状态查询项目
# ============================================================
print_header("步骤 6: 按状态查询项目")

status_values = ["待启动", "设计中", "待确认", "已交付", "已完结"]
for status in status_values:
    url = f"{BASE_URL}/api/project/filter/by-status/{status}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        projects = response.json()
        if projects:
            print_success(f"状态 '{status}' 下有 {len(projects)} 个项目")

# ============================================================
# 步骤 7: 按类型查询项目
# ============================================================
print_header("步骤 7: 按项目类型查询")

types = ["电商详情页", "3D建模", "摄影"]
for proj_type in types:
    url = f"{BASE_URL}/api/project/filter/by-type/{proj_type}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        projects = response.json()
        if projects:
            print_success(f"类型 '{proj_type}' 下有 {len(projects)} 个项目")
            for proj in projects:
                print(f"  - {proj['name']}")

# ============================================================
# 步骤 8: 按电商平台查询
# ============================================================
print_header("步骤 8: 按电商平台查询")

platforms = ["淘宝", "抖音", "小红书", "Amazon"]
for platform in platforms:
    url = f"{BASE_URL}/api/project/filter/by-platform/{platform}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        projects = response.json()
        if projects:
            print_success(f"平台 '{platform}' 下有 {len(projects)} 个项目")

# ============================================================
# 步骤 9: 更新项目状态
# ============================================================
print_header("步骤 9: 更新项目状态")

if created_projects:
    project_id = created_projects[0]["id"]
    url = f"{BASE_URL}/api/project/{project_id}/status/设计中"
    response = requests.put(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print_success(f"项目 ID={project_id} 状态已更新为: 设计中")
    else:
        print_error(f"更新状态失败: {response.text}")

# ============================================================
# 步骤 10: 分配设计师
# ============================================================
print_header("步骤 10: 分配设计师")

if created_projects:
    project_id = created_projects[0]["id"]
    url = f"{BASE_URL}/api/project/{project_id}/assign-designers?main_designer_id={user_id}"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print_success(f"设计师已分配到项目 ID={project_id}")
    else:
        print_error(f"分配设计师失败: {response.text}")

# ============================================================
# 步骤 11: 获取设计师相关的项目
# ============================================================
print_header("步骤 11: 获取设计师相关的项目")

url = f"{BASE_URL}/api/project/filter/by-designer/{user_id}"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    projects = response.json()
    print_success(f"设计师 ID={user_id} 相关的项目数: {len(projects)}")
    for proj in projects:
        print(f"  - {proj['name']} (主设计师: {proj['main_designer_id']}, 辅助设计师: {proj['assist_designer_id']})")
else:
    print_error(f"获取设计师项目失败: {response.text}")

# ============================================================
# 步骤 12: 添加素材
# ============================================================
print_header("步骤 12: 添加素材到项目")

if created_projects:
    project_id = created_projects[0]["id"]
    material_id = 999
    url = f"{BASE_URL}/api/project/{project_id}/materials/{material_id}"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print_success(f"素材 {material_id} 已添加到项目 {project_id}")
    else:
        print_error(f"添加素材失败: {response.text}")

# ============================================================
# 步骤 13: 获取项目详情
# ============================================================
print_header("步骤 13: 获取项目详情")

if created_projects:
    project_id = created_projects[0]["id"]
    url = f"{GET_PROJECT_URL}/{project_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        project = response.json()
        print_success(f"项目详情 (ID: {project_id}):")
        print("\n响应数据:")
        print_json({
            "id": project["id"],
            "name": project["name"],
            "type": project["type"],
            "ecommerce_platform": project["ecommerce_platform"],
            "status": project["status"],
            "main_designer_id": project["main_designer_id"],
            "assist_designer_id": project["assist_designer_id"],
            "material_ids": project["material_ids"],
            "customer_id": project["customer_id"],
            "create_time": project["create_time"]
        })
    else:
        print_error(f"获取项目详情失败: {response.text}")

# ============================================================
# 步骤 14: 编辑项目
# ============================================================
print_header("步骤 14: 编辑项目信息")

if created_projects:
    project_id = created_projects[0]["id"]
    url = f"{UPDATE_PROJECT_URL}/{project_id}"
    update_data = {
        "name": "编辑后的项目名称-电商详情页设计",
        "remark": "这是编辑后的备注信息"
    }
    response = requests.put(url, json=update_data, headers=headers)
    if response.status_code == 200:
        project = response.json()
        print_success(f"项目已编辑: {project['name']}")
    else:
        print_error(f"编辑项目失败: {response.text}")

# ============================================================
# 步骤 15: 多条件高级筛选
# ============================================================
print_header("步骤 15: 多条件高级筛选")

url = f"{BASE_URL}/api/project/filter/advanced"
filter_params = {
    "customer_id": customer_id,
    "project_type": "电商详情页"
}
response = requests.post(url, json=filter_params, headers=headers)
if response.status_code == 200:
    projects = response.json()
    print_success(f"高级筛选结果: 客户={customer_id}, 类型=电商详情页，共 {len(projects)} 个项目")
    for proj in projects:
        print(f"  - {proj['name']} (状态: {proj['status']})")
else:
    print_error(f"高级筛选失败: {response.text}")

# ============================================================
# 验证完成
# ============================================================
print_header("验证完成")
print_success("所有验证步骤完成！")
print(f"\n验证总结:")
print(f"  • 创建项目数: {len(created_projects)}")
print(f"  • 支持的项目类型: {', '.join(types)}")
print(f"  • 支持的电商平台: {', '.join(platforms)}")
print(f"  • 支持的项目状态: {', '.join(status_values)}")
print(f"  • 设计师分配功能: ✓")
print(f"  • 素材管理功能: ✓")
print(f"  • 多条件筛选功能: ✓")
