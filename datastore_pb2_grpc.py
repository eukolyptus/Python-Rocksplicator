# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import datastore_pb2 as datastore__pb2


class DatastoreStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.put = channel.unary_unary(
        '/Datastore/put',
        request_serializer=datastore__pb2.Request.SerializeToString,
        response_deserializer=datastore__pb2.Response.FromString,
        )
    self.get = channel.unary_unary(
        '/Datastore/get',
        request_serializer=datastore__pb2.Request.SerializeToString,
        response_deserializer=datastore__pb2.Response.FromString,
        )
    self.get2 = channel.unary_unary(
        '/Datastore/get2',
        request_serializer=datastore__pb2.Request2.SerializeToString,
        response_deserializer=datastore__pb2.Response2.FromString,
        )
    self.hw2_put = channel.stream_stream(
        '/Datastore/hw2_put',
        request_serializer=datastore__pb2.Request.SerializeToString,
        response_deserializer=datastore__pb2.Response.FromString,
        )
    self.connector = channel.unary_stream(
        '/Datastore/connector',
        request_serializer=datastore__pb2.ReplicationRequest.SerializeToString,
        response_deserializer=datastore__pb2.ReplicationStream.FromString,
        )


class DatastoreServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def put(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def get2(self, request, context):
    """Put request to accomodate for replication 
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def hw2_put(self, request_iterator, context):
    """Automatically puts 'put' requests into master db 
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def connector(self, request, context):
    """Connects the slave server with master server for replication 
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_DatastoreServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'put': grpc.unary_unary_rpc_method_handler(
          servicer.put,
          request_deserializer=datastore__pb2.Request.FromString,
          response_serializer=datastore__pb2.Response.SerializeToString,
      ),
      'get': grpc.unary_unary_rpc_method_handler(
          servicer.get,
          request_deserializer=datastore__pb2.Request.FromString,
          response_serializer=datastore__pb2.Response.SerializeToString,
      ),
      'get2': grpc.unary_unary_rpc_method_handler(
          servicer.get2,
          request_deserializer=datastore__pb2.Request2.FromString,
          response_serializer=datastore__pb2.Response2.SerializeToString,
      ),
      'hw2_put': grpc.stream_stream_rpc_method_handler(
          servicer.hw2_put,
          request_deserializer=datastore__pb2.Request.FromString,
          response_serializer=datastore__pb2.Response.SerializeToString,
      ),
      'connector': grpc.unary_stream_rpc_method_handler(
          servicer.connector,
          request_deserializer=datastore__pb2.ReplicationRequest.FromString,
          response_serializer=datastore__pb2.ReplicationStream.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Datastore', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
