from sqlalchemy import Column, String, Integer, Float

from . import Base


class DailyCampaign(Base):
    __tablename__ = "tbl_daily_campaigns"
    id = Column('campaign_id', String(64), nullable=True, primary_key=True)
    date = Column(String(50), nullable=True, primary_key=True)
    impressions = Column(Integer, nullable=True)
    clicks = Column(Integer, nullable=True)
    name = Column('campaign_name', String(50), nullable=True)
    cpm = Column(Float, nullable=True)
    views = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Daily Campaign: {self.id}-{self.name}>"

class DailyScore(Base):
    __tablename__ = 'tbl_daily_scores'
    id = Column('campaign_id', String(64), nullable=True, primary_key=True)
    date = Column(String(50), nullable=True, primary_key=True)
    media = Column(Integer, nullable=True)
    name = Column('campaign_name', String(50), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    effectiveness = Column(Float, nullable=True)
    status = Column(Integer, nullable=True)
    creative = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Daily Score: {self.id}-{self.name}>"