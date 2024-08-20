from datadog import initialize, api

options = {
    "api_key": "<YOUR_API_KEY>",
    "app_key": "<YOUR_APP_KEY>",
}

initialize(**options)

title = "Something big happened!"
text = "And let me tell you all about it here!"
tags = ["version:1", "application:web"]

api.metrics.Metric.send()
