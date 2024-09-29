import json
import boto3
from boto3.dynamodb.conditions import Key

# DynamoDBへの接続を初期化
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("shikakupass-users")

print("Loading function")


def lambda_handler(event, context):
    operation = event["queryStringParameters"]["operation"]

    if operation == "GET":
        # API Gatewayからemailパラメータを取得
        email = event["queryStringParameters"]["email"]

        # DynamoDBからemailに一致するレコードを検索
        response = table.query(KeyConditionExpression=Key("email").eq(email))

        # 検索結果を返す
        items = response["Items"]
        if items:
            return {"statusCode": 200, "body": json.dumps(items)}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found. v2."}),
            }
    else:
        raise ValueError('Unrecognized operation "{}"'.format(operation))
