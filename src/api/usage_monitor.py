import os
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIUsageMonitor:
    def __init__(self, api_name, daily_limit=500):
        """
        Initialize usage monitor for a specific API.
        
        Args:
            api_name: Name of the API to monitor
            daily_limit: Maximum number of calls allowed per day
        """
        self.api_name = api_name
        self.daily_limit = daily_limit
        self.usage_file = os.path.join("data", "usage", f"{api_name}_usage.json")
        self.today = datetime.now().strftime("%Y-%m-%d")
        self._load_usage()
        
    def _load_usage(self):
        """Load current usage data from file"""
        os.makedirs(os.path.dirname(self.usage_file), exist_ok=True)
        
        if os.path.exists(self.usage_file):
            with open(self.usage_file, 'r') as f:
                self.usage = json.load(f)
        else:
            self.usage = {self.today: 0}
            
        # Initialize today's usage if not exists
        if self.today not in self.usage:
            self.usage[self.today] = 0
    
    def _save_usage(self):
        """Save current usage data to file"""
        with open(self.usage_file, 'w') as f:
            json.dump(self.usage, f)
    
    def increment(self, count=1):
        """
        Increment usage counter.
        
        Args:
            count: Number of API calls to add to the counter
        """
        self._load_usage()  # Ensure we have the latest data
        self.usage[self.today] += count
        self._save_usage()
        
        # Log warning if approaching limit
        if self.usage[self.today] > self.daily_limit * 0.8:
            logger.warning(
                f"{self.api_name} usage at {self.usage[self.today]}/{self.daily_limit} "
                f"({self.usage[self.today]/self.daily_limit*100:.1f}%) for today"
            )
    
    def can_make_request(self, count=1):
        """
        Check if a request can be made within limits.
        
        Args:
            count: Number of API calls to check for
            
        Returns:
            Boolean indicating if the request is within limits
        """
        self._load_usage()
        return (self.usage[self.today] + count) <= self.daily_limit