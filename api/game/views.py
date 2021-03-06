import pandas as pd

from rest_framework.decorators import action
# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceModel, StoreModel
# noinspection PyUnresolvedReferences
from game.serializers import (
    GameSerializer, PriceSerializer, PriceDetailSerializer, StoreSerializer
)
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status


class BasicGameAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Basic view set class for the game API"""

    def get_queryset(self):
        """Retrieve the objects of the serializer"""
        return self.queryset.order_by('name')


class GameViewSet(BasicGameAttrViewSet):
    """View set to manage the game objects"""
    queryset = GameModel.objects.all()
    serializer_class = GameSerializer


class StoreViewSet(BasicGameAttrViewSet):
    """View set to manage the game objects"""
    queryset = StoreModel.objects.all()
    serializer_class = StoreSerializer


class PriceViewSet(viewsets.ModelViewSet):
    """View set to manage the price objects"""
    queryset = PriceModel.objects.all()
    serializer_class = PriceSerializer

    def get_queryset(self):
        """Retrieve the price objects"""
        filtered_by_game_id = self._filter_by_game_id(self.queryset)
        return filtered_by_game_id.order_by('price')

    def _filter_by_game_id(self, queryset):
        if self.request.query_params.get('game_id'):
            game_id = self.request.query_params.get('game_id')
            parsed_game_id = int(game_id)

            return queryset.filter(game__id=parsed_game_id)

        return queryset

    @action(detail=False, methods=['get'])
    def best_prices(self, request, pk=None):

        lowest_prices_ids = self._get_lowest_prices_ids()
        filtered_queryset = self.queryset.filter(id__in=lowest_prices_ids)
        filtered_queryset = self._filter_by_name(filtered_queryset)
        initial_index = self._filter_by_start()
        final_index = self._filter_by_end()

        ordered_queryset = filtered_queryset.order_by('price')
        ordered_queryset = ordered_queryset[initial_index:final_index]

        serializer = self.get_serializer(ordered_queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def _get_lowest_prices_ids(self):
        price_query = self.queryset.values()
        price_data = pd.DataFrame(price_query.values())
        try:
            return self._get_filtered_ids(price_data)
        except KeyError:
            raise KeyError(f'The available columns are: {price_data.columns}')

    def _get_filtered_ids(self, price_data):
        filtered_price_data = price_data[
            ['id', 'game_id', 'price']
        ].groupby(
            ['game_id']
        ).min()
        return list(filtered_price_data['id'])

    def _filter_by_name(self, queryset):
        game_name = self.request.query_params.get('game_name')

        if game_name:
            return queryset.filter(
                game__name__icontains=game_name
            )

        return queryset

    def _filter_by_start(self):
        ranking_start = self.request.query_params.get('from')

        if ranking_start:
            ranking_start = int(ranking_start) - 1
            return ranking_start

        return 0

    def _filter_by_end(self):
        ranking_end = self.request.query_params.get('to')

        if ranking_end:
            ranking_end = int(ranking_end)
            return ranking_end

        return 1

    def get_serializer_class(self):
        """Return the appropriated serializer class based on the action
        requested"""
        if self.action == 'retrieve' or self.action == 'best_prices':
            return PriceDetailSerializer
        return self.serializer_class
