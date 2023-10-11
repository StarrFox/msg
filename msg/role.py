from pydantic import BaseModel

from msg.permissions import Permissions


class Role(BaseModel):
    id: int
    positive_permissions: Permissions
    negative_permissions: Permissions
    name: str
    is_tag: bool









