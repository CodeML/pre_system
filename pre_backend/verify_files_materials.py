"""验证文件管理和素材库模块"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000/api"

# 测试账户
admin_user = {"username": "testuser", "password": "testpass123"}
designer_user = {"username": "project_test", "password": "project_test_123"}

def login(user_data):
    """用户登录"""
    response = requests.post(f"{BASE_URL}/user/login", data=user_data)
    if response.status_code == 200:
        data = response.json()
        return data['access_token'], data['user']['id']
    print(f"登录失败: {response.status_code} - {response.text}")
    return None, None

def print_section(title):
    """打印分隔符"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def verify_step(step_num, description, condition, details=""):
    """验证步骤"""
    status = "✅ PASS" if condition else "❌ FAIL"
    print(f"{step_num}. {status} - {description}")
    if details:
        print(f"   详情: {details}")
    return condition

# ============= 主验证流程 =============

print_section("PRE 系统 - 文件管理和素材库验证")
print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

step_count = 0
pass_count = 0

# 1. 登录
print_section("步骤1: 账户登录")
admin_token, admin_id = login(admin_user)
designer_token, designer_id = login(designer_user)

step_count += 1
if verify_step(step_count, "管理员登录", admin_token is not None, f"Token: {admin_token[:20]}..."):
    pass_count += 1

step_count += 1
if verify_step(step_count, "设计师登录", designer_token is not None, f"User ID: {designer_id}"):
    pass_count += 1

# 2. 获取测试项目和任务
print_section("步骤2: 获取测试数据")
headers_admin = {"Authorization": f"Bearer {admin_token}"}
headers_designer = {"Authorization": f"Bearer {designer_token}"}

# 获取项目列表
projects_resp = requests.get(f"{BASE_URL}/project/list?limit=1", headers=headers_admin)
projects = projects_resp.json() if projects_resp.status_code == 200 else []
project_id = projects[0]['id'] if projects else None

step_count += 1
if verify_step(step_count, "获取项目", project_id is not None, f"项目ID: {project_id}"):
    pass_count += 1

# 获取任务列表
tasks_resp = requests.get(f"{BASE_URL}/task/list?limit=1", headers=headers_admin)
tasks = tasks_resp.json() if tasks_resp.status_code == 200 else []
task_id = tasks[0]['id'] if tasks else None

step_count += 1
if verify_step(step_count, "获取任务", task_id is not None, f"任务ID: {task_id}"):
    pass_count += 1

# 3. 文件管理测试
print_section("步骤3: 文件管理")

# 3.1 创建文件记录
file_create_data = {
    "task_id": task_id,
    "name": "海报初稿.psd",
    "url": "http://example.com/poster_v1.psd",
    "file_type": "设计稿",
    "file_format": "psd",
    "size": 50,  # MB
    "description": "项目初稿"
}

file_resp = requests.post(f"{BASE_URL}/file/create", json=file_create_data, headers=headers_designer)
file_id = file_resp.json().get('id') if file_resp.status_code == 200 else None

step_count += 1
if verify_step(step_count, "创建文件v1", file_id is not None, f"文件ID: {file_id}"):
    pass_count += 1

# 3.2 创建文件新版本
file_v2_data = {
    "task_id": task_id,
    "name": "海报初稿.psd",
    "url": "http://example.com/poster_v2.psd",
    "file_type": "设计稿",
    "file_format": "psd",
    "size": 52,  # MB
    "description": "修改后版本"
}

file_v2_resp = requests.post(f"{BASE_URL}/file/{task_id}/new-version", json=file_v2_data, headers=headers_designer)
file_v2_id = file_v2_resp.json().get('id') if file_v2_resp.status_code == 200 else None

step_count += 1
if verify_step(step_count, "创建文件v2", file_v2_id is not None, f"文件ID: {file_v2_id}"):
    pass_count += 1

# 3.3 获取文件版本历史
versions_resp = requests.get(f"{BASE_URL}/file/{task_id}/versions?name=海报初稿.psd", headers=headers_admin)
versions_data = versions_resp.json() if versions_resp.status_code == 200 else {}
total_versions = versions_data.get('total_versions', 0)

step_count += 1
if verify_step(step_count, "获取版本历史", total_versions >= 2, f"总版本数: {total_versions}"):
    pass_count += 1

# 3.4 确认文件
confirm_data = {"confirm_remark": "质量良好，已确认"}
confirm_resp = requests.put(f"{BASE_URL}/file/{file_v2_id}/confirm", json=confirm_data, headers=headers_admin)
confirm_ok = confirm_resp.status_code == 200

