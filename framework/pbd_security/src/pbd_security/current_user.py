from typing import List, Union


class CurrentUser:

    is_authenticated: bool = False
    id: str = None
    username: str = None
    name: str = None
    surname: str = None
    email: str = None
    email_verified: bool = False
    phone_number: str = None
    phone_number_verified: bool = False
    tenant_id: str = None
    roles: List[str] = []
    claims: dict = {}

    def __init__(self, id: str, username: str, name: str, surname: str, email: str, email_verified: bool,
                 phone_number: str, phone_number_verified: bool, tenant_id: str, roles: List[str], claims: dict):
        self.id = id
        self.username = username
        self.name = name
        self.surname = surname
        self.email = email
        self.email_verified = email_verified
        self.phone_number = phone_number
        self.phone_number_verified = phone_number_verified
        self.tenant_id = tenant_id
        self.roles = roles
        self.claims = claims
        self.is_authenticated = True
    
    def is_in_role(self, role: str) -> bool:
        return role in self.roles
    
    def has_claim(self, claim: str) -> bool:
        return claim in self.claims
    
    def find_claim(self, claim: str) -> Union[str, None]:
        return self.claims.get(claim, None) 
    
    def get_all_claims(self) -> dict:
        return self.claims or {}





