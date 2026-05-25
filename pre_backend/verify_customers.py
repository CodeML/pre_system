#!/usr/bin/env python3
"""
验证脚本：客户管理模块 - 新增/编辑/查询/筛选
流程：
1. 用现有用户登录获取 token
2. 创建多个客户（不同电商平台）
3. 查询客户列表
4. 按电商平台筛选
5. 按名称搜索
6. 编辑客户信息
7. 获取特定创建人的客户
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_step(msg: str):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}► {msg}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.YELLOW}ℹ {msg}{Colors.END}")

def print_response(title: str, data: Dict[str, Any]):
    print(f"\n{Colors.YELLOW}响应 ({title}):{Colors.END}")
    print(json.dumps(data, indent=2, ensure_ascii=False))

# 1. 用现有用户登录获取 token
def login():
    print_step("步骤 1: 用现有用户登录")
    
    response = requests.post(
        f"{BASE_URL}/api/user/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        user = token_data["user"]
        print_success(f"登录成功! 用户: {user['username']} (ID: {user['id']})")
        return token, user["id"]
    else:
        print_error(f"登录失败: {response.status_code}")
        return None, None

# 2. 创建多个客户
def create_customers(token: str):
    print_step("步骤 2: 创建多个客户")
    
    customers_data = [
        {
            "name": "淘宝店铺A",
            "contact": "张三",
            "phone": "13800138001",
            "type": "company",
            "ecommerce_platform": "淘宝",
            "remark": "主营女装"
        },
        {
            "name": "抖音品牌B",
            "contact": "李四",
            "phone": "13800138002",
            "type": "brand",
            "ecommerce_platform": "抖音",
            "remark": "新兴美妆品牌"
        },
        {
            "name": "小红书博主C",
            "contact": "王五",
            "phone": "13800138003",
            "type": "individual",
            "ecommerce_platform": "小红书",
            "remark": "生活方式内容创作者"
        },
        {
            "name": "Amazon卖家D",
            "contact": "孙六",
            "phone": "13800138004",
            "type": "company",
            "ecommerce_platform": "Amazon",
            "remark": "跨境电商卖家"
        }
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    created_customers = []
    
    for customer_data in customers_data:
        response = requests.post(
            f"{BASE_URL}/api/customer/create",
            json=customer_data,
            headers=headers
        )
        
        if response.status_code == 200:
            customer = response.json()
            created_customers.append(customer)
            print_success(f"创建客户: {customer['name']} (ID: {customer['id']})")
            print_response(f"客户详情 {customer['name']}", customer)
        else:
            print_error(f"创建客户失败: {response.status_code} - {response.text}")
    
    return created_customers

# 3. 查询客户列表
def list_customers():
    print_step("步骤 3: 查询客户列表")
    
    response = requests.get(f"{BASE_URL}/api/customer/list?limit=100")
    
    if response.status_code == 200:
        customers = response.json()
        print_success(f"获取到 {len(customers)} 个客户")
        print_response("客户列表", {"count": len(customers), "customers": customers})
        return customers
    else:
        print_error(f"查询客户列表失败: {response.status_code}")
        return []

# 4. 按电商平台筛选
def filter_by_platform(platform: str):
    print_step(f"步骤 4: 按电商平台筛选 - {platform}")
    
    response = requests.get(f"{BASE_URL}/api/customer/filter/platform/{platform}")
    
    if response.status_code == 200:
        customers = response.json()
        print_success(f"筛选到 {len(customers)} 个 {platform} 平台的客户")
        print_response(f"{platform} 平台客户", {"customers": customers})
        return customers
    else:
        print_error(f"筛选失败: {response.status_code}")
        return []

# 5. 按名称搜索
def search_by_name(name: str):
    print_step(f"步骤 5: 按名称搜索 - {name}")
    
    response = requests.get(f"{BASE_URL}/api/customer/search/name/{name}")
    
    if response.status_code == 200:
        customers = response.json()
        print_success(f"搜索到 {len(customers)} 个包含 '{name}' 的客户")
        print_response(f"搜索结果 '{name}'", {"customers": customers})
        return customers
    else:
        print_error(f"搜索失败: {response.status_code}")
        return []

# 6. 编辑客户信息
def update_customer(customer_id: int, token: str):
    print_step(f"步骤 6: 编辑客户 ID={customer_id}")
    
    update_data = {
        "contact": "修改后的联系人",
        "phone": "18800188001",
        "remark": "已更新备注信息"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{BASE_URL}/api/customer/{customer_id}",
        json=update_data,
        headers=headers
    )
    
    if response.status_code == 200:
        customer = response.json()
        print_success(f"编辑客户成功")
        print_response("编辑后的客户", customer)
        return customer
    else:
        print_error(f"编辑客户失败: {response.status_code} - {response.text}")
        return None

# 7. 获取特定创建人的客户
def get_customers_by_creator(creator_id: int):
    print_step(f"步骤 7: 获取用户 ID={creator_id} 创建的客户")
    
    response = requests.get(f"{BASE_URL}/api/customer/creator/{creator_id}")
    
    if response.status_code == 200:
        customers = response.json()
        print_success(f"获取到 {len(customers)} 个由该用户创建的客户")
        print_response(f"创建人 {creator_id} 的客户", {"customers": customers})
        return customers
    else:
        print_error(f"查询失败: {response.status_code}")
        return []

def main():
    print(f"\n{Colors.BLUE}{'*'*60}{Colors.END}")
    print(f"{Colors.BLUE}         客户管理模块验证测试{Colors.END}")
    print(f"{Colors.BLUE}{'*'*60}{Colors.END}")
    
    try:
        # 1. 登录
        token, user_id = login()
        if not token:
            print_error("无法登录，测试中断")
            return
        
        # 2. 创建客户
        created_customers = create_customers(token)
        if not created_customers:
            print_error("无法创建客户，测试中断")
            return
        
        # 3. 查询客户列表
        all_customers = list_customers()
        
        # 4. 按平台筛选
        taobao_customers = filter_by_platform("淘宝")
        douyin_customers = filter_by_platform("抖音")
        
        # 5. 按名称搜索
        search_results = search_by_name("淘宝")
        
        # 6. 编辑客户
        if created_customers:
            updated = update_customer(created_customers[0]["id"], token)
        
        # 7. 获取创建人的客户
        my_customers = get_customers_by_creator(user_id)
        
        # 最终总结
        print_step("验证完成")
        print(f"{Colors.GREEN}✓ 所有验证步骤完成！{Colors.END}")
        print(f"\n{Colors.YELLOW}验证总结:{Colors.END}")
        print(f"  • 创建客户数: {len(created_customers)}")
        print(f"  • 总客户数: {len(all_customers)}")
        print(f"  • 淘宝客户数: {len(taobao_customers)}")
        print(f"  • 抖音客户数: {len(douyin_customers)}")
        print(f"  • 搜索结果数: {len(search_results)}")
        print(f"  • 我创建的客户数: {len(my_customers)}")
        
    except Exception as e:
        print_error(f"测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
