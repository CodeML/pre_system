#!/usr/bin/env python3
"""
API 接口检查和整理脚本
检查指定模块的重复英文接口和文档一致性
"""

import sys
import re
from pathlib import Path
from collections import defaultdict

def extract_endpoints(file_path):
    """从 API 文件中提取所有端点"""
    endpoints = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配路由装饰器和函数
    pattern = r'@router\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\'].*?\)\s*(?:.*?\n)*?def\s+(\w+)\s*\([^)]*\):\s*["\']([^"\']*)["\']'
    
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        method, path, func_name, docstring = match.groups()
        endpoints.append({
            'method': method.upper(),
            'path': path,
            'function': func_name,
            'docstring': docstring.strip() if docstring else '',
            'file': file_path.name
        })
    
    return endpoints

def check_endpoints(directory):
    """检查指定目录中的所有 API 文件"""
    api_dir = Path(directory)
    
    modules_of_interest = [
        'notification_api.py',
        'dashboard_api.py', 
        'material_api.py',
        'file_api.py',
        'task_api.py',
        'project_api.py',
        'customer_tag_api.py'
    ]
    
    all_endpoints = defaultdict(list)
    
    print("=" * 80)
    print("API 接口检查报告")
    print("=" * 80)
    
    for module_file in modules_of_interest:
        file_path = api_dir / module_file
        
        if not file_path.exists():
            print(f"\n⚠️  文件不存在: {module_file}")
            continue
        
        print(f"\n📋 模块: {module_file}")
        print("-" * 80)
        
        endpoints = extract_endpoints(file_path)
        
        if not endpoints:
            print("  无法解析端点")
            continue
        
        for ep in endpoints:
            key = f"{ep['method']} {ep['path']}"
            all_endpoints[key].append(module_file)
            
            print(f"  {ep['method']:6} {ep['path']:50} | {ep['docstring'][:40]}")
    
    # 检查重复
    print("\n" + "=" * 80)
    print("重复接口检查")
    print("=" * 80)
    
    duplicates = {k: v for k, v in all_endpoints.items() if len(v) > 1}
    
    if duplicates:
        print(f"\n⚠️  发现 {len(duplicates)} 个重复接口:\n")
        for endpoint, modules in sorted(duplicates.items()):
            print(f"  {endpoint}")
            for module in modules:
                print(f"    - {module}")
    else:
        print("\n✅ 未发现重复接口")
    
    # 统计
    print("\n" + "=" * 80)
    print("统计信息")
    print("=" * 80)
    
    total_endpoints = sum(len(eps) for eps in extract_endpoints(api_dir / f) 
                         if (api_dir / f).exists() for f in modules_of_interest)
    
    print(f"✅ 总端点数: {total_endpoints}")
    print(f"⚠️  重复端点: {len(duplicates)}")

if __name__ == "__main__":
    backend_dir = "/Users/shaiweiminglei/pre_system/pre_backend/api"
    check_endpoints(backend_dir)
