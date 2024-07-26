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


def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    return type(obj).__class__.__name__ == "ModelMetaclass"


def parse_pydantic_schema(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    for key, value in parsed_schema.items():
        try:
            if isinstance(value, list) and len(value):
                if is_pydantic(value[0]):
                    parsed_schema[key] = [
                        schema.Meta.orm_model(**schema.dict()) for schema in value
                    ]
            else:
                if is_pydantic(value) and hasattr(value, "dict"):
                    value_dict = value.dict()
                    if value_dict is not None:
                        print(f"Parsed SCHEMA KEY: {parsed_schema[key]}\nVALUE DICT for ORM MODEL: {value_dict}")
                        parsed_schema[key] = value.Meta.orm_model(**value_dict)
        except AttributeError:
            raise AttributeError(
                "Found nested Pydantic model but Meta.orm_model was not specified."
            )
    return parsed_schema
