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
    Iterates through pydantic schema and parses all nested (to all nested layers) schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    def recursive_parse(value):
        if isinstance(value, list) and len(value):
            if is_pydantic(value[0]):
                return [value[0].Meta.orm_model(**recursive_parse(item.model_dump())) for item in value]
        elif is_pydantic(value):
            value_dict = value.dict()
            for key, nested_value in value_dict.items():
                if isinstance(nested_value, (list, dict)) or is_pydantic(nested_value):
                    value_dict[key] = recursive_parse(nested_value)
            return value.Meta.orm_model(**value_dict)
        return value

    parsed_schema = schema.model_dump()
    print(f"\nPARSED SCHEMA: {parsed_schema}\n")
    for key, value in parsed_schema.items():
        print(f"\nParsed SCHEMA KEY: {parsed_schema[key]}\n\nVALUE DICT for ORM MODEL: {value}\n")
        parsed_schema[key] = recursive_parse(value)

    return parsed_schema
