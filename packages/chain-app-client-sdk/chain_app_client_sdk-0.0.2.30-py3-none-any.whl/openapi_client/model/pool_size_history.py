# coding: utf-8

"""
    BIND Public API

    Description for BIND.   # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@bind.com
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from openapi_client import schemas  # noqa: F401


class PoolSizeHistory(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "data",
            "test",
        }
        
        class properties:
            test = schemas.StrSchema
            
            
            class data(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['PoolSizeHistoryItem']:
                        return PoolSizeHistoryItem
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['PoolSizeHistoryItem'], typing.List['PoolSizeHistoryItem']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'data':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'PoolSizeHistoryItem':
                    return super().__getitem__(i)
            __annotations__ = {
                "test": test,
                "data": data,
            }
    
    data: MetaOapg.properties.data
    test: MetaOapg.properties.test
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["test"]) -> MetaOapg.properties.test: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["test", "data", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["test"]) -> MetaOapg.properties.test: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["test", "data", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        data: typing.Union[MetaOapg.properties.data, list, tuple, ],
        test: typing.Union[MetaOapg.properties.test, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PoolSizeHistory':
        return super().__new__(
            cls,
            *args,
            data=data,
            test=test,
            _configuration=_configuration,
            **kwargs,
        )

from openapi_client.model.pool_size_history_item import PoolSizeHistoryItem
