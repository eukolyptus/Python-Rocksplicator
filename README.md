# CMPE273Assignment2
In this assignment 2, you will be implementing a RocksDB replication in Python using the design from this C++ replicator (https://medium.com/@Pinterest_Engineering/open-sourcing-rocksplicator-a-real-time-rocksdb-data-replicator-558cd3847a9d). 

You can use Lab 1 as a based line.

Differences form the replicator are:

 1. You will be using GRPC Python server instead of Thrift server.
 2. You will be exploring more into GRPC sync, async, and streaming.
 3. You can ignore all cluster management features from the replicator.


Build Docker Image with RocksDB and gRPC using image provided from class.
Source: https://github.com/sithu/cmpe273-fall17/tree/master/docker

    docker build -t ubuntu-python3.6-rocksdb-grpc:1.0 .

Create a Docker network so that each container can connect to the host under the fixed IP 192.168.0.1.

    docker network create -d bridge --subnet 192.168.0.0/24 --gateway 192.168.0.1 dockernet

Generate the stub for client and server

    docker run -it --rm --name grpc-tools -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto

Start the masterServer.py file

    docker run -p 3000:3000 -it --rm --name lab1-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 masterServer.py

Start up the slave databases with the slaveServer.py file. This will be done on 3 separate terminal windows:


    #slave1
    docker run -it --rm --name hw2-client1 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 slaveServer.py 192.168.0.1 slave1

    #slave2
    docker run -it --rm --name hw2-client2 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 slaveServer.py 192.168.0.1 slave2

    #slave3
    docker run -it --rm --name hw2-client3 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 slaveServer.py 192.168.0.1 slave3

Run the operations.py file, this will load the master database

    docker run -it --rm --name hw2-ops -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 operations.py 192.168.0.1 put

Check if the slave database received the replication using the operation.py file.
Example: docker run -it --rm --name hw2-ops -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 operations.py 192.168.0.1 get [database name] [key]


    docker run -it --rm --name hw2-ops -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 python3.6 operations.py 192.168.0.1 get slave1 9bce8241a4b14f92a2566da7e9e4255a


It will yield the following result:

> SERVER NAME =        slave1.db
> Key =                e6d9e0e679aa48569780a4dc195266f4
> Value =              nihao

