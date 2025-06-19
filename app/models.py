from pydantic import BaseModel
from typing import List, Optional

class FamilyCreate(BaseModel):
    Fname: str
    Faddress: str

class Family(FamilyCreate):
    Fid: int

class PersonInput(BaseModel):
    PName: str
    Qualification: str
    Gender: str

class Person(PersonInput):
    Pid: int
    Fid: int

class FamilyWithMembers(BaseModel):
    family: Family
    members: List[Person]

class FamilyWithMembersCreate(BaseModel):
    family: FamilyCreate
    members: List[PersonInput]