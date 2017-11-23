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
from functools import wraps

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

dataStream = [] # holds queue for put requests


class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        print("INITIALIZATION")

        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))
        self.followers = 0 # keeps track of the number of slave dbs

    def put(self, request, context):
        key = uuid.uuid4().hex.encode("utf-8")
        s = request.data.encode("utf-8")
        self.db.put(key, s)
        print("\nput: \t\t" + request.data)

        return datastore_pb2.Response(data=key)

    def get(self, request, context):
        print("get: \t\t" + request.data)
        value = self.db.get(request.data.encode("utf-8"))

        return datastore_pb2.Response(data=value)

    def hw2_put(self, request_iterator, context):
        for req in request_iterator:
            key = uuid.uuid4().hex.encode("utf-8")
            value = req.data.encode("utf-8")
            self.db.put(key, value)

            print("\nstream put: \t" + req.data)
            # temp = self.db.get_live_files_metadata()
            # seqNo: " + str(temp[0]["largest_seqno"])
            # print("seq no: " + str(temp[0]["largest_seqno"]))

            yield datastore_pb2.Response(data=key)

    def connector(self, request, context):

        slaveId = self.followers

        self.followers = self.followers + 1 # keep track of number of slave dbs
        print("SLAVE DBS CONNECTED: " + str(self.followers))

        dataStream.append([])
        while len(dataStream[slaveId]) > 0:
            data = dataStream[slaveId].pop(0)
            yield datastore_pb2.ReplicationStream(key=data["key"], value=data["value"])


    def replication(func):
        print("REPLICATION")

        @wraps(func)
        def wrapper(*args, **kwargs):
            print("hello wrapper")
            for i in range(args[0].totalConnections):
                dataStream[i].append({"key": args[1].key, "value":args[1].value})

            return func(*args, **kwargs)

        return wrapper


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