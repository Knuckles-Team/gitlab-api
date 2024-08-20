#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union, Any

from sqlalchemy.engine import reflection
import requests

from gitlab_api.gitlab_response_models import Response
from sqlalchemy.orm import AppenderQuery
from sqlalchemy.orm.collections import InstrumentedList

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
    print(f"\n\nSCHEMA: {schema}")
    parsed_schema = dict(schema)
    parsed_schema = remove_none_values(dictionary=parsed_schema)

    print(f"\n\nCLEANED PARSED SCHEMA: {parsed_schema}")
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
                        f"\nNew schema: {new_schema}\n\tFor Model: {item.Meta.orm_model}"
                    )
                    new_model = item.Meta.orm_model(**new_schema)
                    print(
                        f"\nNew model: {new_model}\n\tFor Item: {item}"  # \n\tIn Value: {value}"
                    )
                    parsed_schemas.append(new_model)
                parsed_schema[key] = parsed_schemas
            elif is_pydantic(value):
                print(f"\n\nUpdating Nonlist: {key} {value}")
                new_model = value.Meta.orm_model(**pydantic_to_sqlalchemy(value))
                print(
                    f"\n\nNew Model: {new_model} for schema: {parsed_schema} in key: {key} of value: {value}"
                )
                parsed_schema[key] = new_model
                print(f"\n\nFinished Updated Nonlist: {key} {value}")
        except AttributeError as e:
            print(
                f"\n\nFound nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified.\nExact Error: {e}"
            )
            raise (
                f"\n\nFound nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified.\nExact Error: {e}"
            )
    print(f"\n\nReturning parsed schema: {parsed_schema}")
    return parsed_schema


def upsert(model: Any, session):

    if not model:
        return

    for key, value in model.items():
        if key == "data":
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


# def upsert_row(session, model, processed_models=None):
#     if model is None:
#         return None
#
#     if processed_models is None:
#         processed_models = set()
#
#     model_type = type(model)
#     model_identifier = (model_type, model.id)
#
#     if model_identifier in processed_models:
#         return None
#
#     processed_models.add(model_identifier)
#
#     # Ensure related models like UserDBModel are attached to the session
#     if isinstance(model, ProjectDBModel):
#         if model.creator and not session.contains(model.creator):
#             session.add(model.creator)
#         if model.owner and not session.contains(model.owner):
#             session.add(model.owner)
#
#     # Function to upsert nested models
#     def upsert_nested_models(session, model):
#         for relation in model.__mapper__.relationships:
#             related_model = getattr(model, relation.key)
#             if isinstance(related_model, InstrumentedList):
#                 for item in related_model:
#                     if item is not None:
#                         upsert_row(session=session, model=item, processed_models=processed_models)
#             elif isinstance(related_model, AppenderQuery):
#                 pass
#             elif related_model is not None:
#                 upsert_row(session=session, model=related_model, processed_models=processed_models)
#
#     # Upsert nested models first
#     upsert_nested_models(session, model)
#
#     try:
#         session.add(model)  # Use session.add() to handle new objects
#         session.commit()
#         return model
#     except Exception as e:
#         session.rollback()
#         print(f"Error inserting/updating {model_type.__name__} with ID {model.id}: {e}")
#         raise


# def upsert(model: Any, session):
#
#     if not model:
#         return
#     with session.no_autoflush:
#         for item in model["data"]:
#             # Load existing associated objects to avoid duplicate insertion
#             if item.id:
#                 existing_model = session.query(item.__class__).get(item.id)
#                 if existing_model:
#                     # Update existing model attributes with incoming item's attributes
#                     for attr, value in vars(item).items():
#                         if attr != 'id':  # Do not overwrite the ID
#                             print(f"Setting {attr}-{value} for {existing_model}")
#                             setattr(existing_model, attr, value)
#                     item = existing_model
#
#             # Ensure all nested/related models are merged first
#             for attr, value in vars(item).items():
#                 if isinstance(value, BaseDBModel):  # Assuming all models inherit from BaseDBModel
#                     # Check if the related model already exists
#                     related_existing = session.query(value.__class__).get(value.id)
#                     if related_existing:
#                         # Update the existing related model's attributes
#                         for rel_attr, rel_value in vars(value).items():
#                             if rel_attr != 'id':  # Do not overwrite the ID
#                                 setattr(related_existing, rel_attr, rel_value)
#                         setattr(item, attr, related_existing)
#                     else:
#                         session.merge(value)
#
#             # Now merge the item (parent model)
#             session.merge(item)
#
#     session.commit()

# def upsert(model: Any, session):
#
#     if not model:
#         return
#
#     # print(f"\n\nMODEL TO INSERT: {model['data']}")
#
#     # if hasattr(model, "data"):
#     #     print("\n\nHAS ATTR TRUE FOR DATA")
#     # for item in model["data"]:
#     #     print(f"MODEL TO INSERT: {model}")
#     #     session.merge(item)
#     #     print(f"MERGED: {item}\n\n")
#     # session.commit()
#     print(f"EVEN UPSERT? MODEL!!!!: {model}")
#     if hasattr(model, "data"):
#         print("EVEN UPSERT234234234234234234234?!")
#     for item in model["data"]:
#         # Load existing associated objects to avoid duplicate insertion
#         print(f"ITEM ID: {item.id} - {item}")
#         if item.id:
#             existing_model = session.query(item.__class__).get(item.id)
#             print(f"\n\n\n\nEXISTING MODEL: {existing_model}")
#             if existing_model:
#                 print(f"\n\n\n\nFOUND EXISTING MODEL:!!!! {existing_model}")
#                 item = existing_model
#
#         # Repeat similar logic for other associated models (commit, runner, etc.)
#
#         session.merge(item)
#     session.commit()


def create_table(db_instance, engine):
    inspector = reflection.Inspector.from_engine(engine)
    table_name = db_instance.__table__.name

    if not inspector.has_table(table_name):
        db_instance.__table__.create(engine)
        logging.debug(f"Table {table_name} created.")
    else:
        logging.debug(f"Table {table_name} already exists.")
