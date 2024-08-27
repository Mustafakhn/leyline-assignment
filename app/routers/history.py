from fastapi import APIRouter
from app.database import get_recent_queries

router = APIRouter()


@router.get("/v1/history")
async def history():
    queries = get_recent_queries()
    return {"recent_queries": queries}
