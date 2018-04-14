console.log('Post Request Received');

var doc = require('dynamodb-doc');
var dynamodb = new doc.DynamoDB();

const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient({region: 'us-east-1'});

exports.handler = function(event, context, callback) {

    console.log("Request received:\n", JSON.stringify(event));
    console.log("Context received:\n", JSON.stringify(context));

    let what = event.result.parameters['device-name'];
    let location = event.result.parameters['location'];
    let intentType = event.result.metadata['intentName']; //search_device, know-more, meta-info
    let action = event.result.parameters['action'];

    var params = {
        TableName : "use-logger",
      //  KeyConditionExpression: "contains(what, :what)",
      //  FilterExpression:'what = :what',
        FilterExpression: "contains(what, :what)",
        ExpressionAttributeValues:{ ":what" : what.toLowerCase() }
    };

    docClient.scan(params, function(err, data) {
      if (err) {
        console.error("Unable to query. Error:", JSON.stringify(err, null, 2));
      } else {
          console.log("Query succeeded.");
          var objects = [];
          data.Items.forEach(function(item) {
            console.log(" -", item.what + " : " + item.where.location + " | " + item.who + " | " + item.when);
            objects.push(new FoundObject(item.what, item.where.location, item.who, new Date(item.when), item.meta));
          });

          if(objects.length < 1) {
              // objects is empty (Would return true in this example)
              callback(null, {"speech": "Sorry, I couldn't find any information about the device!"});
          } else {
              // objects is NOT empty
              // sort by date
              objects.sort(function(a,b) {return (a.when > b.when) ? -1 : ((b.when > a.when) ? 1 : 0);});

              var chosenValue = "Sorry I couldn't process your request.";

              if (intentType == "search_device") {
                // processed result for Search Devices Intent (What / Where)
                let response = "I found the " + objects[0].what + " at " + objects[0].location + ". Let me know if you need more information.";
                let response2 = "Oh, the " + objects[0].what + " is at " + objects[0].location + ".";
                chosenValue = Math.random() < 0.5 ? response : response2;
              } else if ( intentType == "know-more") {
                // processed result for Who / When Intent
                if (action == null) {
                    // don't know the action
                    action = "left"; // fall back to common default
                }
                let response = objects[0].who + " " + action + " the " + objects[0].what + " there " + millisecondsToStr(new Date(Date.now()-objects[0].when)) + " ago.";
                let response2 = "The " + objects[0].what + " has been there since " + millisecondsToStr(new Date(Date.now()-objects[0].when)) + ". " + objects[0].who + " " + action + " it there.";
                chosenValue = Math.random() < 0.5 ? response : response2;
              } else if ( intentType == "meta-info") {
                // processed result for how intent (i.e. any other meta info I might have)
                var info = "";
                
                for (var key in objects[0].meta) {
                  info += objects[0].meta[key] + " " + key;
                  info += " and ";
                }

                let response = "The " + objects[0].what + " has " + info + " it's being regularly tracked.";
                chosenValue = response;
              }



              callback(null, {"speech": chosenValue,
                  "displayText": chosenValue,
                  "data": {},
                  "source": "AWS",
                  "contextOut": [{"device-name": objects[0].what}],
              });
          }
      }
    });

};


function FoundObject(what, location, who, when, meta) {
            this.what = what;
            this.location = location;
            this.who = who;
            this.when = when;
            this.meta = meta;
}

function millisecondsToStr (milliseconds) {
    // TIP: to find current time in milliseconds, use:
    // var  current_time_milliseconds = new Date().getTime();

    function numberEnding (number) {
        return (number > 1) ? 's' : '';
    }

    var temp = Math.floor(milliseconds / 1000);
    var years = Math.floor(temp / 31536000);
    if (years) {
        return years + ' year' + numberEnding(years);
    }
    //TODO: Months! Maybe weeks?
    var days = Math.floor((temp %= 31536000) / 86400);
    if (days) {
        return days + ' day' + numberEnding(days);
    }
    var hours = Math.floor((temp %= 86400) / 3600);
    if (hours) {
        return hours + ' hour' + numberEnding(hours);
    }
    var minutes = Math.floor((temp %= 3600) / 60);
    if (minutes) {
        return minutes + ' minute' + numberEnding(minutes);
    }
    var seconds = temp % 60;
    if (seconds) {
        return seconds + ' second' + numberEnding(seconds);
    }
    return 'less than a second'; //'just now' //or other string you like;
}
