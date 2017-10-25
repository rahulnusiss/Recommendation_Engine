var AWS = require("aws-sdk");

AWS.config.update({
  region: "ap-southeast-1",
  endpoint: "https://dynamodb.ap-southeast-1.amazonaws.com"
});

// Will not work on lambda test but will work with APIGateway due ot JSON.parse
exports.handle = function(e, ctx, cb) {
var docClient = new AWS.DynamoDB.DocumentClient()

var table = "UserCart";

var body = JSON.parse(e.body);
// Update the item, unconditionally,

var params = {
        TableName:table,
        Key:{
            "id": body.id      
        },
        UpdateExpression: "set Customer.Retailers = :r",
        ExpressionAttributeValues:{
            ":r": body.data
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

