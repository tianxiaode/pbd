from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SecurityLog(BaseModel):
    application_name: Optional[str] = None
    identity: Optional[str] = None
    action: Optional[str] = None
    extra_properties: Optional[dict] = {}
    user_id: Optional[UUID] = None
    username: Optional[str] = None
    tenant_id: Optional[UUID] = None
    tenant_name: Optional[str] = None
    client_id: Optional[str] = None
    correlation_id: Optional[str] = None
    client_ip: Optional[str] = None
    browser_info: Optional[str] = None
    created_at: Optional[datetime] = None
