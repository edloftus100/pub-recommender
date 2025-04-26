import sys
import os
sys.path.append(os.path.abspath('..'))

from src.api.usage_monitor import APIUsageMonitor

def test_usage_monitor():
    # Create a monitor
    monitor = APIUsageMonitor("test_api", daily_limit=10)
    
    # Check if we can make requests
    print(f"Can make request? {monitor.can_make_request()}")
    
    # Increment usage
    print("Incrementing usage by 5")
    monitor.increment(5)
    
    # Check again
    print(f"Can make request (5 more)? {monitor.can_make_request(5)}")
    print(f"Can make request (6 more)? {monitor.can_make_request(6)}")
    
    # Increment again
    print("Incrementing usage by 2")
    monitor.increment(2)
    
    # Check final status
    print(f"Final status - Can make request (3 more)? {monitor.can_make_request(3)}")
    print(f"Final status - Can make request (4 more)? {monitor.can_make_request(4)}")

if __name__ == "__main__":
    test_usage_monitor()