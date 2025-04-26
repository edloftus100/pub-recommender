import os
import json
import hashlib
import time

class APICache:
    def __init__(self, cache_dir="data/cache", ttl=86400):  # Default TTL: 1 day
        """
        Initialize API cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            ttl: Time-to-live for cache entries in seconds (default: 1 day)
        """
        self.cache_dir = cache_dir
        self.ttl = ttl
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _get_cache_key(self, params):
        """Generate a cache key from request parameters"""
        param_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(param_str.encode()).hexdigest()
    
    def _get_cache_path(self, key):
        """Get file path for a cache key"""
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, params):
        """
        Get cached response if available and not expired.
        
        Args:
            params: Parameters that uniquely identify the API request
            
        Returns:
            Cached data if available and valid, None otherwise
        """
        key = self._get_cache_key(params)
        cache_path = self._get_cache_path(key)
        
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                
            # Check if cache is still valid
            if time.time() - cached_data["timestamp"] < self.ttl:
                return cached_data["data"]
                
        return None
    
    def set(self, params, data):
        """
        Cache API response.
        
        Args:
            params: Parameters that uniquely identify the API request
            data: Data to cache
        """
        key = self._get_cache_key(params)
        cache_path = self._get_cache_path(key)
        
        cached_data = {
            "timestamp": time.time(),
            "data": data
        }
        
        with open(cache_path, 'w') as f:
            json.dump(cached_data, f)