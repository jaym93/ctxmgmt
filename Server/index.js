console.log('Loading event');
var doc = require('dynamodb-doc');
var dynamodb = new doc.DynamoDB();

exports.handler = function(event, context) {
    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));
    var tableName = "use-logger";
    var item = {};
    var count = 0;
    JSON.parse(JSON.stringify(event), (key, value) => {
        count += 1;
        if (count < 7) {
            item[key] = value
        }
        console.log(key); // log the current property name, the last is "".
        console.log(value);
        console.log("done");
        return value;     // return the unchanged property value.
    });

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
