from fastapi import APIRouter, HTTPException, Request


router = APIRouter(prefix="/leads")


@router.get("/{lead_id}")
def get_leads_by_id(lead_id: int) -> Lead:
    if lead_id not in leads:
        raise HTTPException(status_code=404, detail="data not found")

    return leads[lead_id]


@router.post("/")
def add_lead(lead: Lead) -> dict[str, Lead]:
    if lead.id in leads:
        raise HTTPException(status_code=400, detail="already exists")

    leads[lead.id] = lead
    return {"added": lead}
