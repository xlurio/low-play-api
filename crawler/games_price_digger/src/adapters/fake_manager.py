from django.core.exceptions import ObjectDoesNotExist


class FakeManager:

    def __init__(self, model, data):
        self._model = model
        self._data = data

    def get_or_create(self, **kwargs):
        try:
            object_got = self.get(**kwargs)
            return (object_got, False)

        except IndexError:
            object_created = self.create(**kwargs)
            return (object_created, True)

    def create(self, **kwargs):
        new_object = self._model(**kwargs)
        self._data.append(new_object)

    def get(self, **kwargs):
        data = self._data

        for filter_arg in kwargs.items():
            data = self._filter_data(filter_arg, data)

        found_object = data[0]

        if not (found_object is None):
            return found_object

        raise ObjectDoesNotExist()

    def _filter_data(self, filter_parameter, data_to_filter):
        KEY = 0
        VALUE = 1
        model_field = filter_parameter[KEY]

        data = [
            data_object for data_object in data_to_filter
            if filter_parameter[VALUE] ==
            getattr(data_object, model_field)
        ]

        return data

    def _get_first_row(self, data):
        FIRST_ITEM = 0

        for table_column in data.keys():
            data[table_column] = data[table_column][FIRST_ITEM]

        return data

    def set_data(self, data):
        self._data = data
