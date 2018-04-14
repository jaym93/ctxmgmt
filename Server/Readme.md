# Instructions

## `POST` Event to be used by Rasberry Pis

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

- `what` must be lowercased

- `when` MUST have similar sub-json with time formatted exactly like `3/19/2018 12:11:04 PM`

- `sno` MUST be a unique integer

- `where` must have sub json with attribute `location` with complete localized information.

- `meta` is designed to handle any random sub-JSON but the formatting goes in style "`what` has `attribute value` `attribute` and " so make sure to format the input accordingly.



## `POST` WebHook Fullfilment used by DialogFlow (for reference)
```
URL: https://ao9kkk5kze.execute-api.us-east-1.amazonaws.com/testing/fulfillment
TYPE: POST
RESPONSE: {
  "speech": "I found the tripod at 2nd floor of Aware Home. Let me know if you need more informatiion.",
  "displayText": "I found the tripod at 2nd floor of Aware Home. Let me know if you need more informatiion.",
  "data": {},
  "source": "AWS",
  "contextOut": [
    {
      "device-name": "tripod"
    }
  ]
}
```

