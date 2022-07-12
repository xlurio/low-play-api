import os
import time
from core import models
from django.core.exceptions import ObjectDoesNotExist

from games_price_digger.src.image_downloaders.image_downloader import ImageDownloader


class GamePipeline:

    def process_item(self, item, _):
        try:
            item = item.get('game_metadata')
            return self._get_or_create_object(item)
        except KeyError:
            return item

    def _get_or_create_object(self, item):
        try:
            return self._update_object(item)

        except ObjectDoesNotExist:
            return self._create_object(item)

    def _create_object(self, item):
        game_name = item.get_name()
        game_score = item.get_score()
        game_image = item.get_image()
        image_path = self._get_image_path(game_image)

        models.GameModel.objects.create(
            name=game_name, score=game_score, image=image_path
        )

        time.sleep(3)

        return {
            'name': game_name,
            'score': game_score,
            'image': image_path,
        }

    def _get_image_destination_folder(self):
        current_module = os.path.dirname(__file__)
        module_path = os.path.abspath(current_module)
        root_folder = os.path.join(module_path, '../../')
        destination_folder = os.path.join(root_folder, './api/uploads/game')
        return os.path.abspath(destination_folder)

    def _update_object(self, item):
        game_name = item.get_name()
        game_score = item.get_score()
        game_image = item.get_image()
        image_path = self._get_image_path(game_image)

        game = models.GameModel.objects.get(
            name=game_name
        )
        setattr(game, 'score', game_score)
        setattr(game, 'image', image_path)
        game.save()

        time.sleep(3)

        return {
            'name': game_name,
            'score': game_score,
            'image': image_path,
        }

    def _get_image_path(self, url):
        destination_folder = self._get_image_destination_folder()
        downloader = ImageDownloader(destination_folder)

        downloader.download(url)
        image_filename = downloader.get_filename()
        image_path = os.path.join('uploads/game', image_filename)
        return image_path


class PricePipeline:

    def process_item(self, item, _):
        try:
            return self._get_or_create_objects(item)
        except KeyError:
            return item
        except AttributeError:
            return item

    def _get_or_create_objects(self, item):
        game_data = item.get('game')
        search_data = item.get('search')

        self.game = models.GameModel.objects.get_or_create(
            name=search_data.get_game()
        )[0]
        self.store = models.StoreModel.objects.get_or_create(
            name=search_data.get_store()
        )[0]
        self.price = game_data.get_price()
        self.link = game_data.get_link()

        self._create_price_object()

        return {
            'game': str(game_data),
            'search': str(search_data),
        }

    def _create_price_object(self):
        try:
            self._update_price_object()
        except ObjectDoesNotExist:
            self._create_price_object()

    def _update_price_object(self):
        price_object = models.PriceModel.objects.get(
            game=self.game,
            store=self.store,
        )
        setattr(price_object, 'price', self.price)
        setattr(price_object, 'link', self.link)
        price_object.save()

    def _create_price_object(self):
        models.PriceModel.objects.create(
            game=self.game,
            store=self.store,
            price=self.price,
            link=self.link,
        )
