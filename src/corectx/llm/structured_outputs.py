from __future__ import annotations

from pydantic import BaseModel


def schema_for(model: type[BaseModel]) -> dict:
    return model.model_json_schema()
