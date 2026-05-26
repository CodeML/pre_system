from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Boolean, Float
from models.base import BaseModel
from datetime import datetime

class Comment(BaseModel):
    """
    统一协作评论与批注系统
    支持：项目、任务、文件、改稿记录
    """
    __tablename__ = "comments"

    # 多态关联
    target_type = Column(String(50), nullable=False, index=True, comment="对象类型(project/task/file/revision)")
    target_id = Column(Integer, nullable=False, index=True, comment="对应ID")
    
    # 核心内容
    content = Column(Text, nullable=False, comment="评论内容")
    mentions = Column(JSON, nullable=True, comment="提及的人员ID列表")
    attachments = Column(JSON, nullable=True, comment="附件URL列表")
    
    # 画布级批注功能 (Canvas Annotation)
    pos_x = Column(Float, nullable=True, comment="X坐标(0-1)")
    pos_y = Column(Float, nullable=True, comment="Y坐标(0-1)")
    width = Column(Float, nullable=True, comment="标注区域宽度")
    height = Column(Float, nullable=True, comment="标注区域高度")
    
    # 深度增强：多画板/多页支持
    page_index = Column(Integer, default=0, comment="画板或页面索引")
    artboard_id = Column(String(100), nullable=True, comment="画板唯一ID(适配Figma/Sketch等)")
    
    # 深度增强：标注类型
    # type: point(点), rect(矩形), circle(圆), arrow(箭头), freehand(手绘)
    annotation_type = Column(String(20), default="point", comment="标注图形类型")
    
    # 终极增强：批注状态跟踪
    # status: open(待解决), resolved(已解决), ignored(已忽略), reopened(重新打开)
    annotation_status = Column(String(20), default="open", comment="批注解决状态")
    
    # 意见分类与来源（用于治理沟通黑洞）
    category = Column(String(50), nullable=True, comment="反馈类别")
    client_role = Column(String(50), nullable=True, comment="甲方角色(老板/运营/市场)")
    
    # 工业级增强：审阅人身份标识 (Reviewer Identity)
    # identity: owner, operation, marketing, legal, etc.
    reviewer_identity = Column(String(50), nullable=True, comment="审阅人具体身份标识")
    
    # 层级关系
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True, comment="父评论ID")
    
    # 作者
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 状态
    is_internal = Column(Boolean, default=False, comment="是否仅内部可见（客户不可见）")
    # is_resolved 保留为了向下兼容，但逐渐被 annotation_status 替代
    is_resolved = Column(Boolean, default=False, comment="标记为已解决（改稿点）")
