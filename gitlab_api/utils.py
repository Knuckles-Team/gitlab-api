#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union, Any

from sqlalchemy.engine import reflection
import requests
from sqlalchemy.orm import AppenderQuery
from sqlalchemy.orm.collections import InstrumentedList

try:
    from gitlab_api.gitlab_models import (
        Response,
    )
except ModuleNotFoundError:
    from gitlab_models import (
        Response,
    )

try:
    from gitlab_api.gitlab_models import (
        LabelsDBModel,
        LabelDBModel,
        TagDBModel,
        TagsDBModel,
        CommitDBModel,
        ParentIDDBModel,
        ParentIDsDBModel,
        ArtifactDBModel,
        ArtifactsDBModel,
    )
except ModuleNotFoundError:
    pass
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
        print(f"\nPydantic True for {obj}")
        return True
    else:
        print(f"\nPydantic False for {obj}")
        return False


def pydantic_to_sqlalchemy(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    parsed_schema = remove_none_values(dictionary=parsed_schema)
    for key, value in parsed_schema.items():
        if not value:
            continue
        print(f"\n\n\nKEY: {key} VALUE: {value}")
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                print(f"\n\nUpdating: {key} {parsed_schema[key]}")
                parsed_schema[key] = [
                    item.Meta.orm_model(**pydantic_to_sqlalchemy(item))
                    for item in value
                    if value is not None
                ]
                print(f"\n\nFinished Updated List: {key} {parsed_schema[key]}")
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

    for key, value in model.items():
        if key == "base_type":
            continue
        print(f"SCANNING: {str(key)}")
        for item in model[key]:
            upsert_row(session=session, model=item)


def upsert_row(session, model, processed_models=None):
    if model is None:
        return None

    if processed_models is None:
        processed_models = set()

    model_type = type(model)
    print(f"\n\nSearching for {model} in {model_type}")
    model_identifier = (model_type, model.id)

    if model_identifier in processed_models:
        return None

    processed_models.add(model_identifier)

    # Function to upsert nested models
    def upsert_nested_models(session, model):
        related_models = []
        for relation in model.__mapper__.relationships:
            related_model = getattr(model, relation.key)
            if isinstance(related_model, InstrumentedList):
                for item in related_model:
                    if item is not None:
                        related_models.append(item)
            elif isinstance(related_model, AppenderQuery):
                pass
            elif related_model is not None:
                related_models.append(related_model)

        # Recursively upsert nested models first
        for related_model in related_models:
            upsert_row(
                session=session,
                model=related_model,
                processed_models=processed_models,
            )

    # Upsert nested models first
    upsert_nested_models(session, model)

    try:
        print(f"\n\nCommitting: {model}")
        existing_model = session.merge(model)
        session.commit()
        print("Committed Session!")
        return existing_model
    except Exception as e:
        session.rollback()
        print(f"Error inserting/updating {model_type.__name__} with ID {model.id}: {e}")


def create_table(db_instance, engine):
    inspector = reflection.Inspector.from_engine(engine)
    table_name = db_instance.__table__.name

    if not inspector.has_table(table_name):
        db_instance.__table__.create(engine)
        print(f"Table {table_name} created.")
    else:
        print(f"Table {table_name} already exists.")
