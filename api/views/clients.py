from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from api import serializers
from client import models


class ClientAccountViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """ Client model view set.

    EndPoints:

        * GET .../api/client -> client list,
        * GET .../api/client/<uid64>/ -> detail client,
        * POST .../api/client/<uid64>/cash/ -> send cash
        from client with id = uid64 to clients from
        "clients" list.

    """
    queryset = models.ClientAccount.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [AllowAny, ]

    response_status = status.HTTP_400_BAD_REQUEST
    response_post_msg = 'validation error'

    @action(methods=['post'], detail=False, permission_classes=[AllowAny],
            url_path='(?P<cli_uid>[^/.]+)/cash')
    def send_client_cash_action(self, request: Request, cli_uid: str) -> Response:
        """ Sending cash endpoint.
        Warn: AllowAny for review, use IsAuthenticated for production.

        Params:
            "request" - request: object,
            "cli_uid" - user base64: id url argument,

        Api Params: {
            "cash": <amount>,
            "clients": [ "cli_uid", ... ]
        }

        Return: {
            msg: str message,
            status: Rest Status
        }

        """
        serializer = serializers.ClientSerializerSendCashForm(data=request.data)

        if serializer.is_valid():
            client = self.queryset.get(id=cli_uid)
            self.response_status, self.response_post_msg = client.manager.send_cash(**serializer.data)
        return Response({'msg': self.response_post_msg}, status=self.response_status)
