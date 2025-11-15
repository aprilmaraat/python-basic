"""Timezone utilities for Philippines Time (GMT+8)"""
from datetime import datetime, timedelta

def now_philippines() -> datetime:
	"""Get current naive datetime in Philippines local time (GMT+8)
	
	Returns naive datetime without timezone info, representing local Philippines time.
	This avoids timezone conversion issues and uses local time directly.
	"""
	# Get UTC time and add 8 hours for Philippines Time
	utc_now = datetime.utcnow()
	philippines_now = utc_now + timedelta(hours=8)
	return philippines_now