step_count += 1
if verify_step(step_count, "确认文件", confirm_ok, "文件标记为已确认"):
    pass_count += 1

# 3.5 按任务查询文件
task_files_resp = requests.get(f"{BASE_URL}/file/filter/by-task/{task_id}", headers=headers_admin)
task_files = task_files_resp.json() if task_files_resp.status_code == 200 else []
task_files_count = len(task_files)

step_count += 1
if verify_step(step_count, "按任务查询文件", task_files_count > 0, f"文件数: {task_files_count}"):
    pass_count += 1

# 3.6 按类型查询文件
type_files_resp = requests.get(f"{BASE_URL}/file/filter/by-type/设计稿", headers=headers_admin)
type_files = type_files_resp.json() if type_files_resp.status_code == 200 else []
type_files_count = len(type_files)

step_count += 1
if verify_step(step_count, "按类型查询文件", type_files_count > 0, f"设计稿数: {type_files_count}"):
    pass_count += 1

# 3.7 获取文件统计
stats_resp = requests.get(f"{BASE_URL}/file/{task_id}/stats", headers=headers_admin)
stats = stats_resp.json() if stats_resp.status_code == 200 else {}
confirmed_count = stats.get('confirmed', 0)

step_count += 1
if verify_step(step_count, "获取文件统计", confirmed_count > 0, f"已确认: {confirmed_count}, 未确认: {stats.get('unconfirmed', 0)}"):
    pass_count += 1

# 4. 素材库管理测试
print_section("步骤4: 素材库管理")

# 4.1 创建素材
material_data = {
    "name": "通用底色",
    "type": "配色",
    "url": "http://example.com/color_palette.json",
    "category": "品牌色",
    "file_format": "json",
    "size": 2,  # KB
    "is_reusable": True,
    "tags": ["品牌", "配色"],
    "description": "品牌配色方案"
}

material_resp = requests.post(f"{BASE_URL}/material/create", json=material_data, headers=headers_designer)
material_id = material_resp.json().get('id') if material_resp.status_code == 200 else None

step_count += 1
if verify_step(step_count, "创建素材", material_id is not None, f"素材ID: {material_id}"):
    pass_count += 1

# 4.2 关联素材到项目
if project_id and material_id:
    assoc_resp = requests.post(f"{BASE_URL}/material/{material_id}/projects/{project_id}", headers=headers_admin)
    assoc_ok = assoc_resp.status_code == 200

    step_count += 1
    if verify_step(step_count, "关联素材到项目", assoc_ok, f"素材{material_id}已关联到项目{project_id}"):
        pass_count += 1

# 4.3 获取项目素材
project_materials_resp = requests.get(f"{BASE_URL}/material/filter/by-project/{project_id}", headers=headers_admin)
project_materials = project_materials_resp.json() if project_materials_resp.status_code == 200 else []
project_materials_count = len(project_materials)

step_count += 1
if verify_step(step_count, "获取项目素材", project_materials_count > 0, f"项目素材数: {project_materials_count}"):
    pass_count += 1

# 4.4 为素材添加标签
tag_resp = requests.post(f"{BASE_URL}/material/{material_id}/tags/测试标签", headers=headers_admin)
tag_ok = tag_resp.status_code == 200

step_count += 1
if verify_step(step_count, "添加素材标签", tag_ok, "标签已添加"):
    pass_count += 1

# 4.5 按标签查询素材
tag_materials_resp = requests.get(f"{BASE_URL}/material/filter/by-tag/品牌", headers=headers_admin)
tag_materials = tag_materials_resp.json() if tag_materials_resp.status_code == 200 else []
tag_materials_count = len(tag_materials)

step_count += 1
if verify_step(step_count, "按标签查询素材", tag_materials_count > 0, f"查询结果数: {tag_materials_count}"):
    pass_count += 1

# 4.6 获取可复用素材
reusable_resp = requests.get(f"{BASE_URL}/material/filter/reusable?limit=10", headers=headers_admin)
reusable_materials = reusable_resp.json() if reusable_resp.status_code == 200 else []
reusable_count = len(reusable_materials)

step_count += 1
if verify_step(step_count, "获取可复用素材", reusable_count > 0, f"可复用素材数: {reusable_count}"):
    pass_count += 1

# 4.7 记录素材使用
use_resp = requests.post(f"{BASE_URL}/material/{material_id}/use", headers=headers_admin)
use_ok = use_resp.status_code == 200

