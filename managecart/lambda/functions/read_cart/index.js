var AWS = require("aws-sdk");

AWS.config.update({
  region: "ap-southeast-1",
  endpoint: "https://dynamodb.ap-southeast-1.amazonaws.com"
});

var docClient = new AWS.DynamoDB.DocumentClient()

var table = "UserCart";

var id = 430;

var params = {
    TableName: table,
    Key:{
        "id": id        
    }
};

//exports.handle = function(e, ctx, cb) {
    docClient.get(params, function(err, data) {
        if (err) {
            console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
        } else {
            console.log("GetItem succeeded:", JSON.stringify(data, null, 2));
        }
        //console.log('processing event: %j', e)
        //cb(null, {"statusCode": 200, "body": JSON.stringify(data, null, 2)})
    });
//}
