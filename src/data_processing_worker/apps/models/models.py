from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID, BYTEA
from sqlalchemy import (
    Column, String, DateTime, Text, Boolean, UniqueConstraint,
    BigInteger, DECIMAL, text, ForeignKey, and_, null
)

from data_processing_worker.apps.models.abstract import IDBase, TimestampBase

indicators_rel = "indicators.id"


class ContextSource(IDBase, TimestampBase):
    __tablename__ = "context_sources"

    ioc_type = Column(String(32))
    source_url = Column(String(255))
    request_method = Column(String(16))
    request_headers = Column(Text)
    request_body = Column(Text)
    inbound_removable_prefix = Column(String(128), nullable=True)
    outbound_appendable_prefix = Column(String(128), nullable=True)
    created_by = Column(BigInteger)


class IndicatorContextSourceRelationship(IDBase, TimestampBase):
    __tablename__ = "indicator_context_source_relationships"

    indicator_id = Column(UUID, ForeignKey(indicators_rel), nullable=True)
    context_source_id = Column(BigInteger, ForeignKey('context_sources.id'))


class Feed(IDBase, TimestampBase):
    __tablename__ = "feeds"

    title = Column(String(128))
    provider = Column(String(128))
    description = Column(String(255))
    format = Column(String(8))
    url = Column(String(128))
    auth_type = Column(String(16))
    auth_api_token = Column(String(255))
    auth_login = Column(String(32))
    auth_pass = Column(String(32))
    certificate = Column(BYTEA)
    use_taxii = Column(Boolean, default=False)
    polling_frequency = Column(String(32))
    weight = Column(DECIMAL())
    available_fields = Column(JSONB)
    parsing_rules = Column(JSONB)
    status = Column(String(32))
    is_active = Column(Boolean, default=True)
    is_truncating = Column(Boolean, default=True)
    max_records_count = Column(DECIMAL)
    updated_at = Column(DateTime)

    def __eq__(self, other):
        return self.id == other.id


class IndicatorFeedRelationship(IDBase, TimestampBase):
    __tablename__ = "indicator_feed_relationships"
    indicator_id = Column(UUID, ForeignKey(indicators_rel), nullable=True)
    feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=True)
    deleted_at = Column(DateTime)


class Tag(IDBase, TimestampBase):
    __tablename__ = "tags"

    title = Column(String(128), unique=True)
    weight = Column(DECIMAL)
    created_by = Column(BigInteger)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    UniqueConstraint(title, name='tags_unique_title')


class Indicator(TimestampBase):
    __tablename__ = "indicators"

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    ioc_type = Column(String(32))
    value = Column(String(1024))
    context = Column(JSONB)
    is_sending_to_detections = Column(Boolean, default=True)
    is_false_positive = Column(Boolean, default=False)
    weight = Column(DECIMAL)
    feeds_weight = Column(DECIMAL)
    time_weight = Column(DECIMAL)
    tags_weight = Column(DECIMAL)
    is_archived = Column(Boolean, default=False)
    false_detected_counter = Column(BigInteger)
    positive_detected_counter = Column(BigInteger)
    total_detected_counter = Column(BigInteger)
    first_detected_at = Column(DateTime)
    last_detected_at = Column(DateTime)
    created_by = Column(BigInteger)
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

    tags = relationship(
        Tag,
        backref='indicators',
        secondary='indicator_tag_relationships',
    )

    UniqueConstraint(value, ioc_type, name='indicators_unique_value_type')


class IndicatorActivity(IDBase, TimestampBase):
    __tablename__ = "indicator_activities"

    indicator_id = Column(UUID(as_uuid=True))
    activity_type = Column(String(32))
    details = Column(JSONB)
    created_by = Column(BigInteger, nullable=True)


class IndicatorTagRalationship(IDBase, TimestampBase):
    __tablename__ = "indicator_tag_relationships"

    indicator_id = Column(UUID, ForeignKey(indicators_rel))
    tag_id = Column(BigInteger, ForeignKey('tags.id'))


class Process(IDBase):
    __tablename__ = "processes"
    parent_id = Column(BigInteger, nullable=True)
    service_name = Column(String(64))
    title = Column(String(128))
    result = Column(JSONB)
    status = Column(String(32))
    started_at = Column(DateTime)
    finished_at = Column(DateTime)


class PlatformSetting(IDBase):
    __tablename__ = "platform_settings"
    key = Column(String(128))
    value = Column(JSONB)
    updated_at = Column(DateTime)
    created_by = Column(BigInteger)
