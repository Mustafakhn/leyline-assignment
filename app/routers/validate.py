from fastapi import APIRouter, HTTPException
from app.schemas import ValidateIPRequest
from app.models import ValidateIPResponse
import ipaddress

router = APIRouter()


@router.post("/v1/tools/validate", response_model=ValidateIPResponse)
async def validate_ip(request: ValidateIPRequest):
    try:
        ipaddress.ip_address(request.ip)
        return ValidateIPResponse(status=True)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid IP address")