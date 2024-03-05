import json
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class MetaBase():
    default_data = None

    def __getitem__(self, key):
        return self.data[key]

    @property
    def data(self):
        if not hasattr(self, '_meta_data'):
            self._meta_data = json.loads(self.meta) if self.meta else self.default_data
        return self._meta_data

    def store_data(self, data):
        self.meta = json.dumps(data)

    def data_save(self):
        self.store_data(self._meta_data)

    @property
    def keys(self):
        return self.data.keys()
