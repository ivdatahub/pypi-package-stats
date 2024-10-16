curl -X POST "https://api.datadoghq.com/api/v2/series" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: ${DD_API_KEY}" \
-d @- << EOF
{
  "series": [
    {
      "metric": "pypi.deployment",
      "type": 0,
      "points": [
        {
          "timestamp": $(date +%s),
          "value": 1
        }
      ]
    }
  ]
}
EOF
