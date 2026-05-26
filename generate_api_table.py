import os
import re

api_dir = "/Users/shaiweiminglei/pre_system/pre_backend/api"
files = [f for f in os.listdir(api_dir) if f.endswith("_api.py")]

print("# PRE 系统 API 功能全览表\n")

# 定义模块名映射
module_map = {
    "user_api.py": "用户管理",
    "role_api.py": "角色权限",
    "customer_api.py": "客户管理",
    "customer_tag_api.py": "客户标签",
    "task_category_api.py": "任务分类",
    "project_api.py": "项目管理",
    "task_api.py": "任务中心",
    "file_api.py": "文件管理",
    "material_api.py": "素材中心",
    "dashboard_api.py": "仪表板",
    "notification_api.py": "消息通知",
    "finance_api.py": "财务核算",
    "after_sales_api.py": "售后风控",
    "hr_api.py": "人事绩效",
    "crm_api.py": "CRM & 营销",
    "im_api.py": "即时通讯"
}

# 排序以保证输出整齐
files.sort()

for file in files:
    module_name = module_map.get(file, file)
    print(f"## {module_name}")
    print("| 方法 | 路径 | 功能描述 |")
    print("| :--- | :--- | :--- |")
    
    with open(os.path.join(api_dir, file), "r", encoding="utf-8") as f:
        content = f.read()
        
        # 匹配 @router.get("/...", summary="...") 格式
        # 支持多种方法和跨行匹配
        pattern = r'@router\.(get|post|put|delete)\(\s*["\']([^"\']+)["\'][^)]*summary=["\']([^"\']+)["\']'
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        
        # 获取基础前缀（从 api/__init__.py 或约定中获取）
        # 这里为了表格简洁，直接显示路径，实际请求需加上 /api/模块前缀
        
        for method, path, summary in matches:
            method = method.upper()
            # 清理摘要中的换行
            summary = summary.replace("\n", " ").strip()
            print(f"| {method} | `{path}` | {summary} |")
    print("\n")
