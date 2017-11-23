'''
################################## client.py #############################
# Assignment gRPC RocksDB Client
################################## client.py #############################
'''
import grpc
import datastore_pb2
import datastore_pb2_grpc
import argparse
import sys

import time
import random

import rocksdb
from functools import wraps


PORT = 3000

slaveId = sys.argv[2] # TODO - set slavedb name here

class DatastoreClient():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)
        self.slave = rocksdb.DB(slaveId + ".db", rocksdb.Options(create_if_missing=True))

        # self.slave1.put(b'a', b'v1')
        print("CREATED: \t" + slaveId + ".db")

    def connect(self):
        print("CONNECTED: \tREADY FOR REPLICATION")
        res = self.stub.connector(datastore_pb2.Request())
        for re in res:
            key = re.key
            value = re.value
            self.slave.put(key, value)
            print("\n## SERVER NAME = " + slaveId + ".db")
            print("## Key = " + key)
            print("## Value = " + value)


def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("host", help="display a square of a given number")  # sys.argv[1]
        parser.add_argument("slaveId", help="the slave db")
        args = parser.parse_args()

        print("Slave is connecting to Server at {}:{}...".format(args.host, PORT))

        client = DatastoreClient(host=args.host)
        client.connect()

if __name__ == "__main__":
        main()
