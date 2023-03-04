import json
import os

import boto3

ACM_ARN = os.getenv('ACM_ARN')


def lambda_handler(event, context):
    result = os.popen('certbot certonly -d wsskorea.cloud -d *.wsskorea.cloud --dns-route53 --logs-dir /tmp '
                      '--config-dir /tmp --work-dir /tmp -m wsskorea.cloud@gmail.com --agree-tos --non-interactive '
                      '--server https://acme-v02.api.letsencrypt.org/directory').read()
    print(result)

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/tmp/live/wsskorea.cloud/fullchain.pem', 'wsskorea-tls-certification', 'fullchain.pem')
    s3.meta.client.upload_file('/tmp/live/wsskorea.cloud/privkey.pem', 'wsskorea-tls-certification', 'privkey.pem')

    # fullchain_pem = ''
    # privkey_pem = ''

    with open('/tmp/live/wsskorea.cloud/fullchain.pem', 'r') as f:
        fullchain_pem = f.read()
        fullchain_pem = fullchain_pem.encode('UTF-8')

    with open('/tmp/live/wsskorea.cloud/privkey.pem', 'r') as f:
        privkey_pem = f.read()
        privkey_pem = privkey_pem.encode('UTF-8')

    acm = boto3.client('acm')
    acm.import_certificate(
        CertificateArn=ACM_ARN,
        Certificate=fullchain_pem,
        PrivateKey=privkey_pem,
        CertificateChain=fullchain_pem
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'OK'})
    }


# Use only development environment
if __name__ == '__main__':
    result = lambda_handler(None, None)
    print(result)
