'''
################################## client.py #############################
# Assignment gRPC RocksDB Client
################################## client.py #############################
'''
import grpc
import datastore_pb2
import argparse

import time
import random

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

    def hw2_get(self, req):
        return self.stub.get(datastore_pb2.Request(data=req))


def generateRequests():

    greet1 = ["hello", datastore_pb2.Request(data='hello')]
    greet2 = ["aloha", datastore_pb2.Request(data='aloha')]
    greet3 = ["bonjour", datastore_pb2.Request(data='bonjour')]
    greet4 = ["konichiwa", datastore_pb2.Request(data='konichiwa')]
    greet5 = ["nihao", datastore_pb2.Request(data='nihao')]

    reqs = [greet1, greet2, greet3, greet4, greet5]

    for req in reqs:
        print("\n## PUT Request: value = " + req[0])
        yield req[1]
        time.sleep(random.uniform(2, 4))


def main():
    print("main")
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="display a square of a given number")
    args = parser.parse_args()
    print("Client is connecting to Server at {}:{}...".format(args.host, PORT))
    client = DatastoreClient(host=args.host)

    # STREAM CODE
    res = client.hw2_put(generateRequests())
    for re in res:
        key = re.data
        print("## PUT Response: key = " + key)
        print("## GET Request: key = " + key)
        value = client.get(key)
        print("## GET Response: value = " + value.data)


if __name__ == "__main__":
    main()

