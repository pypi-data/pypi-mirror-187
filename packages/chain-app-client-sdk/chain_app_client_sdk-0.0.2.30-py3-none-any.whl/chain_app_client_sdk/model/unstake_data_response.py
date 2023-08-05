# coding: utf-8

"""
    Chain App BIND client SDK

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

from chain_app_client_sdk import schemas  # noqa: F401


class UnstakeDataResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "txh",
            "transaction_fee",
        }
        
        class properties:
            transaction_fee = schemas.NumberSchema
            txh = schemas.StrSchema
            __annotations__ = {
                "transaction_fee": transaction_fee,
                "txh": txh,
            }
    
    txh: MetaOapg.properties.txh
    transaction_fee: MetaOapg.properties.transaction_fee
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_fee"]) -> MetaOapg.properties.transaction_fee: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["txh"]) -> MetaOapg.properties.txh: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["transaction_fee", "txh", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_fee"]) -> MetaOapg.properties.transaction_fee: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["txh"]) -> MetaOapg.properties.txh: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["transaction_fee", "txh", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        txh: typing.Union[MetaOapg.properties.txh, str, ],
        transaction_fee: typing.Union[MetaOapg.properties.transaction_fee, decimal.Decimal, int, float, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'UnstakeDataResponse':
        return super().__new__(
            cls,
            *args,
            txh=txh,
            transaction_fee=transaction_fee,
            _configuration=_configuration,
            **kwargs,
        )
