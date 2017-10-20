var AWS = require("aws-sdk");

AWS.config.update({
  region: "us-east-1",
  endpoint: "https://dynamodb.us-east-1.amazonaws.com"
});

exports.handle = function(e, ctx, cb) {
var docClient = new AWS.DynamoDB.DocumentClient()

var table = "UserCart";

var id = 326;
// Update the item, unconditionally,

var params = {
        TableName:table,
        Key:{
            "id": id        
        },
        UpdateExpression: "set Customer.Retailers = :r",
        ExpressionAttributeValues:{
            ":r": e.data
        },
        ReturnValues:"UPDATED_NEW"
    };
    console.log("Updating the item...");
    docClient.update(params, function(err, data) {
        if (err) {
            console.error("Unable to update item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("UpdateItem succeeded:", JSON.stringify(data, null, 2));
        }
         console.log('processing event: %j', e)
         cb(null, {"statusCode": 200, "body": JSON.stringify(data, null, 2)})
    });
}

