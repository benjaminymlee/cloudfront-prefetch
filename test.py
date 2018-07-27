from botocore.vendored import requests
from botocore.exceptions import ClientError
import boto3

headers = {'host': 'd138jiqnlw2og4.cloudfront.net'}
response = requests.head('http://d138jiqnlw2og4.ATL50.cloudfront.net/test.txt', headers=headers)
print(response)