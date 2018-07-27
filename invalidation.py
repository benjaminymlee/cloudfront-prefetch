from botocore.exceptions import ClientError
import boto3
import time
import datetime
import random

client = boto3.client('cloudfront')

##Create CallerReference
HASH = random.getrandbits(16)
NOW = datetime.datetime.now()
TIMEHASH = time.mktime(NOW.timetuple())
CALLERREFERENCE = str(HASH+TIMEHASH)

def check_invalidation_path(distributionId, bucketName, key):
    print('[Started check_invalidation_path]')
    try:
        get_distribution_response = client.get_distribution(
            Id = distributionId
        )
        for i in get_distribution_response.get('Distribution').get('DistributionConfig').get('Origins').get('Items'):
            if(bucketName == i.get('DomainName').split('.s3')[0]):
                if(i.get('OriginPath') != ''):
                    print(key.split(i.get('originPath'), 1)[1])
                    print('[Completed check_invalidation_path]')
                    return key.split(i.get('originPath'), 1)[1]
                else:
                    print(key)
                    print('[Completed check_invalidation_path]')
                    return key
    except ClientError as e:
        print('Failed check_invInvalidation_path: {}' . format(e))

def create_invalidation(distributionId, invalidationPath):
    print('[Started create_invalidation]')
    try:
        create_invalidation_response = client.create_invalidation(
            DistributionId = distributionId,
            InvalidationBatch = {
                'Paths': {
                    'Quantity': 1,
                    'Items': [
                        invalidationPath,
                    ]
                },
                'CallerReference': CALLERREFERENCE
            }
        )
        print(create_invalidation_response)
        print('[Completed create_invalidation]')
        return create_invalidation_response
    except ClientError as e:
        print('Failed create_invalidation: {}' . format(e))

def check_invalidation(distributionId, invalidationId):
    timewait = 0
    status = None
    print('[Started check_invalidation]')
    while 1:
        print('Inprogress Invalidation... {}'.format(timewait))
        try:
            get_invalidation_response = client.get_invalidation(
                DistributionId = distributionId,
                Id = invalidationId
            )
            status = get_invalidation_response.get('Invalidation').get('Status')
            if(status == 'Completed'):
                print(get_invalidation_response)
                print('[Completed Check_Invalidation]')
                return get_invalidation_response
            else:
                timewait += 5
                time.sleep(5)
        except ClientError as e:
            print('Failed check_Invalidation: {}' .format(e))