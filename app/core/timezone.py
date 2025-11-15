"""Timezone utilities for Philippines Time (GMT+8)"""
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

# Philippines timezone (GMT+8)
PHILIPPINES_TZ = ZoneInfo("Asia/Manila")

def now_philippines() -> datetime:
	"""Get current datetime in Philippines timezone (GMT+8)"""
	return datetime.now(PHILIPPINES_TZ)

def to_philippines(dt: datetime) -> datetime:
	"""Convert datetime to Philippines timezone"""
	if dt.tzinfo is None:
		# Assume naive datetime is already in Philippines time
		return dt.replace(tzinfo=PHILIPPINES_TZ)
	return dt.astimezone(PHILIPPINES_TZ)

def make_aware(dt: datetime) -> datetime:
	"""Make naive datetime timezone-aware (Philippines time)"""
	if dt.tzinfo is not None:
		return dt
	return dt.replace(tzinfo=PHILIPPINES_TZ)
