# Instructions

## POST Event

Warning: Handle with caution! This is directly sent to dynamoDB matching keys with table rows. DO NOT DEVIATE

```
URL: https://ao9kkk5kze.execute-api.us-east-1.amazonaws.com/testing/
TYPE: POST
BODY:
{
  "meta": {
    "battery": "20%"
  },
  "sno": "20",
  "what": "Samsung TV Remote",
  "when": "2018-03-18 10:45:13",
  "where": {
    "location": "1st floor",
    "streetAddress": "479 10th Street NW"
  },
  "who": "Adam"
}
```

All keys must be String except, `meta` and `where` which are a sub-map. `meta` is designed to handle any random sub-JSON but `where` MUST have similar sub-json
