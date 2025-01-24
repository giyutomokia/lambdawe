import json

def lambda_handler(event, context):
    # Get the numbers from the event (the input provided to the Lambda function)
    num1 = event.get("num1", 0)
    num2 = event.get("num2", 0)

    # Calculate the sum of the two numbers
    result = num1 + num2

    # Return the result as a JSON object
    return {
        'statusCode': 200,
        'body': json.dumps({
            'result': result
        })
    }
