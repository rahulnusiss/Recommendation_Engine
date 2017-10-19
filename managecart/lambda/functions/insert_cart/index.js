var AWS = require("aws-sdk");

AWS.config.update({
  region: "us-east-1",
  endpoint: "https://dynamodb.us-east-1.amazonaws.com"
});

var docClient = new AWS.DynamoDB.DocumentClient();

var table = "UserCart";

var usercart = {
  "id": 426,
  "Customer": {
    "CustomerId": "124336",
    "Retailers": {
      "RetailerLambda": [
        "LHBeer",
        "LHCoke"
      ],
      "RetailerLambda23": [
        "LHWax",
        "LHCandle"
      ]
    }
  }
}

var params = {
    TableName:table,
    Item:{
        "id":  usercart.id,
        "Customer": usercart.Customer   
        }
    };

exports.handle = function(e, ctx, cb) {
    console.log("Adding a new item...");
    docClient.put(params, function(err, data) {
    if (err) {
        console.error("Unable to add item. Error JSON:", JSON.stringify(err, null, 2));
    } else {
        console.log("Added item:", JSON.stringify(data, null, 2));
    }
    console.log('processing event: %j', e)
    cb(null, {"statusCode": 200, "body": JSON.stringify(err, null, 2)})
    });
}
