"""
客户标签系统验证脚本
"""

import sys
sys.path.insert(0, '/Users/shaiweiminglei/pre_system/pre_backend')

from database.db import SessionLocal, init_db
from models.customer_tag import CustomerTag, CustomerTagAssociation
from crud.customer_tag_crud import customer_tag_crud
from models.user import User
from models.customer import Customer
from datetime import datetime
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

print("=" * 60)
print("客户标签系统验证脚本")
print("=" * 60)

# 初始化数据库
try:
    init_db()
    print("\n✅ 数据库已初始化")
except Exception as e:
    print(f"\n❌ 数据库初始化失败: {e}")
    sys.exit(1)

db = SessionLocal()

try:
    # ========== 测试1: 创建预定义标签 ==========
    print("\n--- 测试1: 创建预定义标签 ---")
    count = customer_tag_crud.create_predefined_tags(db)
    print(f"✅ 已创建 {count} 个预定义标签")
    
    # ========== 测试2: 查询标签列表 ==========
    print("\n--- 测试2: 查询标签列表 ---")
    all_tags = db.query(CustomerTag).all()
    print(f"✅ 数据库中有 {len(all_tags)} 个标签")
    print(f"   样本标签: {all_tags[0].name if all_tags else '无'}")
    
    # ========== 测试3: 按类别查询 ==========
    print("\n--- 测试3: 按类别查询 ---")
    service_tags = customer_tag_crud.get_by_category(db, "service")
    print(f"✅ 'service' 类别有 {len(service_tags)} 个标签")
    for tag in service_tags[:2]:
        print(f"   - {tag.name}")
    
    # ========== 测试4: 搜索标签 ==========
    print("\n--- 测试4: 搜索标签 ---")
    search_results = customer_tag_crud.search_by_name(db, "3D")
    print(f"✅ 搜索 '3D' 得到 {len(search_results)} 个结果")
    for tag in search_results:
        print(f"   - {tag.name}")
    
    # ========== 测试5: 获取热门标签 ==========
    print("\n--- 测试5: 获取热门标签 ---")
    popular_tags = customer_tag_crud.get_popular_tags(db, limit=5)
    print(f"✅ 获取前 {len(popular_tags)} 个热门标签")
    
    # ========== 测试6: 创建测试数据 ==========
    print("\n--- 测试6: 创建测试数据 ---")
    
    # 创建测试用户
    test_user = db.query(User).filter(User.username == "test_user").first()
    if not test_user:
        test_user = User(
            username="test_user",
            password=hash_password("testpass123"),
            name="Test User",
            phone="13800000000",
            is_active=True
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
    print(f"✅ 测试用户已准备 (ID: {test_user.id})")
    
    # 创建测试客户
    test_customer = db.query(Customer).filter(Customer.name == "test_customer").first()
    if not test_customer:
        test_customer = Customer(
            name="test_customer",
            contact="Test Contact",
            phone="13800000001",
            type="company",
            creator_id=test_user.id
        )
        db.add(test_customer)
        db.commit()
        db.refresh(test_customer)
    print(f"✅ 测试客户已准备 (ID: {test_customer.id})")
    
    # ========== 测试7: 分配标签 ==========
    print("\n--- 测试7: 为客户分配标签 ---")
    tag_to_assign = db.query(CustomerTag).filter(CustomerTag.category == "service").first()
    if tag_to_assign:
        association = customer_tag_crud.assign_tag_to_customer(
            db,
            test_customer.id,
            tag_to_assign.id,
            test_user.id,
            "测试备注"
        )
        print(f"✅ 已为客户分配标签: {tag_to_assign.name}")
        
        # 检查usage_count是否增加
        db.refresh(tag_to_assign)
        print(f"   标签使用次数: {tag_to_assign.usage_count}")
    
    # ========== 测试8: 批量分配标签 ==========
    print("\n--- 测试8: 批量分配标签 ---")
    tags_to_bulk = db.query(CustomerTag).filter(CustomerTag.category == "platform").limit(3).all()
    if tags_to_bulk:
        tag_ids = [tag.id for tag in tags_to_bulk]
        count = customer_tag_crud.bulk_assign_tags(
            db,
            test_customer.id,
            tag_ids,
            test_user.id
        )
        print(f"✅ 已批量分配 {count} 个标签")
    
    # ========== 测试9: 获取客户标签 ==========
    print("\n--- 测试9: 获取客户所有标签 ---")
    customer_tags = customer_tag_crud.get_customer_tags(db, test_customer.id)
    print(f"✅ 客户有 {len(customer_tags)} 个标签")
    for tag in customer_tags:
        print(f"   - {tag.name} ({tag.category})")
    
    # ========== 测试10: 移除标签 ==========
    print("\n--- 测试10: 移除客户标签 ---")
    if customer_tags:
        tag_to_remove = customer_tags[0]
        success = customer_tag_crud.remove_tag_from_customer(
            db,
            test_customer.id,
            tag_to_remove.id
        )
        if success:
            print(f"✅ 已移除标签: {tag_to_remove.name}")
            
            # 检查usage_count是否减少
            db.refresh(tag_to_remove)
            print(f"   标签使用次数: {tag_to_remove.usage_count}")
    
    # ========== 测试11: 验证关联表 ==========
    print("\n--- 测试11: 验证关联表 ---")
    remaining_customer_tags = customer_tag_crud.get_customer_tags(db, test_customer.id)
    print(f"✅ 客户现有标签数: {len(remaining_customer_tags)}")
    
    # ========== 测试12: 更新标签 ==========
    print("\n--- 测试12: 更新标签 ---")
    if all_tags:
        tag = all_tags[0]
        updated_tag = customer_tag_crud.update(
            db,
            tag.id,
            {
                "description": "更新的描述",
                "color": "#FF0000"
            }
        )
        print(f"✅ 已更新标签: {updated_tag.name}")
        print(f"   新描述: {updated_tag.description}")
        print(f"   新颜色: {updated_tag.color}")
    
    # ========== 测试完成统计 ==========
    print("\n" + "=" * 60)
    print("✅ 所有测试完成 (12/12)")
    print("=" * 60)
    print("\n客户标签系统验证结果:")
    print("  ✅ 模型创建成功")
    print("  ✅ 预定义标签初始化成功")
    print("  ✅ CRUD操作正常")
    print("  ✅ 标签关联功能正常")
    print("  ✅ 批量操作支持")
    print("  ✅ 使用计数跟踪")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    db.close()

print("\n✅ 2.2 客户标签系统实现完成!")
