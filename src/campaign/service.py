from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.sql.functions import coalesce, min, max, func
import logging
from .models import DailyCampaign, DailyScore
from .schemas import ResponseModel, CampaignCard, PerformanceMetrics, CurrentMetrics, VolumeUnitCostTrend, \
    ImpressionsCpm, CampaignTable
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .utils import transform_date_strings

logger = logging.getLogger("campaign_service")

async def get_campaigns_data(db_session: AsyncSession,
                             campaign_id: Optional[str] = None,
                             start_date: Optional[str] = None,
                             end_date: Optional[str] = None) -> ResponseModel:
    filters = []
    if campaign_id:
        filters.append(DailyCampaign.id == campaign_id)
    if start_date:
        filters.append(DailyCampaign.date >= start_date)
    if end_date:
        filters.append(DailyCampaign.date <= end_date)

    query_campaign = select(
        DailyCampaign.id,
        DailyCampaign.name,
        DailyCampaign.date,
        DailyCampaign.impressions,
        DailyCampaign.clicks,
        DailyCampaign.views,
        DailyCampaign.cpm,
    ).filter(*filters).order_by(DailyCampaign.date)

    result = await db_session.execute(query_campaign)
    rows = result.all()

    if not rows:
        logger.error("No campaign data found for the specified filters:")
        raise HTTPException(status_code=404, detail="No campaign data found for the specified filters.")

    logger.info(f"Found {len(rows)} rows of filtered campaign data.")

    total_impressions = 0
    total_clicks = 0
    total_views = 0
    impressions_dict = {}
    cpm_dict  = {}

    for row in rows:
        id, name, date, impressions, clicks, views, cpm = row
        total_impressions += impressions
        total_clicks += clicks
        total_views += views

        if date not in impressions_dict:
            impressions_dict[date] = impressions
            cpm_dict[date] = round(cpm,2)
        else:
            impressions_dict[date] += impressions
            cpm_dict[date] += round(cpm,2)

    # Set daily_campaign table as real ranges and handle missing values in daily_scores table as 0
    query = (
        select(
            DailyCampaign.id,
            DailyCampaign.name,
            min(DailyScore.start_date).label('start_date'),
            max(DailyScore.end_date).label('end_date'),
            func.avg(coalesce(DailyScore.media, 0)).label('media'),
            func.avg(coalesce(DailyScore.effectiveness,0.0)).label('effectiveness'),
            func.avg(coalesce(DailyScore.creative, 0.0)).label('creative'),
        )
    .join(DailyScore, and_(DailyCampaign.id == DailyScore.id,
          DailyCampaign.date == DailyScore.date), isouter=True)
    .group_by(DailyCampaign.id, DailyCampaign.name)
    .order_by(min(DailyCampaign.date))
    )

    result = await db_session.execute(query)
    rows = result.all()

    if not rows:
        logger.error("No score data found.")
        raise HTTPException(status_code=404, detail="No score data found.")

    logger.info(f"Found {len(rows)} rows of all campaign data.")

    campaign_table = {
        'start_date': [],
        'end_date': [],
        'adin_id': [],
        'campaign': [],
        'effectiveness': [],
        'media': [],
        'creative': []
    }

    for row in rows:
        id, name, score_start_date, score_end_date, media, effectiveness, creative = row
        campaign_table['start_date'].append(score_start_date)
        campaign_table['end_date'].append(score_end_date)
        campaign_table['adin_id'].append(id)
        campaign_table['campaign'].append(name)
        campaign_table['effectiveness'].append(round(effectiveness))
        campaign_table['media'].append(round(media))
        campaign_table['creative'].append(round(creative))

    if campaign_id:
        index = campaign_table['adin_id'].index(campaign_id)
        campaign_name = campaign_table['campaign'][index]
        start_date = campaign_table['start_date'][index]
        end_date = campaign_table['end_date'][index]
    else:
        campaign_name = "All" # Default value if campaign_id not provided
        if start_date:
            start_date = start_date
        else: # First date occurrence of campaign in daily_campaign table if parameter not provided
            start_date = list(impressions_dict.keys())[0]

        if end_date:
            end_date = end_date
        else: # Last date occurrence of campaign in daily_campaign table if parameter not provided
            end_date = list(impressions_dict.keys())[-1]


    interval, dates_range= transform_date_strings(start_date, end_date)

    return ResponseModel(
    campaignCard=CampaignCard(
        campaignName= campaign_name,
        range=dates_range,
        days=interval
    ),
    performanceMetrics=PerformanceMetrics(
        currentMetrics=CurrentMetrics(
            impressions=total_impressions,
            clicks=total_clicks,
            views=round(total_views)
        )
    ),
    volumeUnitCostTrend=VolumeUnitCostTrend(
        impressionsCpm=ImpressionsCpm(
            impression=impressions_dict,
            cpm=cpm_dict
        )
    ),
    campaignTable=CampaignTable(
        start_date=campaign_table["start_date"],
        end_date=campaign_table["end_date"],
        adin_id=campaign_table["adin_id"],
        campaign=campaign_table["campaign"],
        effectiveness=campaign_table["effectiveness"],
        media=campaign_table["media"],
        creative=campaign_table["creative"]
    )
)









