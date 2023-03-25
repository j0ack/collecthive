"""Meta model for Pydantic objects."""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict

from bson.objectid import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    """ObjectId wrapper.

    MongoDB stores data as BSON, BSON has support for additional non-JSON-native
    data types, including ObjectId which can't be directly encoded as JSON.
    Because of this, we convert ObjectIds to strings before storing them as
    the _id.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CollectHiveModel(BaseModel):
    """CollectHive meta model."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = datetime.utcnow()

    class Config:
        json_encoders = {ObjectId: str}

    def dict(self) -> Dict[str, Any]:
        """Override dict super method to serialize ObjectId."""
        data = super().dict()
        copy = deepcopy(data)
        for key, value in data.items():
            if isinstance(value, ObjectId):
                copy[key] = str(value)
            elif isinstance(value, datetime):
                copy[key] = value.isoformat()

        return copy
