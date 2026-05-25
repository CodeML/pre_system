#!/usr/bin/env python3
"""
验证脚本：账号登录 + 多角色分配
流程：
1. 初始化数据库，插入默认角色
2. 创建测试用户
3. 测试登录获取 JWT token
4. 为用户分配多个角色
5. 查询用户详情和角色列表
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"

# 彩色输出
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

# 1. 初始化默认角色
def init_default_roles():
    print_step("步骤 1: 初始化默认角色")
    
    roles = [
        {"name": "电商设计师", "code": "ECOMMERCE_DESIGNER", "permission": "design,manage_projects"},
        {"name": "3D建模师", "code": "3D_MODELER", "permission": "3d_design,render"},
        {"name": "项目经理", "code": "PROJECT_MANAGER", "permission": "manage_all,approve"},
        {"name": "管理员", "code": "ADMIN", "permission": "system_admin"},
    ]
    
    role_ids = {}
    for role in roles:
        response = requests.post(f"{BASE_URL}/api/role/create", json=role)
        if response.status_code == 200:
            data = response.json()
            role_ids[role["code"]] = data["id"]
            print_success(f"创建角色: {role['name']} (ID: {data['id']})")
        elif response.status_code == 400:
            print_info(f"角色 {role['name']} 已存在（跳过）")
            # 获取现有角色的ID
            list_resp = requests.get(f"{BASE_URL}/api/role/list")
            if list_resp.status_code == 200:
                roles_list = list_resp.json()
                for r in roles_list:
                    if r["code"] == role["code"]:
                        role_ids[role["code"]] = r["id"]
                        break
        else:
            print_error(f"创建角色失败: {response.status_code} - {response.text}")
    
    return role_ids

# 2. 获取角色列表
def get_roles_list():
    print_step("步骤 2: 获取角色列表")
    
    response = requests.get(f"{BASE_URL}/api/role/list")
    if response.status_code == 200:
        roles = response.json()
        print_success(f"获取到 {len(roles)} 个角色")
        print_response("角色列表", {"roles": roles})
        return roles
    else:
        print_error(f"获取角色列表失败: {response.status_code}")
        return []

# 3. 创建测试用户
def create_test_user():
    print_step("步骤 3: 创建测试用户")
    
    user_data = {
        "username": "testuser",
        "password": "testpass123",
        "name": "测试用户",
        "phone": "13800138000"
    }
    
    response = requests.post(f"{BASE_URL}/api/user/create", json=user_data)
    if response.status_code == 200:
        user = response.json()
        print_success(f"创建用户成功: {user['username']} (ID: {user['id']})")
        print_response("用户信息", user)
        return user
    elif response.status_code == 400:
        print_info("用户已存在（跳过创建）")
        # 获取用户列表找到该用户
        list_resp = requests.get(f"{BASE_URL}/api/user/list")
        if list_resp.status_code == 200:
            users = list_resp.json()
            for u in users:
                if u["username"] == "testuser":
                    return u
    else:
        print_error(f"创建用户失败: {response.status_code} - {response.text}")
        return None

# 4. 登录获取 token
def login_user(username: str, password: str):
    print_step("步骤 4: 用户登录获取 JWT Token")
    
    response = requests.post(
        f"{BASE_URL}/api/user/login",
        data={"username": username, "password": password}
    )
    
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        user = token_data["user"]
        print_success(f"登录成功! 用户: {user['username']}")
        print_info(f"Token (前32字符): {token[:32]}...")
        print_response("登录响应", token_data)
        return token, user
    else:
        print_error(f"登录失败: {response.status_code} - {response.text}")
        return None, None

# 5. 为用户分配角色
def assign_roles(user_id: int, role_ids: list):
    print_step("步骤 5: 为用户分配多个角色")
    
    assigned_roles = []
    for role_id in role_ids[:3]:  # 分配前3个角色
        response = requests.post(
            f"{BASE_URL}/api/user/assign_role/{user_id}",
            params={"role_id": role_id}
        )
        
        if response.status_code == 200:
            result = response.json()
            assigned_roles.append(role_id)
            print_success(f"分配角色成功 (Role ID: {role_id})")
            print_response(f"分配结果 (Role {role_id})", result)
        else:
            print_error(f"分配角色失败: {response.status_code} - {response.text}")
    
    return assigned_roles

# 6. 查询用户的角色列表
def get_user_roles(user_id: int):
    print_step("步骤 6: 查询用户的所有角色")
    
    response = requests.get(f"{BASE_URL}/api/user/{user_id}/roles")
    
    if response.status_code == 200:
        data = response.json()
        roles = data.get("roles", [])
        print_success(f"用户共有 {len(roles)} 个角色")
        print_response("用户角色列表", data)
        return roles
    else:
        print_error(f"查询用户角色失败: {response.status_code} - {response.text}")
        return []

# 7. 测试角色取消分配
def revoke_role(user_id: int, role_id: int):
    print_step("步骤 7: 测试取消角色分配")
    
    response = requests.delete(
        f"{BASE_URL}/api/user/revoke_role/{user_id}",
        params={"role_id": role_id}
    )
    
    if response.status_code == 200:
        result = response.json()
        print_success(f"取消角色成功 (Role ID: {role_id})")
        print_response("取消结果", result)
    else:
        print_error(f"取消角色失败: {response.status_code} - {response.text}")

# 主测试流程
def main():
    print(f"\n{Colors.BLUE}{'*'*60}{Colors.END}")
    print(f"{Colors.BLUE}      账号登录 + 多角色分配验证测试{Colors.END}")
    print(f"{Colors.BLUE}{'*'*60}{Colors.END}")
    
    try:
        # 1. 初始化角色
        role_ids_dict = init_default_roles()
        role_ids = list(role_ids_dict.values())
        
        if not role_ids:
            print_error("无法获取角色列表，测试中断")
            return
        
        # 2. 获取角色列表
        roles = get_roles_list()
        
        # 3. 创建用户
        user = create_test_user()
        if not user:
            print_error("无法创建用户，测试中断")
            return
        
        user_id = user["id"]
        
        # 4. 登录获取 token
        token, logged_user = login_user("testuser", "testpass123")
        if not token:
            print_error("无法获取 token，测试中断")
            return
        
        # 5. 为用户分配角色
        assigned = assign_roles(user_id, role_ids)
        
        # 6. 查询用户角色
        user_roles = get_user_roles(user_id)
        
        # 7. 取消一个角色
        if assigned:
            revoke_role(user_id, assigned[0])
            # 再查一遍看是否成功取消
            get_user_roles(user_id)
        
        # 最终总结
        print_step("验证完成")
        print(f"{Colors.GREEN}✓ 所有验证步骤完成！{Colors.END}")
        print(f"\n{Colors.YELLOW}验证总结:{Colors.END}")
        print(f"  • 已创建 {len(roles)} 个角色")
        print(f"  • 用户: testuser (ID: {user_id})")
        print(f"  • Token 长度: {len(token)} 字符")
        print(f"  • 分配的角色数: {len(assigned)}")
        
    except Exception as e:
        print_error(f"测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
