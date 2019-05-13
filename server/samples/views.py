from django.shortcuts import render
from samples.sample_pb2 import Sample, Activity, Location
from google.protobuf.any_pb2 import Any

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import BaseParser

from samples.models import Activity as Act
from samples.models import Location as Loc

from django.contrib.gis.geos import Point

class ProtobufParser(BaseParser):
    """Accept Content-type: application/x-protobuf to parse Protobuf stream"""

    media_type = 'application/x-protobuf'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()

def pb_to_model(sample):
    """pb_to_model return Activity or Location models"""

    any_data = Any()
    any_data.CopyFrom(sample.data)

    if any_data.Is(Activity.DESCRIPTOR):
        activity = Activity()
        any_data.Unpack(activity)
        
        a = Act(
            activity_id = sample.id,
            unknown = activity.unknown,
            stationary = activity.stationary,
            walking = activity.walking,
            running = activity.running,
            created_at = sample.timestamp.ToJsonString()
        )        
        return a

    elif any_data.Is(Location.DESCRIPTOR):
        location = Location()
        any_data.Unpack(location)

        loc = Loc(
            location_id = sample.id,
            location = Point(location.latitude, location.longitude),
            created_at = sample.timestamp.ToJsonString()
        )
        return loc
    else:
        return None

# @csrf_exempt
class SampleList(APIView):

    # mimetype = "application/x-protobuf"
    parser_classes = (ProtobufParser,)

    def post(self, request, format=None):
        
        # Parse protobuf from byte string
        try:
            sample = Sample.FromString(request.data)
        except Exception as e:
            return Response("error parsing sample: {}".format(str(e)), status=status.HTTP_400_BAD_REQUEST)
        
        model = pb_to_model(sample)
        if model is None:
            return Response("error parsing sample data", status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: error handle here
        model.save()
        
        # Supposed to return save amount of data.
        # Since the current implement does not support bulk create
        # Simply return 1 for each request here
        return Response("1 sample processed", status=status.HTTP_201_CREATED)