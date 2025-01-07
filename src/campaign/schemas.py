from pydantic import BaseModel
from typing import Dict, List


class CampaignCard(BaseModel):
    campaignName: str = "All"
    range: str
    days: int

class CurrentMetrics(BaseModel):
    impressions: int
    clicks: int
    views: int

class PerformanceMetrics(BaseModel):
    currentMetrics: CurrentMetrics

class ImpressionsCpm(BaseModel):
    impression: Dict[str, int]
    cpm: Dict[str, float]

class VolumeUnitCostTrend(BaseModel):
    impressionsCpm: ImpressionsCpm

class CampaignTable(BaseModel):
    start_date: List[str]
    end_date: List[str]
    adin_id: List[str]
    campaign: List[str]
    effectiveness: List[int]
    media: List[int]
    creative: List[int]


class ResponseModel(BaseModel):
    campaignCard: CampaignCard
    performanceMetrics: PerformanceMetrics
    volumeUnitCostTrend: VolumeUnitCostTrend
    campaignTable: CampaignTable
