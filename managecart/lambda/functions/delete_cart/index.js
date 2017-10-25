var AWS = require("aws-sdk");

AWS.config.update({
  region: "ap-southeast-1",
  endpoint: "https://dynamodb.ap-southeast-1.amazonaws.com"
});

exports.handle = function(e, ctx, cb) {
    var docClient = new AWS.DynamoDB.DocumentClient();
    
    var table = "UserCart";
    
    var body = JSON.parse(e.body);
    var id = body.id ;
    
    var params = {
        TableName:table,
        Key:{
            "id":id
        }
       // ConditionExpression:"Customer.Retailers == :val",
       // ExpressionAttributeValues: {
         //   ":val": {"R1" .......... }
       // }
    };
    
    console.log("Attempting a unconditional delete...");
    docClient.delete(params, function(err, data) {
        if (err) {
            console.error("Unable to delete item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("DeleteItem succeeded:", JSON.stringify(data, null, 2));
        }
        console.log('processing event: %j', e)
        cb(null, {"statusCode": 200, "body": JSON.stringify(data, null, 2)})
    });
}
