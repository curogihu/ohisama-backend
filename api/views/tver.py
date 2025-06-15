from rest_framework import viewsets
from django.utils.timezone import now

from api.models import TVer
from api.serializers import TVerSerializer

class TVerViewSet(viewsets.ModelViewSet):
    serializer_class = TVerSerializer

    def get_queryset(self):
        queryset = TVer.objects.filter(is_deleted=False)

        # ?member_id=2 のような指定があれば絞る
        member_id = self.request.query_params.get('member_id')
        if member_id:
            queryset = queryset.filter(members__id=member_id)

        current = now()
        queryset = queryset.filter(start_datetime__lte=current, end_datetime__gte=current)

        return queryset.order_by('-start_datetime')