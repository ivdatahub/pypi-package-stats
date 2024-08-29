from datadog.dogstatsd import DogStatsd
from datetime import datetime
import time
import random


client = DogStatsd(host="34.138.10.108", port=8125)


df = {
    [
        {
            "user_datetime": int(datetime.now().timestamp()),
            "core-metric": "register",
            "site": "MLB",
            "bu": "mercadopago",
            "total_starts": 100,
            "total_ends": 80,
        }
    ],
    [
        {
            "user_datetime": int(datetime.now().timestamp()),
            "core-metric": "login",
            "site": "MLB",
            "bu": "mercadopago",
            "total_starts": 100,
            "total_ends": 80,
        }
    ],
}


print("Client initialized")

list = []
for i in range(10):
    ts = datetime.now()
    rnd_value = random.randint(50, 100)
    print(f"Sending metric with value: {rnd_value}", "with timestamp: ", ts)
    client.gauge_with_timestamp(
        metric="local_metric",
        timestamp=int(ts.timestamp()),
        value=rnd_value,
        tags=["env:dev", "type:gauge"],
    )
    client.count_with_timestamp(
        metric="local_metric",
        timestamp=int(ts.timestamp()),
        value=rnd_value,
        tags=["env:dev", "type:count"],
    )
    list.append(rnd_value)
    time.sleep(10)

print("sum of values: ", sum(list))
