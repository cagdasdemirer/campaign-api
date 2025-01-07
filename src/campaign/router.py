import logging
from fastapi import APIRouter, Query
from .schemas import ResponseModel
from typing import Optional
from .dependencies import DBSessionDep
from .service import get_campaigns_data

campaign_router = APIRouter(
    prefix="/campaigns",
    tags=["Campaigns"],
)

logger = logging.getLogger("campaign_router")

@campaign_router.get("/", response_model=ResponseModel, status_code=200, description="Get campaigns data", responses={404: {"description": "No campaign data found for the specified filters."}})
async def get_campaigns(db_session: DBSessionDep,
                        campaign_id: Optional[str] = Query(None),
                        start_date: Optional[str] = Query(None),
                        end_date: Optional[str] = Query(None)):
    logger.info(f"Received request to get campaigns data with campaign_id: {campaign_id}, start_date: {start_date}, end_date: {end_date}")
    result = await get_campaigns_data(db_session, campaign_id, start_date, end_date)
    logger.info(f"Returning campaigns data")
    return result
