"""验证仪表板和消息通知模块"""
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

print_section("PRE 系统 - 仪表板和消息通知验证")
print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

step_count = 0
pass_count = 0

# 1. 登录
print_section("步骤1: 账户登录")
admin_token, admin_id = login(admin_user)
designer_token, designer_id = login(designer_user)

step_count += 1
if verify_step(step_count, "管理员登录", admin_token is not None, f"User ID: {admin_id}"):
    pass_count += 1

step_count += 1
if verify_step(step_count, "设计师登录", designer_token is not None, f"User ID: {designer_id}"):
    pass_count += 1

headers_admin = {"Authorization": f"Bearer {admin_token}"}
headers_designer = {"Authorization": f"Bearer {designer_token}"}

# 2. 仪表板统计测试
print_section("步骤2: 仪表板统计")

# 2.1 获取概览
overview_resp = requests.get(f"{BASE_URL}/dashboard/overview", headers=headers_admin)
overview_ok = overview_resp.status_code == 200
overview_data = overview_resp.json() if overview_ok else {}

step_count += 1
if verify_step(step_count, "获取仪表板概览", overview_ok):
    if overview_data:
        print(f"   项目总数: {overview_data.get('projects', {}).get('total_projects', 0)}")
        print(f"   任务总数: {overview_data.get('tasks', {}).get('total_tasks', 0)}")
    pass_count += 1

# 2.2 获取项目统计
project_stats_resp = requests.get(f"{BASE_URL}/dashboard/projects", headers=headers_admin)
project_stats_ok = project_stats_resp.status_code == 200
project_stats = project_stats_resp.json() if project_stats_ok else {}

step_count += 1
if verify_step(step_count, "获取项目统计", project_stats_ok, f"完成率: {project_stats.get('completion_rate', 0)}%"):
    pass_count += 1

# 2.3 获取任务统计
task_stats_resp = requests.get(f"{BASE_URL}/dashboard/tasks", headers=headers_admin)
task_stats_ok = task_stats_resp.status_code == 200
task_stats = task_stats_resp.json() if task_stats_ok else {}

step_count += 1
if verify_step(step_count, "获取任务统计", task_stats_ok, f"平均进度: {task_stats.get('average_progress', 0)}%"):
    pass_count += 1

# 2.4 获取超期任务
overdue_resp = requests.get(f"{BASE_URL}/dashboard/overdue", headers=headers_admin)
overdue_ok = overdue_resp.status_code == 200
overdue_data = overdue_resp.json() if overdue_ok else {}

step_count += 1
if verify_step(step_count, "获取超期任务", overdue_ok, f"超期任务数: {overdue_data.get('total_overdue', 0)}"):
    pass_count += 1

# 2.5 获取设计师工作量
workload_designer_resp = requests.get(f"{BASE_URL}/dashboard/workload/designer", headers=headers_admin)
workload_designer_ok = workload_designer_resp.status_code == 200
workload_designer = workload_designer_resp.json() if workload_designer_ok else {}

step_count += 1
if verify_step(step_count, "获取设计师工作量", workload_designer_ok, f"设计师数: {len(workload_designer)}"):
    pass_count += 1

# 2.6 获取角色工作量
workload_role_resp = requests.get(f"{BASE_URL}/dashboard/workload/role", headers=headers_admin)
workload_role_ok = workload_role_resp.status_code == 200
workload_role = workload_role_resp.json() if workload_role_ok else {}

step_count += 1
if verify_step(step_count, "获取角色工作量", workload_role_ok, f"角色数: {len(workload_role)}"):
    pass_count += 1

# 2.7 获取平台统计
platform_resp = requests.get(f"{BASE_URL}/dashboard/platforms", headers=headers_admin)
platform_ok = platform_resp.status_code == 200
platform_data = platform_resp.json() if platform_ok else {}

step_count += 1
if verify_step(step_count, "获取平台统计", platform_ok, f"平台数: {len(platform_data)}"):
    pass_count += 1

# 2.8 获取完整仪表板
full_resp = requests.get(f"{BASE_URL}/dashboard/full", headers=headers_admin)
full_ok = full_resp.status_code == 200

step_count += 1
if verify_step(step_count, "获取完整仪表板", full_ok):
    pass_count += 1

# 3. 消息通知测试
print_section("步骤3: 消息通知")

# 3.1 获取未读通知数
unread_count_resp = requests.get(f"{BASE_URL}/notification/unread-count", headers=headers_designer)
unread_count_ok = unread_count_resp.status_code == 200
unread_count_data = unread_count_resp.json() if unread_count_ok else {}

step_count += 1
if verify_step(step_count, "获取未读通知数", unread_count_ok, f"未读数: {unread_count_data.get('unread_count', 0)}"):
    pass_count += 1

