from typing import TypedDict


class PartnershipInstitution(TypedDict):
    educational_institution: str
    parent: str


class PartnershipBusiness(TypedDict):
    business: str
    parent: str
