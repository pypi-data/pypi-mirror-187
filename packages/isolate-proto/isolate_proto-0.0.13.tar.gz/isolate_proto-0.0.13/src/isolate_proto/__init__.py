from __future__ import annotations

import datetime

from google.protobuf.json_format import MessageToDict as struct_to_dict
from google.protobuf.struct_pb2 import Struct
from google.protobuf.timestamp_pb2 import Timestamp

# Imitates how includes in our protobuf files are handled.
from isolate.connections.grpc.definitions import *
from isolate.server.definitions import *
from isolate_proto.controller_pb2 import *
from isolate_proto.controller_pb2_grpc import (
    IsolateControllerServicer,
    IsolateControllerStub,
)
from isolate_proto.controller_pb2_grpc import (
    add_IsolateControllerServicer_to_server as register_controller,
)


def timestamp_from_datetime(datetime: datetime.datetime):
    ts = Timestamp()
    ts.FromDatetime(datetime)
    return ts
