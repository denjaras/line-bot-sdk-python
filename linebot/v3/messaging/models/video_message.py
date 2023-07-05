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
from pydantic import BaseModel, Field, StrictStr
from linebot.v3.messaging.models.message import Message
from linebot.v3.messaging.models.quick_reply import QuickReply
from linebot.v3.messaging.models.sender import Sender

class VideoMessage(Message):
    """
    VideoMessage
    """
    original_content_url: Optional[StrictStr] = Field(None, alias="originalContentUrl")
    preview_image_url: Optional[StrictStr] = Field(None, alias="previewImageUrl")
    tracking_id: Optional[StrictStr] = Field(None, alias="trackingId")
    type: str = "video"

    __properties = ["type", "quickReply", "sender", "originalContentUrl", "previewImageUrl", "trackingId"]

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
    def from_json(cls, json_str: str) -> VideoMessage:
        """Create an instance of VideoMessage from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of quick_reply
        if self.quick_reply:
            _dict['quickReply'] = self.quick_reply.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sender
        if self.sender:
            _dict['sender'] = self.sender.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> VideoMessage:
        """Create an instance of VideoMessage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return VideoMessage.parse_obj(obj)

        _obj = VideoMessage.parse_obj({
            "type": obj.get("type"),
            "quick_reply": QuickReply.from_dict(obj.get("quickReply")) if obj.get("quickReply") is not None else None,
            "sender": Sender.from_dict(obj.get("sender")) if obj.get("sender") is not None else None,
            "original_content_url": obj.get("originalContentUrl"),
            "preview_image_url": obj.get("previewImageUrl"),
            "tracking_id": obj.get("trackingId")
        })
        return _obj
