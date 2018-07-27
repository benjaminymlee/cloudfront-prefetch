from botocore.vendored import requests
from botocore.exceptions import *
import boto3
client = boto3.client('cloudfront')

S3URL = '.s3.amazonaws.com'

def get_s3_object_etag(bucketName, s3Path):
    print('[Started get_s3_object]')
    try:
        response = requests.get('http://' + bucketName + S3URL + s3Path)
        print('S3 Object Etag: {}' .format(response.headers.get('Etag')))
        return response.headers.get('Etag')
    except ClientError as e:
        print('Failed get_s3_object_etag: {}'.format(e))

def get_cf_metadata(distributionId, cloudfrontPath):
    print('[Started get_cf_metadata]')
    try:
        get_distribution_response = client.get_distribution(
            Id=distributionId
        )
        cloudfrontHost = get_distribution_response.get('Distribution').get('DomainName')
    except ClientError as e:
        print('Failed get_s3_object_etag: {}'.format(e))

    cloudfrontEdgeList = []
    try:
        with open('./edge_list') as f:
            edge_list = f.readlines()
            for i in edge_list:
                url = 'http://' + cloudfrontHost.split('.')[0] + '.' + i.strip() + cloudfrontPath
                cloudfrontEdgeList.append(url)
            print(cloudfrontHost, cloudfrontEdgeList)
            print('[Completed get_cf_metadata]')
            return {'cloudfrontHost':cloudfrontHost, 'cloudfrontEdgeList':cloudfrontEdgeList}
    except FileNotFoundError as e:
        print('Failed get_cf_metadata: {}'.format(e))

def get_cf_object_etag(cloudfrontHost, cloudfrontEdge, s3_etag, conn):
    headers = {'host': cloudfrontHost}
    response = None
    cloudfrontEtag = None
    cloudfrontXcache = None
    for i in range(0, 2):
        try:
            response = requests.get(cloudfrontEdge, headers=headers)
            cloudfrontEtag = response.headers.get('Etag')
            cloudfrontXcache = response.headers.get('X-Cache')
        except requests.ConnectionError as e:
            print('Failed get_cf_object: {}, Error: {}'.format(cloudfrontEdge, e))
    if (cloudfrontEtag != s3_etag or cloudfrontEtag == None):
        print('Failed Invalidation(object: {}, s3_etag:{}, cf_etag:{}'.format(cloudfrontEdge, cloudfrontEtag, s3_etag))
    if (cloudfrontXcache == 'Hit from cloudfront' or cloudfrontXcache == 'RefreshHit from cloudfront'):
        print('Succeed Pre-fetch(object: {}, s3_etag: {}, cf_etag: {}, cf_cache: {}'.format(cloudfrontEdge, cloudfrontEtag, s3_etag, cloudfrontXcache))
    conn.close()
    return None
