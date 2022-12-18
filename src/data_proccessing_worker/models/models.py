from sqlalchemy import Column, String

from data_proccessing_worker.models.abstract import IDBase, TimestampBase


class IndicatorsContextSources(IDBase, TimestampBase):
    __tablename__ = "indicators_context_sources"

    ioc_type = Column(String(50))
    source_url = Column(String(255))
    inbound_removable_prefix = Column(String(150))
    outbound_appendable_prefix = Column(String(150))
