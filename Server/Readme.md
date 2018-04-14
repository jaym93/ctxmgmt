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
  "when": "3/19/2018 12:11:04 PM",
  "where": {
    "location": "1st floor of Aware Home",
    "streetAddress": "479 10th Street NW"
  },
  "who": "Adam"
}
```

All keys must be String except, `meta` and `where` which are a sub-map. 

- `meta` is designed to handle any random sub-JSON but the formatting goes in style "`what` has `attribute value` `attribute` and " so make sure to format the input accordingly.

- `where` MUST have similar sub-json with time formatted exactly like `3/19/2018 12:11:04 PM`
