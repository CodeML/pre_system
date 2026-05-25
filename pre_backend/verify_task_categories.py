#!/usr/bin/env python3
"""
验证脚本：任务分类多级管理
流程：
1. 用现有用户登录获取 token
2. 创建多级分类（一级/二级/三级）
3. 获取分类树结构
4. 按电商平台筛选分类
5. 按角色筛选可操作分类
6. 获取分类的子分类和父分类
7. 编辑分类信息
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

# 1. 登录
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

# 2. 创建多级分类
def create_categories(token: str):
    print_step("步骤 2: 创建多级分类（一级/二级/三级）")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 一级分类
    level1_categories = [
        {
            "name": "电商设计",
            "is_ecommerce": True,
            "description": "电商平台设计相关任务",
            "role_ids": [1]  # 电商设计师角色
        },
        {
            "name": "3D设计",
            "is_ecommerce": False,
            "description": "3D建模和渲染任务",
            "role_ids": [2]  # 3D建模师角色
        },
        {
            "name": "其他设计",
            "is_ecommerce": False,
            "description": "摄影、平面等设计任务",
            "role_ids": None  # 无限制
        }
    ]
    
    created_categories = {}
    
    for cat_data in level1_categories:
        response = requests.post(
            f"{BASE_URL}/api/task-category/create",
            json=cat_data,
            headers=headers
        )
        
        if response.status_code == 200:
            cat = response.json()
            category_name = cat_data["name"]
            created_categories[category_name] = cat["id"]
            print_success(f"创建一级分类: {category_name} (ID: {cat['id']})")
        else:
            print_error(f"创建分类失败: {response.status_code}")
    
    # 二级分类（电商设计下的子分类）
    if "电商设计" in created_categories:
        ecommerce_parent_id = created_categories["电商设计"]
        level2_ecommerce = [
            {"name": "主图设计", "description": "商品主图设计"},
            {"name": "详情页设计", "description": "商品详情页设计"},
            {"name": "海报设计", "description": "营销海报设计"}
        ]
        
        for cat_data in level2_ecommerce:
            cat_data["parent_id"] = ecommerce_parent_id
            response = requests.post(
                f"{BASE_URL}/api/task-category/create",
                json=cat_data,
                headers=headers
            )
            
            if response.status_code == 200:
                cat = response.json()
                print_success(f"创建二级分类: {cat_data['name']} (ID: {cat['id']}, Parent: {ecommerce_parent_id})")
                created_categories[f"ecommerce_{cat_data['name']}"] = cat["id"]
            else:
                print_error(f"创建分类失败: {response.status_code}")
    
    # 二级分类（3D设计下的子分类）
    if "3D设计" in created_categories:
        modeling_parent_id = created_categories["3D设计"]
        level2_modeling = [
            {"name": "产品建模", "description": "商品3D建模"},
            {"name": "场景渲染", "description": "场景3D渲染"}
        ]
        
        for cat_data in level2_modeling:
            cat_data["parent_id"] = modeling_parent_id
            response = requests.post(
                f"{BASE_URL}/api/task-category/create",
                json=cat_data,
                headers=headers
            )
            
            if response.status_code == 200:
                cat = response.json()
                print_success(f"创建二级分类: {cat_data['name']} (ID: {cat['id']}, Parent: {modeling_parent_id})")
                created_categories[f"modeling_{cat_data['name']}"] = cat["id"]
            else:
                print_error(f"创建分类失败: {response.status_code}")
    
    return created_categories

# 3. 获取分类树结构
def get_category_tree():
    print_step("步骤 3: 获取分类树结构（多级）")
    
    response = requests.get(f"{BASE_URL}/api/task-category/tree")
    
    if response.status_code == 200:
        tree = response.json()
        print_success(f"获取分类树成功，共 {len(tree)} 个一级分类")
        print_response("分类树结构", {"tree": tree})
        return tree
    else:
        print_error(f"获取分类树失败: {response.status_code}")
        return []

# 4. 获取电商分类
def filter_ecommerce_categories():
    print_step("步骤 4: 获取所有电商设计分类")
    
    response = requests.get(f"{BASE_URL}/api/task-category/filter/ecommerce")
    
    if response.status_code == 200:
        categories = response.json()
        print_success(f"获取到 {len(categories)} 个电商分类")
        print_response("电商分类", {"categories": categories})
        return categories
    else:
        print_error(f"获取电商分类失败: {response.status_code}")
        return []

# 5. 获取用户可操作的分类
def get_accessible_categories(token: str):
    print_step("步骤 5: 获取当前用户可操作的分类（按角色筛选）")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{BASE_URL}/api/task-category/filter/my-accessible",
        headers=headers
    )
    
    if response.status_code == 200:
        categories = response.json()
        print_success(f"获取到 {len(categories)} 个用户可操作的分类")
        print_response("用户可操作分类", {"categories": categories})
        return categories
    else:
        print_error(f"获取用户可操作分类失败: {response.status_code}")
        return []

# 6. 获取分类的子分类和父分类
def get_category_hierarchy(category_id: int):
    print_step(f"步骤 6: 获取分类 ID={category_id} 的子分类和父分类")
    
    # 获取子分类
    sub_response = requests.get(f"{BASE_URL}/api/task-category/{category_id}/subcategories")
    if sub_response.status_code == 200:
        subcategories = sub_response.json()
        print_success(f"获取到 {len(subcategories)} 个子分类")
        if subcategories:
            print_response("子分类", {"subcategories": subcategories})
    else:
        print_error(f"获取子分类失败: {sub_response.status_code}")
        subcategories = []
    
    # 获取父分类链
    parent_response = requests.get(f"{BASE_URL}/api/task-category/{category_id}/parents")
    if parent_response.status_code == 200:
        parents = parent_response.json()
        print_success(f"获取到 {len(parents)} 个父分类")
        if parents:
            print_response("父分类链", {"parents": parents})
    else:
        print_error(f"获取父分类失败: {parent_response.status_code}")
        parents = []
    
    return subcategories, parents

# 7. 编辑分类信息
def update_category(category_id: int, token: str):
    print_step(f"步骤 7: 编辑分类 ID={category_id}")
    
    update_data = {
        "description": "更新后的分类描述"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(
        f"{BASE_URL}/api/task-category/{category_id}",
        json=update_data,
        headers=headers
    )
    
    if response.status_code == 200:
        category = response.json()
        print_success(f"编辑分类成功")
        print_response("编辑后的分类", category)
        return category
    else:
        print_error(f"编辑分类失败: {response.status_code}")
        return None

def main():
    print(f"\n{Colors.BLUE}{'*'*60}{Colors.END}")
    print(f"{Colors.BLUE}      任务分类多级管理验证测试{Colors.END}")
    print(f"{Colors.BLUE}{'*'*60}{Colors.END}")
    
    try:
        # 1. 登录
        token, user_id = login()
        if not token:
            print_error("无法登录，测试中断")
            return
        
        # 2. 创建多级分类
        created_categories = create_categories(token)
        if not created_categories:
            print_error("无法创建分类，测试中断")
            return
        
        # 3. 获取分类树结构
        tree = get_category_tree()
        
        # 4. 获取电商分类
        ecommerce_cats = filter_ecommerce_categories()
        
        # 5. 获取用户可操作的分类
        accessible_cats = get_accessible_categories(token)
        
        # 6. 获取某个分类的子分类和父分类
        if created_categories:
            first_category_id = list(created_categories.values())[0]
            subcats, parents = get_category_hierarchy(first_category_id)
        
        # 7. 编辑分类
        if created_categories:
            first_category_id = list(created_categories.values())[0]
            updated = update_category(first_category_id, token)
        
        # 最终总结
        print_step("验证完成")
        print(f"{Colors.GREEN}✓ 所有验证步骤完成！{Colors.END}")
        print(f"\n{Colors.YELLOW}验证总结:{Colors.END}")
        print(f"  • 创建分类数: {len(created_categories)}")
        print(f"  • 分类树一级数: {len(tree)}")
        print(f"  • 电商分类数: {len(ecommerce_cats)}")
        print(f"  • 用户可操作分类数: {len(accessible_cats)}")
        
    except Exception as e:
        print_error(f"测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
