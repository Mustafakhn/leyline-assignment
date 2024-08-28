from fastapi import APIRouter
from app.database import get_recent_queries
from app.models import HistoryResponse

router = APIRouter()


@router.get("/v1/history", response_model=HistoryResponse)
async def history():
    queries = get_recent_queries()
    return queries
