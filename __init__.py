from invalidation import *
from check_object import *
from multiprocessing import Process, Pipe

DISTRIBUTIONID='E12OX8RSSI1M70'
BUCKETNAME = 'cf-prefetch'
KEY = 'test.txt'

if __name__ == "__main__":
    start_time = time.time()

    cloudfrontPath = check_invalidation_path(DISTRIBUTIONID, BUCKETNAME, KEY)
    invalidation_response = create_invalidation(DISTRIBUTIONID, '/' + cloudfrontPath)
    invalidation_check_response = check_invalidation(DISTRIBUTIONID, invalidation_response.get('Invalidation').get('Id'))

    time.sleep(20) ##Delay for S3 data consistency

    get_s3_object_etag_response = get_s3_object_etag(BUCKETNAME, '/' + KEY)
    get_cf_metadata_response = get_cf_metadata(DISTRIBUTIONID, '/' + cloudfrontPath)

    #Multi Processing
    processes = []
    parent_connections = []

    for i in get_cf_metadata_response.get('cloudfrontEdgeList'):
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        process = Process(target=get_cf_object_etag, args=(get_cf_metadata_response.get('cloudfrontHost'), i, get_s3_object_etag_response, child_conn))
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print('Completed ---{}seconds ---'.format(time.time() - start_time))