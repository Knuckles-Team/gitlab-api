#!/usr/bin/python
# coding: utf-8
import logging
import os
import pickle
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
    dictionary.pop("json_output", None)
    dictionary.pop("raw_output", None)
    dictionary.pop("status_code", None)
    dictionary.pop("headers", None)
    dictionary.pop("message", None)
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
    logging.debug(f"\n\nSchema: {schema}")
    parsed_schema = dict(schema)
    parsed_schema = remove_none_values(dictionary=parsed_schema)

    logging.debug(f"\n\nCleaned Schema: {parsed_schema}")
    for key, value in parsed_schema.items():
        if not value:
            continue
        logging.debug(f"\n\n\nKEY: {key} VALUE: {value}")
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                logging.debug(f"\n\nUpdating: {key} {parsed_schema[key]}")
                parsed_schemas = []
                for item in value:
                    logging.debug(f"\nGoing through Item: {item} in Value: {value}")
                    new_schema = pydantic_to_sqlalchemy(item)
                    logging.debug(
                        f"\nNew schema: {new_schema}\n\tFor Model: {item.Meta.orm_model}"
                    )
                    new_model = item.Meta.orm_model(**new_schema)
                    logging.debug(
                        f"\nNew model: {new_model}\n\tFor Item: {item}"  # \n\tIn Value: {value}"
                    )
                    parsed_schemas.append(new_model)
                parsed_schema[key] = parsed_schemas
            elif is_pydantic(value):
                logging.debug(f"\n\nUpdating Nonlist: {key} {value}")
                new_model = value.Meta.orm_model(**pydantic_to_sqlalchemy(value))
                logging.debug(
                    f"\n\nNew Model: {new_model} for schema: {parsed_schema} in key: {key} of value: {value}"
                )
                parsed_schema[key] = new_model
                logging.debug(f"\n\nFinished Updated Nonlist: {key} {value}")
        except AttributeError as e:
            logging.debug(
                f"\n\nFound nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified.\nExact Error: {e}"
            )
            raise (
                f"\n\nFound nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified.\nExact Error: {e}"
            )
    logging.debug(f"\n\nReturning parsed schema: {parsed_schema}")
    return parsed_schema


def upsert(model: Any, session):
    if not model or "data" not in model:
        logging.debug(f"No data in model: {model}")
        return

    data = model["data"]
    item_ids = [item.id for item in data if item.id]
    existing_items = (
        session.query(data[0].__class__)
        .filter(data[0].__class__.id.in_(item_ids))
        .all()
    )
    existing_items_map = {item.id: item for item in existing_items}

    for item in data:
        logging.debug(f"Going through Item: {item}")
        if item.id and item.id in existing_items_map:
            existing_model = existing_items_map[item.id]
            logging.debug(f"Found Existing Model: {existing_model}")
            for attr, value in vars(item).items():
                setattr(existing_model, attr, value)
            session.merge(existing_model)
        else:
            session.merge(item)

    session.commit()


def create_table(db_instance, engine):
    inspector = reflection.Inspector.from_engine(engine)
    table_name = db_instance.__table__.name

    if not inspector.has_table(table_name):
        db_instance.__table__.create(engine)
        logging.debug(f"Table {table_name} created.")
    else:
        logging.debug(f"Table {table_name} already exists.")


def save_model(model: Any, file_name: str = "model", file_path: str = ".") -> str:
    pickle_file = os.path.join(file_path, f"{file_name}.pkl")
    with open(pickle_file, "wb") as file:
        pickle.dump(model, file)
    return pickle_file


def load_model(file: str) -> Any:
    with open(file, "rb") as model_file:
        model = pickle.load(model_file)
    return model
