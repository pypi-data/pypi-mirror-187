# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from aos_prov.communication.unit.v0.generated import api_iamanager_iamanager_pb2 as api__iamanager__iamanager__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class IAManagerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetCertTypes = channel.unary_unary(
                '/iamanager.IAManager/GetCertTypes',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.GetCertTypesRsp.FromString,
                )
        self.FinishProvisioning = channel.unary_unary(
                '/iamanager.IAManager/FinishProvisioning',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.Clear = channel.unary_unary(
                '/iamanager.IAManager/Clear',
                request_serializer=api__iamanager__iamanager__pb2.ClearReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.SetOwner = channel.unary_unary(
                '/iamanager.IAManager/SetOwner',
                request_serializer=api__iamanager__iamanager__pb2.SetOwnerReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.CreateKey = channel.unary_unary(
                '/iamanager.IAManager/CreateKey',
                request_serializer=api__iamanager__iamanager__pb2.CreateKeyReq.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.CreateKeyRsp.FromString,
                )
        self.ApplyCert = channel.unary_unary(
                '/iamanager.IAManager/ApplyCert',
                request_serializer=api__iamanager__iamanager__pb2.ApplyCertReq.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.ApplyCertRsp.FromString,
                )
        self.GetCert = channel.unary_unary(
                '/iamanager.IAManager/GetCert',
                request_serializer=api__iamanager__iamanager__pb2.GetCertReq.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.GetCertRsp.FromString,
                )
        self.GetSystemInfo = channel.unary_unary(
                '/iamanager.IAManager/GetSystemInfo',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.GetSystemInfoRsp.FromString,
                )
        self.SetUsers = channel.unary_unary(
                '/iamanager.IAManager/SetUsers',
                request_serializer=api__iamanager__iamanager__pb2.SetUsersReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.GetUsers = channel.unary_unary(
                '/iamanager.IAManager/GetUsers',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.GetUsersRsp.FromString,
                )
        self.SubscribeUsersChanged = channel.unary_stream(
                '/iamanager.IAManager/SubscribeUsersChanged',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=api__iamanager__iamanager__pb2.UsersChangedNtf.FromString,
                )
        self.EncryptDisk = channel.unary_unary(
                '/iamanager.IAManager/EncryptDisk',
                request_serializer=api__iamanager__iamanager__pb2.EncryptDiskReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class IAManagerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetCertTypes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FinishProvisioning(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Clear(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetOwner(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApplyCert(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCert(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSystemInfo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUsers(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeUsersChanged(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EncryptDisk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IAManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetCertTypes': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCertTypes,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.GetCertTypesRsp.SerializeToString,
            ),
            'FinishProvisioning': grpc.unary_unary_rpc_method_handler(
                    servicer.FinishProvisioning,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'Clear': grpc.unary_unary_rpc_method_handler(
                    servicer.Clear,
                    request_deserializer=api__iamanager__iamanager__pb2.ClearReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'SetOwner': grpc.unary_unary_rpc_method_handler(
                    servicer.SetOwner,
                    request_deserializer=api__iamanager__iamanager__pb2.SetOwnerReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'CreateKey': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateKey,
                    request_deserializer=api__iamanager__iamanager__pb2.CreateKeyReq.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.CreateKeyRsp.SerializeToString,
            ),
            'ApplyCert': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplyCert,
                    request_deserializer=api__iamanager__iamanager__pb2.ApplyCertReq.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.ApplyCertRsp.SerializeToString,
            ),
            'GetCert': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCert,
                    request_deserializer=api__iamanager__iamanager__pb2.GetCertReq.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.GetCertRsp.SerializeToString,
            ),
            'GetSystemInfo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSystemInfo,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.GetSystemInfoRsp.SerializeToString,
            ),
            'SetUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.SetUsers,
                    request_deserializer=api__iamanager__iamanager__pb2.SetUsersReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'GetUsers': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUsers,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.GetUsersRsp.SerializeToString,
            ),
            'SubscribeUsersChanged': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeUsersChanged,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=api__iamanager__iamanager__pb2.UsersChangedNtf.SerializeToString,
            ),
            'EncryptDisk': grpc.unary_unary_rpc_method_handler(
                    servicer.EncryptDisk,
                    request_deserializer=api__iamanager__iamanager__pb2.EncryptDiskReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'iamanager.IAManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IAManager(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetCertTypes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/GetCertTypes',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            api__iamanager__iamanager__pb2.GetCertTypesRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FinishProvisioning(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/FinishProvisioning',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Clear(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/Clear',
            api__iamanager__iamanager__pb2.ClearReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetOwner(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/SetOwner',
            api__iamanager__iamanager__pb2.SetOwnerReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/CreateKey',
            api__iamanager__iamanager__pb2.CreateKeyReq.SerializeToString,
            api__iamanager__iamanager__pb2.CreateKeyRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ApplyCert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/ApplyCert',
            api__iamanager__iamanager__pb2.ApplyCertReq.SerializeToString,
            api__iamanager__iamanager__pb2.ApplyCertRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetCert(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/GetCert',
            api__iamanager__iamanager__pb2.GetCertReq.SerializeToString,
            api__iamanager__iamanager__pb2.GetCertRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSystemInfo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/GetSystemInfo',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            api__iamanager__iamanager__pb2.GetSystemInfoRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/SetUsers',
            api__iamanager__iamanager__pb2.SetUsersReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUsers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/GetUsers',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            api__iamanager__iamanager__pb2.GetUsersRsp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeUsersChanged(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/iamanager.IAManager/SubscribeUsersChanged',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            api__iamanager__iamanager__pb2.UsersChangedNtf.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def EncryptDisk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/iamanager.IAManager/EncryptDisk',
            api__iamanager__iamanager__pb2.EncryptDiskReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
