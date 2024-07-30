#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union

import requests

try:
    from gitlab_api.gitlab_models import (
        Response,
    )
except ModuleNotFoundError:
    from gitlab_models import (
        Response,
    )
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_response(response: requests.Response) -> Union[Response, requests.Response]:
    try:
        response.raise_for_status()
    except Exception as response_error:
        logging.error(f"Response Error: {response_error}")
    status_code = response.status_code
    raw_output = response.content
    headers = response.headers
    try:
        response = response.json()
    except Exception as response_error:
        logging.error(f"JSON Conversion Error: {response_error}")
    try:
        response = Response(
            data=response,
            status_code=status_code,
            raw_output=raw_output,
            json_output=response,
            headers=headers,
        )
    except Exception as response_error:
        logging.error(f"Response Model Application Error: {response_error}")

    return response


def remove_none_values(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None}


def pydantic_to_sqlalchemy(pydantic_model):
    # Check if the model is already converted by ensuring the model doesn't have Meta pydantic field,
    # but does have base_type sqlalchemy field.
    if (
        not hasattr(pydantic_model, "Meta")
        or not hasattr(pydantic_model.Meta, "orm_model")
    ) and hasattr(pydantic_model, "base_type"):
        sqlalchemy_instance = pydantic_model
        return sqlalchemy_instance
    sqlalchemy_model = pydantic_model.Meta.orm_model
    sqlalchemy_instance = sqlalchemy_model()
    for key, value in pydantic_model.model_dump(exclude_unset=True).items():
        if isinstance(value, list):
            if len(value) > 0:
                related_instances = [
                    (
                        pydantic_to_sqlalchemy(item)
                        if hasattr(item, "Meta") and hasattr(item.Meta, "orm_model")
                        else item
                    )
                    for item in value
                ]
                setattr(sqlalchemy_instance, key, related_instances)
        elif isinstance(value, dict):
            related_sqlalchemy_model = getattr(
                sqlalchemy_model, key
            ).property.mapper.class_
            value = remove_none_values(value)
            nested_model = related_sqlalchemy_model(**value)
            related_instance = pydantic_to_sqlalchemy(nested_model)
            setattr(sqlalchemy_instance, key, related_instance)
        else:
            if value:
                setattr(sqlalchemy_instance, key, value)
    return sqlalchemy_instance
