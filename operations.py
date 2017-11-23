'''
################################## client.py #############################
# Assignment gRPC RocksDB Client
################################## client.py #############################
'''
import grpc
import sys

import datastore_pb2
import argparse

import time
import random

import rocksdb
from functools import wraps


PORT = 3000


class DatastoreClient():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def put(self, value):
        return self.stub.put(datastore_pb2.Request(data=value))

    def get(self, key):
        return self.stub.get(datastore_pb2.Request(data=key))

    def hw2_put(self, req):
        return self.stub.hw2_put(req)


def generateRequests():
    greet1 = ["hello", datastore_pb2.Request(data='hello')]
    greet2 = ["aloha", datastore_pb2.Request(data='aloha')]
    greet3 = ["bonjour", datastore_pb2.Request(data='bonjour')]
    greet4 = ["konichiwa", datastore_pb2.Request(data='konichiwa')]
    greet5 = ["nihao", datastore_pb2.Request(data='nihao')]

    reqs = [greet1, greet2, greet3, greet4, greet5]

    for req in reqs:
        print("\n## PUT Request: value = \t" + req[0])
        yield req[1]
        time.sleep(random.uniform(2, 4))


def main():
    print("OPERATIONS RUNNING")
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number") #sys.argv[1]
    parser.add_argument("command", help="either 'put' or 'get'")

    """
    INITIAL CHECKS
    """
    command = sys.argv[2]
    if command == "put":
        print("PUT COMMAND INITIATED")
    elif command == "get":
        print("GET COMMAND INITIATED")
        parser.add_argument("slaveID", help="the slave db to get data from")
        parser.add_argument("key", help="the key to get the value from")
    else:
        print("ERROR")
        exit()

    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    #client = DatastoreClient(host=args.host)

    """
    OPERATIONS
    """
    if command == "put":
        # STREAM CODE
        client = DatastoreClient(host=args.host)

        res = client.hw2_put(generateRequests())
        for re in res:
            key = re.data
            print("## PUT Response: key = \t\t" + key)
            print("## GET Request: key = \t\t" + key)
            value = client.get(key)
            print("## GET Response: value = \t" + value.data)
    elif command == "get":
        parser.add_argument("slaveID", help="the slave db to get data from")
        parser.add_argument("key", help="the key to get the value from")

        slaveId = sys.argv[3]
        key = sys.argv[4]

        #NEED TO FIX THIS
        #slave = rocksdb.DB(slaveId + ".db", rocksdb.Options(create_if_missing=True))
        #value = slave.get(key)

        client = DatastoreClient(host=args.host)
        value = client.get(key)

        print("\n## SERVER NAME = \t" + slaveId + ".db")
        print("## Key = \t\t" + str(key))
        print("## Value = \t\t" + value.data)

    else:
        print("ERROR")
        exit()


if __name__ == "__main__":
    main()
