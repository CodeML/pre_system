from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class SalesLeadBase(BaseModel):
    name: str
    phone: Optional[str] = None
    source: Optional[str] = None
    status: str = "new"
    priority: str = "normal"
    owner_id: Optional[int] = None
    next_follow_up: Optional[datetime] = None
    remark: Optional[str] = None


class SalesLeadCreate(SalesLeadBase):
    pass


class SalesLeadRead(SalesLeadBase):
    id: int
    create_time: datetime
    last_follow_up: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class DesignPackageBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    unit: str = "套"
    include_revisions: int = 3
    is_active: bool = True
    category: Optional[str] = None


class DesignPackageCreate(DesignPackageBase):
    pass


class DesignPackageRead(DesignPackageBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CaseWorkBase(BaseModel):
    title: str
    description: Optional[str] = None
    cover_url: str
    content_urls: Optional[str] = None
    project_id: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_public: bool = True


class CaseWorkCreate(CaseWorkBase):
    pass


class CaseWorkRead(CaseWorkBase):
    id: int
    create_time: datetime
    model_config = ConfigDict(from_attributes=True)
