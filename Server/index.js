console.log('Loading event');
var doc = require('dynamodb-doc');
var dynamodb = new doc.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    var tableName = "use-logger";
    var item = {
        "meta": event.meta,
        "sno":  event.sno,
        "what": event.what,
        "when": event.when,
        "where": {
            "location": event.location,
            "streetAddress": event.streetAddress
        },
        "who": event.who
    };
    console.log("Item:\n", item);

    dynamodb.putItem({
            "TableName": tableName,
            "Item": item
        }, function(err, data) {
            if (err) {
                context.fail('ERROR: Dynamo failed: ' + err);
            } else {
                console.log('Dynamo Success: ' + JSON.stringify(data, null, '  '));
                context.succeed('SUCCESS');
            }
        });
}
