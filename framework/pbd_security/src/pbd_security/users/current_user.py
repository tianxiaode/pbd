from typing import List, Optional, Union


class CurrentUser:

    is_authenticated: bool = False
    id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = False
    phone_number: Optional[str] = None
    phone_number_verified: Optional[bool] = False
    tenant_id: Optional[str] = None
    roles: List[str] = []
    claims: dict = {}

    def __init__(self, 
        id: Optional[str] = None, 
        username: Optional[str] = None, 
        name: Optional[str] = None, 
        surname: Optional[str] = None, 
        email: Optional[str] = None, 
        email_verified: Optional[bool] = None,
        phone_number: Optional[str] = None, 
        phone_number_verified: Optional[bool] = None, 
        tenant_id: Optional[str] = None, 
        roles: List[str] = [], 
        claims: dict = {}
    ):
        self.id = id
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.email_verified = email_verified
        self.phone_number = phone_number
        self.phone_number_verified = phone_number_verified
        self.tenant_id = tenant_id
        self.roles = roles or []
        self.claims = claims or {}
        self.is_authenticated = True
    
    def is_in_role(self, role: str) -> bool:
        return role in self.roles
    
    def has_claim(self, claim: str) -> bool:
        return claim in self.claims
    
    def find_claim(self, claim: str) -> Union[str, None]:
        return self.claims.get(claim, None) 
    
    def get_all_claims(self) -> dict:
        return self.claims or {}





