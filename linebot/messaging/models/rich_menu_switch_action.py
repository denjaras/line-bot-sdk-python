# coding: utf-8

"""
    LINE Messaging API

    This document describes LINE Messaging API.  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, constr
from linebot.messaging.models.action import Action

class RichMenuSwitchAction(Action):
    """
    RichMenuSwitchAction
    """
    data: Optional[constr(strict=True, max_length=300, min_length=0)] = None
    rich_menu_alias_id: Optional[constr(strict=True, max_length=32, min_length=0)] = Field(None, alias="richMenuAliasId")
    type: str = "richmenuswitch"

    __properties = ["type", "label", "data", "richMenuAliasId"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> RichMenuSwitchAction:
        """Create an instance of RichMenuSwitchAction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RichMenuSwitchAction:
        """Create an instance of RichMenuSwitchAction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RichMenuSwitchAction.parse_obj(obj)

        _obj = RichMenuSwitchAction.parse_obj({
            "type": obj.get("type"),
            "label": obj.get("label"),
            "data": obj.get("data"),
            "rich_menu_alias_id": obj.get("richMenuAliasId")
        })
        return _obj
