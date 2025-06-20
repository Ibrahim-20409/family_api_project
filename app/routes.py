# ✅ FILE: app/routes.py
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.database import read_csv, write_csv, FAMILY_FILE, PERSON_FILE
from app.models import (
    Family, FamilyCreate, FamilyWithMembers,
    FamilyWithMembersCreate, Person, PersonInput
)
from app.auth import (
    authenticate_user, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES, Token,
    get_current_user, User
)

router = APIRouter()

# ✅ LOGIN route
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ PROTECTED ENDPOINTS
@router.get("/families", response_model=List[FamilyWithMembers])
def get_families(current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    persons = read_csv(PERSON_FILE)
    result = []
    for fam in families:
        fam_obj = Family(**fam)
        members = [Person(**p) for p in persons if int(p["Fid"]) == int(fam["Fid"])]
        result.append(FamilyWithMembers(family=fam_obj, members=members))
    return result

@router.get("/family-id")
def get_family_id_by_name(name: str = Query(..., alias="fname"), address: str = Query(None, alias="faddress"), current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    matching = [f for f in families if f["Fname"].lower() == name.lower()]
    if address:
        matching = [f for f in matching if f["Faddress"].lower() == address.lower()]
    if not matching:
        raise HTTPException(status_code=404, detail="No family found")
    return {"Fid(s)": [int(f["Fid"]) for f in matching]}

@router.get("/person-id")
def get_person_id_by_name(name: str = Query(..., alias="pname"), qualification: str = None, gender: str = None, current_user: User = Depends(get_current_user)):
    persons = read_csv(PERSON_FILE)
    matching = [p for p in persons if p["PName"].lower() == name.lower()]
    if qualification:
        matching = [p for p in matching if p["Qualification"].lower() == qualification.lower()]
    if gender:
        matching = [p for p in matching if p["Gender"].lower() == gender.lower()]
    if not matching:
        raise HTTPException(status_code=404, detail="No person found")
    return {"Pid(s)": [int(p["Pid"]) for p in matching]}

@router.get("/families/{fid}", response_model=FamilyWithMembers)
def get_family(fid: int, current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    persons = read_csv(PERSON_FILE)
    fam = next((f for f in families if int(f["Fid"]) == fid), None)
    if not fam:
        raise HTTPException(status_code=404, detail="Family not found")
    members = [Person(**p) for p in persons if int(p["Fid"]) == fid]
    return FamilyWithMembers(family=Family(**fam), members=members)

@router.post("/families")
def add_family(data: FamilyWithMembersCreate, current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    persons = read_csv(PERSON_FILE)
    new_fid = max([int(f["Fid"]) for f in families], default=0) + 1
    family_dict = {"Fid": str(new_fid), "Fname": data.family.Fname, "Faddress": data.family.Faddress}
    max_pid = max([int(p["Pid"]) for p in persons], default=0)
    new_members = []
    for i, member in enumerate(data.members, start=1):
        new_pid = max_pid + i
        member_dict = {
            "Pid": str(new_pid),
            "Fid": str(new_fid),
            "PName": member.PName,
            "Qualification": member.Qualification,
            "Gender": member.Gender
        }
        new_members.append(member_dict)
    families.append(family_dict)
    persons.extend(new_members)
    write_csv(FAMILY_FILE, families, ["Fid", "Fname", "Faddress"])
    write_csv(PERSON_FILE, persons, ["Pid", "Fid", "PName", "Qualification", "Gender"])
    return {"message": "Family and members added", "Fid": new_fid, "members_added": len(data.members)}

@router.post("/families/create", response_model=Family)
def create_family(data: FamilyCreate, current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    new_fid = max([int(f["Fid"]) for f in families], default=0) + 1
    new_family = {"Fid": str(new_fid), "Fname": data.Fname, "Faddress": data.Faddress}
    families.append(new_family)
    write_csv(FAMILY_FILE, families, ["Fid", "Fname", "Faddress"])
    return Family(Fid=new_fid, Fname=data.Fname, Faddress=data.Faddress)

@router.post("/families/{fid}/members")
def add_member_to_family(fid: int, member: PersonInput, current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    if not any(int(f["Fid"]) == fid for f in families):
        raise HTTPException(status_code=404, detail="Family not found")
    persons = read_csv(PERSON_FILE)
    new_pid = max([int(p["Pid"]) for p in persons], default=0) + 1
    new_member = {
        "Pid": str(new_pid),
        "Fid": str(fid),
        "PName": member.PName,
        "Qualification": member.Qualification,
        "Gender": member.Gender
    }
    persons.append(new_member)
    write_csv(PERSON_FILE, persons, ["Pid", "Fid", "PName", "Qualification", "Gender"])
    return {"message": "Member added", "Pid": new_pid}

@router.put("/families/{fid}")
def update_family(fid: int, data: FamilyCreate, current_user: User = Depends(get_current_user)):
    families = read_csv(FAMILY_FILE)
    family = next((f for f in families if int(f["Fid"]) == fid), None)
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    family["Fname"] = data.Fname
    family["Faddress"] = data.Faddress
    write_csv(FAMILY_FILE, families, ["Fid", "Fname", "Faddress"])
    return {"message": "Family updated"}

@router.put("/persons/{pid}")
def update_person(pid: int, data: PersonInput, current_user: User = Depends(get_current_user)):
    persons = read_csv(PERSON_FILE)
    person = next((p for p in persons if int(p["Pid"]) == pid), None)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    person["PName"] = data.PName
    person["Qualification"] = data.Qualification
    person["Gender"] = data.Gender
    write_csv(PERSON_FILE, persons, ["Pid", "Fid", "PName", "Qualification", "Gender"])
    return {"message": "Person updated"}

@router.delete("/families/{fid}")
def delete_family(fid: int, current_user: User = Depends(get_current_user)):
    families = [f for f in read_csv(FAMILY_FILE) if int(f["Fid"]) != fid]
    persons = [p for p in read_csv(PERSON_FILE) if int(p["Fid"]) != fid]
    write_csv(FAMILY_FILE, families, ["Fid", "Fname", "Faddress"])
    write_csv(PERSON_FILE, persons, ["Pid", "Fid", "PName", "Qualification", "Gender"])
    return {"message": "Family and its members deleted"}

@router.delete("/person/{pid}")
def delete_person(pid: int, current_user: User = Depends(get_current_user)):
    persons = read_csv(PERSON_FILE)
    new_persons = [p for p in persons if int(p["Pid"]) != pid]
    if len(new_persons) == len(persons):
        raise HTTPException(status_code=404, detail="Person not found")
    write_csv(PERSON_FILE, new_persons, ["Pid", "Fid", "PName", "Qualification", "Gender"])
    return {"message": f"Person with Pid={pid} deleted"}
