'''
################################## server.py #############################
# Assignment2 gRPC RocksDB Server
################################## server.py #############################
'''
import time
from concurrent import futures

import grpc

import datastore_pb2
import datastore_pb2_grpc

import uuid
import rocksdb
import random



_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        print("initialization")
        # database array
        dbList = ["base1.db", "base2.db", "base3.db"]

        self.db = rocksdb.DB("base1.db", rocksdb.Options(create_if_missing=True))
        # self.db2 = rocksdb.DB("base2.db", rocksdb.Options(create_if_missing=True))
        # self.db3 = rocksdb.DB("base3.db", rocksdb.Options(create_if_missing=True))

        """
        temp = self.db.get_live_files_metadata()
        if (len(temp) != 0):
            print(temp[0]["largest_seqno"])
        else:
            print("Empty DB")

        temp = self.db2.get_live_files_metadata()
        if(len(temp) != 0):
            print(temp[0]["largest_seqno"])
        else:
            print("Empty DB")
            self.db2.put(b'a', b'v1') # Load Database

        temp = self.db3.get_live_files_metadata()
        if (len(temp) != 0):
            print(temp[0]["largest_seqno"])
        else:
            print("Empty DB")
            self.db3.put(b'a', b'v1') #Load Database

        #Backup Procedure
        backup = rocksdb.BackupEngine("base1.db/backups")
        backup.create_backup(self.db, flush_before_backup=True)

        #Restoration on sub servers
        backup.restore_latest_backup("base1.db", "base1.db")
        backup.restore_latest_backup("base2.db", "base2.db")
        backup.restore_latest_backup("base3.db", "base3.db")
        """

    def put(self, request, context):
        key = uuid.uuid4().hex.encode("utf-8")
        s = request.data.encode("utf-8")
        self.db.put(key, s)
        print("put: " + request.data)
        # TODO - save key and value into DB converting request.data string to utf-8 bytes
        # db.put(b"key", b"value")

        return datastore_pb2.Response(data=key)

    def get(self, request, context):
        print("get: " + request.data)
        value = self.db.get(request.data.encode("utf-8"))
        # TODO - retrieve the value from DB by the given key. Needs to convert request.data string to utf-8 bytes.
        # value = None

        return datastore_pb2.Response(data=value)

    def hw2_put(self, request_iterator, context):
        for req in request_iterator:
            print("stream put: " + req.data)
            key = uuid.uuid4().hex.encode("utf-8")
            value = req.data.encode("utf-8")
            self.db.put(key, value)

            yield datastore_pb2.Response(data=key)


def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)