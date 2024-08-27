from fastapi import APIRouter
import re

router = APIRouter()


@router.get("/v1/tools/validate")
async def validate_ip(ip: str):
    ipv4_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    is_valid = bool(ipv4_pattern.match(ip))
    return {"is_valid_ipv4": is_valid}
