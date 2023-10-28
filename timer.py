import asyncio
from datetime import datetime, timedelta

def reset_request_count():
    with open("request_count.txt", "w") as file:
        file.write("0")

def reset_daily_credits():
    with open("user_requests.txt", "w") as file:
        file.write('{}')

def reset_give_requests():
    with open("give_requests.txt", "w") as file:
        file.write("0")

async def reset_all_at_midnight():
    while True:
        now = datetime.now()
        midnight = now.replace(hour=19, minute=00, second=0, microsecond=0) + timedelta(days=1)
        seconds_until_midnight = (midnight - now).seconds
        if seconds_until_midnight == 0:
            reset_request_count()
            reset_daily_credits()
            reset_give_requests()
        await asyncio.sleep(seconds_until_midnight)