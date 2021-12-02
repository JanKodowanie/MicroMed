from pydantic import BaseModel
from datetime import datetime
from pydantic.types import UUID4
from common.enums import AccountStatus, AccountRole

    
class TokenDataSchema(BaseModel):
    sub: UUID4
    username: str
    role: AccountRole
    status: AccountStatus
    exp: datetime