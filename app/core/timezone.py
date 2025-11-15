"""Timezone utilities for Philippines Time (GMT+8)"""
from datetime import datetime

def now_philippines() -> datetime:
	"""Get current local datetime (Philippines Time)
	
	Returns naive datetime representing the local system time.
	Assumes system is configured to Philippines timezone.
	"""
	return datetime.now()
