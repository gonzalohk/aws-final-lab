import json
import boto3
import os

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    # Detectamos el método: GET o POST
    method = event.get('httpMethod')
    params = event.get('queryStringParameters') or {}
    file_name = params.get('file')

    if not file_name:
        return {
            "statusCode": 400, 
            "body": json.dumps({"error": "Debes especificar el nombre del archivo en el query param '?file='"})}

    try:
        if method == 'GET':
            # Generar URL para DESCARGAR (GET_OBJECT)
            url = s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': f"incoming/{file_name}"},
                ExpiresIn=3600
            )
            action = "descarga"
            
        elif method == 'POST':
            # Generar URL para SUBIR (PUT_OBJECT)
            url = s3.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': BUCKET_NAME, 
                    'Key': f"incoming/{file_name}",
                    'ContentType': 'image/jpeg'
                },
                ExpiresIn=300
            )
            action = "subida"

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "url": url,
                "method_to_use": "GET" if method == 'GET' else "PUT",
                "action": action,
                "file": file_name
            })
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}