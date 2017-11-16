# CMPE273Assignment2
In this assignment 2, you will be implementing a RocksDB replication in Python using the design from this C++ replicator (https://medium.com/@Pinterest_Engineering/open-sourcing-rocksplicator-a-real-time-rocksdb-data-replicator-558cd3847a9d). 

You can use Lab 1 as a based line.

Differences form the replicator are:

 1. You will be using GRPC Python server instead of Thrift server.
 2. You will be exploring more into GRPC sync, async, and streaming.
 3. You can ignore all cluster management features from the replicator.
