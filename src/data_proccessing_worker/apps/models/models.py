from sqlalchemy import Column, String, and_, null
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, BYTEA, UUID
from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Boolean, UniqueConstraint,
    BigInteger, ForeignKey, DECIMAL, text
)


from data_proccessing_worker.apps.models.abstract import IDBase, TimestampBase


class IndicatorsContextSources(IDBase, TimestampBase):
    __tablename__ = "indicators_context_sources"

    ioc_type = Column(String(50))
    source_url = Column(String(255))
    inbound_removable_prefix = Column(String(150))
    outbound_appendable_prefix = Column(String(150))


class Feed(IDBase, TimestampBase):
    __tablename__ = "feeds"

    title = Column(String(128))
    provider = Column(String(128))
    format = Column(String(8))
    url = Column(String(128))
    auth_type = Column(String(16))
    auth_api_token = Column(Text)
    auth_login = Column(String(32))
    auth_pass = Column(String(32))
    certificate = Column(Text)
    use_taxii = Column(Boolean)
    polling_frequency = Column(String(32))
    weight = Column(Integer)
    parsing_rules = Column(JSONB)
    status = Column(String(32))
    is_active = Column(Boolean)
    updated_at = Column(DateTime)
    is_truncating = Column(Boolean, default=False)
    max_records_count = Column(DECIMAL)

    def __eq__(self, other):
        return self.id == other.id


class IndicatorFeedRelationship(IDBase, TimestampBase):
    __tablename__ = "indicator_feed_relationships"
    indicator_id = Column(UUID, ForeignKey('indicators.id', ondelete='SET NULL'), nullable=True)
    feed_id = Column(BigInteger, ForeignKey('feeds.id', ondelete='SET NULL'), nullable=True)
    deleted_at = Column(DateTime)


class Indicator(TimestampBase):
    __tablename__ = "indicators"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    ioc_type = Column(String(32))
    value = Column(String(1024))
    context = Column(JSONB)
    is_sending_to_detections = Column(Boolean, default=True)
    is_false_positive = Column(Boolean, default=False)
    ioc_weight = Column(DECIMAL)
    tags_weight = Column(DECIMAL)
    is_archived = Column(Boolean, default=False)
    false_detected_counter = Column(Integer)
    positive_detected_counter = Column(Integer)
    total_detected_counter = Column(Integer)
    first_detected_at = Column(DateTime)
    last_detected_at = Column(DateTime)
    created_by = Column(Integer)
    updated_at = Column(DateTime)

    feeds = relationship(
        Feed,
        backref='indicators',
        secondary='indicator_feed_relationships',
        primaryjoin=(
            and_(
                IndicatorFeedRelationship.indicator_id == id,
                IndicatorFeedRelationship.deleted_at == null()
            )
        )
    )

    UniqueConstraint(value, ioc_type, name='indicators_unique_value_type')