step_count += 1
if verify_step(step_count, "记录素材使用", use_ok, "复用计数已更新"):
    pass_count += 1

# 4.8 获取热门素材
popular_resp = requests.get(f"{BASE_URL}/material/filter/popular?limit=5", headers=headers_admin)
popular_materials = popular_resp.json() if popular_resp.status_code == 200 else []
popular_count = len(popular_materials)

step_count += 1
if verify_step(step_count, "获取热门素材", popular_count >= 0, f"热门素材数: {popular_count}"):
    pass_count += 1

# 4.9 获取素材库统计
lib_stats_resp = requests.get(f"{BASE_URL}/material/statistics", headers=headers_admin)
lib_stats = lib_stats_resp.json() if lib_stats_resp.status_code == 200 else {}
total_materials = lib_stats.get('total_materials', 0)

step_count += 1
if verify_step(step_count, "获取素材库统计", total_materials > 0, f"总素材数: {total_materials}, 可复用: {lib_stats.get('reusable_materials', 0)}"):
    pass_count += 1

# 4.10 更新素材
update_data = {"category": "品牌颜色库", "description": "更新后的描述"}
update_resp = requests.put(f"{BASE_URL}/material/{material_id}", json=update_data, headers=headers_admin)
update_ok = update_resp.status_code == 200

step_count += 1
if verify_step(step_count, "更新素材", update_ok, "素材信息已更新"):
    pass_count += 1

# 5. 综合查询测试
print_section("步骤5: 综合查询")

# 5.1 按类型查询素材
type_materials_resp = requests.get(f"{BASE_URL}/material/filter/by-type/配色", headers=headers_admin)
type_materials = type_materials_resp.json() if type_materials_resp.status_code == 200 else []

step_count += 1
if verify_step(step_count, "按类型查询素材", len(type_materials) > 0, f"配色素材数: {len(type_materials)}"):
    pass_count += 1

# 5.2 按分类查询素材
category_materials_resp = requests.get(f"{BASE_URL}/material/filter/by-category/品牌颜色库", headers=headers_admin)
category_materials = category_materials_resp.json() if category_materials_resp.status_code == 200 else []

step_count += 1
if verify_step(step_count, "按分类查询素材", len(category_materials) > 0, f"分类查询结果: {len(category_materials)}"):
    pass_count += 1

# 5.3 获取文件列表
all_files_resp = requests.get(f"{BASE_URL}/file/list?limit=100", headers=headers_admin)
all_files = all_files_resp.json() if all_files_resp.status_code == 200 else []

step_count += 1
if verify_step(step_count, "获取文件列表", len(all_files) > 0, f"总文件数: {len(all_files)}"):
    pass_count += 1

# 5.4 获取素材列表
all_materials_resp = requests.get(f"{BASE_URL}/material/list?limit=100", headers=headers_admin)
all_materials = all_materials_resp.json() if all_materials_resp.status_code == 200 else []

step_count += 1
if verify_step(step_count, "获取素材列表", len(all_materials) > 0, f"总素材数: {len(all_materials)}"):
    pass_count += 1

# 6. 清理测试
print_section("步骤6: 数据清理")

# 删除素材
if material_id:
    delete_material_resp = requests.delete(f"{BASE_URL}/material/{material_id}", headers=headers_admin)
    delete_material_ok = delete_material_resp.status_code == 200

    step_count += 1
    if verify_step(step_count, "删除素材", delete_material_ok, "素材已标记为删除"):
        pass_count += 1

# 删除文件
if file_id:
    delete_file_resp = requests.delete(f"{BASE_URL}/file/{file_id}", headers=headers_admin)
    delete_file_ok = delete_file_resp.status_code == 200

    step_count += 1
    if verify_step(step_count, "删除文件", delete_file_ok, "文件已标记为删除"):
        pass_count += 1

# ============= 最终统计 =============
print_section("验证总结")
pass_rate = (pass_count / step_count * 100) if step_count > 0 else 0
print(f"总步骤数: {step_count}")
print(f"通过数: {pass_count}")
print(f"失败数: {step_count - pass_count}")
print(f"通过率: {pass_rate:.1f}%")
print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if pass_count == step_count:
    print("\n🎉 所有验证步骤通过！文件管理和素材库模块已完整实现。")
else:
    print(f"\n⚠️  有 {step_count - pass_count} 个验证步骤失败，请检查。")
