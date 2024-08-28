from fastapi import APIRouter, HTTPException
import socket
from app.database import save_query
from app.models import LookupResponse

router = APIRouter()


@router.get("/v1/tools/lookup", response_model=LookupResponse)
async def lookup(domain: str):
    try:
        ipv4_addresses = socket.gethostbyname_ex(domain)[2]
        ipv4_only = [ip for ip in ipv4_addresses if "." in ip]
        save_query(domain, ipv4_only)
        print(ipv4_only)
        return {"ipv4_adresses": ipv4_only}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
