#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union, Any

from sqlalchemy.engine import reflection
import requests

from gitlab_api.gitlab_response_models import Response

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


def remove_none_values(dictionary: dict) -> dict:
    return {k: v for k, v in dictionary.items() if v is not None}


def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    if hasattr(obj, "Meta") and hasattr(obj.Meta, "orm_model"):
        logging.debug(f"\nPydantic True for {obj}")
        return True
    else:
        logging.debug(f"\nPydantic False for {obj}")
        return False


def pydantic_to_sqlalchemy(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    print(f"SCHEMA: {schema}")
    parsed_schema = dict(schema)
    parsed_schema = remove_none_values(dictionary=parsed_schema)
    for key, value in parsed_schema.items():
        if not value:
            continue
        print(f"\n\n\nKEY: {key} VALUE: {value}")
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                print(f"\n\nUpdating: {key} {parsed_schema[key]}")
                parsed_schemas = []
                for item in value:
                    print(f"\nGoing through Item: {item} in Value: {value}")
                    new_schema = pydantic_to_sqlalchemy(item)
                    print(
                        f"\nNew schema: {new_schema}\nFor Model: {item.Meta.orm_model}\nFor Item: {item}\nIn Value: {value}"
                    )
                    new_model = item.Meta.orm_model(**new_schema)
                    print(
                        f"\nNew model: {new_model}\nFor Item: {item}\nIn Value: {value}"
                    )
                    parsed_schemas.append(new_model)
                # parsed_schema[key] = [
                #     item.Meta.orm_model(**pydantic_to_sqlalchemy(item))
                #     for item in value
                # ]
                parsed_schema = parsed_schemas
                # print(f"\n\nFinished Updated List: {key} {parsed_schema[key]}")
            elif is_pydantic(value):
                print(f"\n\nUpdating Nonlist: {key} {value}")
                new_model = value.Meta.orm_model(**pydantic_to_sqlalchemy(value))
                print(f"\n\nNew Model: {new_model}")
                parsed_schema[key] = new_model
                print(f"\n\nFinished Updated Nonlist: {key} {value}")
        except AttributeError:
            raise AttributeError(
                f"\n\nFound nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified."
            )
    print(f"\n\nReturning parsed schema: {parsed_schema}")
    return parsed_schema


def upsert(model: Any, session):

    if not model:
        return

    for item in model:
        session.merge(item)
        print(f"MERGED: {item}\n\n")

    session.commit()

    # for key, value in model.items():
    #     if key == "base_type":
    #         continue
    #     print(f"SCANNING: {str(key)} - {model[key]}")
    #     for item in model[key]:
    #         session.merge(item)
    #         print(f"MERGED: {item}\n\n")
    #
    #     session.commit()


def create_table(db_instance, engine):
    inspector = reflection.Inspector.from_engine(engine)
    table_name = db_instance.__table__.name

    if not inspector.has_table(table_name):
        db_instance.__table__.create(engine)
        logging.debug(f"Table {table_name} created.")
    else:
        logging.debug(f"Table {table_name} already exists.")
