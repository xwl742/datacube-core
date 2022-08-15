# This file is part of the Open Data Cube, see https://opendatacube.org for more information
#
# Copyright (c) 2015-2022 ODC Contributors
# SPDX-License-Identifier: Apache-2.0
import logging

from datacube.index.memory._datasets import DatasetResource  # type: ignore
from datacube.index.memory._fields import get_dataset_fields
from datacube.index.memory._metadata_types import MetadataTypeResource
from datacube.index.memory._products import ProductResource
from datacube.index.memory._users import UserResource
from datacube.index.abstract import AbstractIndex, AbstractIndexDriver
from datacube.model import MetadataType

_LOG = logging.getLogger(__name__)


class Index(AbstractIndex):
    """
    Lightweight in-memory index driver
    """

    def __init__(self) -> None:
        self._users = UserResource()
        self._metadata_types = MetadataTypeResource()
        self._products = ProductResource(self.metadata_types)
        self._datasets = DatasetResource(self.products)

    @property
    def users(self) -> UserResource:
        return self._users

    @property
    def metadata_types(self) -> MetadataTypeResource:
        return self._metadata_types

    @property
    def products(self) -> ProductResource:
        return self._products

    @property
    def datasets(self) -> DatasetResource:
        return self._datasets

    @property
    def url(self) -> str:
        return "memory"

    @classmethod
    def from_config(cls, config, application_name=None, validate_connection=True):
        return cls()

    @classmethod
    def get_dataset_fields(cls, doc):
        return get_dataset_fields(doc)

    def init_db(self, with_default_types=True, with_permissions=True):
        return True

    def close(self):
        pass

    def create_spatiotemporal_index(self, crs_str: str) -> None:
        _LOG.warning("Postgres driver does not support spatio-temporal indexes")

    def __repr__(self):
        return "Index<memory>"


class MemoryIndexDriver(AbstractIndexDriver):
    @staticmethod
    def connect_to_index(config, application_name=None, validate_connection=True):
        return Index.from_config(config, application_name, validate_connection)

    @staticmethod
    def metadata_type_from_doc(definition: dict) -> MetadataType:
        """
        :param definition:
        """
        MetadataType.validate(definition)  # type: ignore
        return MetadataType(definition,
                            dataset_search_fields=Index.get_dataset_fields(definition))


def index_driver_init():
    return MemoryIndexDriver()