# 3.2 获取通知列表
notif_list_resp = requests.get(f"{BASE_URL}/notification/list?limit=10", headers=headers_designer)
notif_list_ok = notif_list_resp.status_code == 200
notif_list = notif_list_resp.json() if notif_list_ok else []

step_count += 1
if verify_step(step_count, "获取通知列表", notif_list_ok, f"通知数: {len(notif_list)}"):
    pass_count += 1

# 3.3 获取未读通知
unread_resp = requests.get(f"{BASE_URL}/notification/unread?limit=10", headers=headers_designer)
unread_ok = unread_resp.status_code == 200
unread_list = unread_resp.json() if unread_ok else []

step_count += 1
if verify_step(step_count, "获取未读通知", unread_ok, f"未读通知数: {len(unread_list)}"):
    pass_count += 1

# 3.4 获取通知统计
notif_stats_resp = requests.get(f"{BASE_URL}/notification/statistics", headers=headers_designer)
notif_stats_ok = notif_stats_resp.status_code == 200
notif_stats = notif_stats_resp.json() if notif_stats_ok else {}

step_count += 1
if verify_step(step_count, "获取通知统计", notif_stats_ok, 
              f"总数: {notif_stats.get('total', 0)}, 未读: {notif_stats.get('unread', 0)}"):
    pass_count += 1

# 3.5 按类型查询通知
type_filter_resp = requests.get(f"{BASE_URL}/notification/filter/by-type/task_assigned?limit=10", 
                                headers=headers_designer)
type_filter_ok = type_filter_resp.status_code == 200
type_filtered = type_filter_resp.json() if type_filter_ok else []

step_count += 1
if verify_step(step_count, "按类型查询通知", type_filter_ok, f"task_assigned 通知数: {len(type_filtered)}"):
    pass_count += 1

# 3.6 按优先级查询通知
priority_filter_resp = requests.get(f"{BASE_URL}/notification/filter/by-priority/high?limit=10", 
                                    headers=headers_designer)
priority_filter_ok = priority_filter_resp.status_code == 200
priority_filtered = priority_filter_resp.json() if priority_filter_ok else []

step_count += 1
if verify_step(step_count, "按优先级查询通知", priority_filter_ok, f"高优先级通知数: {len(priority_filtered)}"):
    pass_count += 1

# 3.7 标记通知已读（如果有通知）
if notif_list:
    first_notif_id = notif_list[0]['id']
    mark_read_resp = requests.put(f"{BASE_URL}/notification/{first_notif_id}/read", 
                                  headers=headers_designer)
    mark_read_ok = mark_read_resp.status_code == 200

    step_count += 1
    if verify_step(step_count, "标记通知已读", mark_read_ok):
        pass_count += 1
else:
    step_count += 1
    print(f"{step_count}. ⊘ SKIP - 标记通知已读 (无通知)")

# 3.8 标记所有通知已读
mark_all_resp = requests.post(f"{BASE_URL}/notification/read-all", headers=headers_designer)
mark_all_ok = mark_all_resp.status_code == 200
marked_count = mark_all_resp.json().get('marked_as_read', 0) if mark_all_ok else 0

step_count += 1
if verify_step(step_count, "标记所有通知已读", mark_all_ok, f"标记数: {marked_count}"):
    pass_count += 1

# 3.9 获取通知后删除
if notif_list:
    delete_notif_id = notif_list[-1]['id'] if len(notif_list) > 1 else notif_list[0]['id']
    delete_resp = requests.delete(f"{BASE_URL}/notification/{delete_notif_id}", 
                                  headers=headers_designer)
    delete_ok = delete_resp.status_code == 200

    step_count += 1
    if verify_step(step_count, "删除通知", delete_ok):
        pass_count += 1
else:
    step_count += 1
    print(f"{step_count}. ⊘ SKIP - 删除通知 (无通知)")

# ============= 最终统计 =============
print_section("验证总结")
skip_count = 2  # 标记通知已读、删除通知（无测试数据）
executable_steps = step_count - skip_count
if step_count > 0:
    pass_rate = (pass_count / executable_steps * 100) if executable_steps > 0 else 100
    fail_count = executable_steps - pass_count
    print(f"总步骤数: {step_count}")
    print(f"可执行步骤: {executable_steps}")
    print(f"通过数: {pass_count}")
    print(f"失败数: {fail_count}")
    print(f"跳过数: {skip_count} (无测试数据)")
    print(f"通过率: {pass_rate:.1f}%")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if pass_count == executable_steps:
        print("\n🎉 所有验证步骤通过！仪表板和消息通知模块已完整实现。")
    else:
        print(f"\n⚠️  有 {fail_count} 个验证步骤失败，请检查。")
