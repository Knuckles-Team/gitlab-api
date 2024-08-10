#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union, Any

from sqlalchemy.engine import reflection
import requests

try:
    from gitlab_api.gitlab_models import (
        Response,
    )
except ModuleNotFoundError:
    from gitlab_models import (
        Response,
    )

try:
    from gitlab_api.gitlab_db_models import (
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


#
#
# def get_related_model(sqlalchemy_model, key, value):
#     """Get the related SQLAlchemy model for a given key."""
#     mapper = class_mapper(sqlalchemy_model)
#     for prop in mapper.iterate_properties:
#         if prop.key == key:
#             return prop.mapper.class_
#     raise ValueError(f"Unable to find related model for key: {key}")
#
#
# def validate(key, value, session, sqlalchemy_model):
#     if isinstance(value, list):
#         print(f"\n\nValue that is a list: {value} for key: {key}")
#         related_models = validate_list(list_object=value, session=session)
#         new_model = related_models
#         print(f"\n\nSQLAlchemy List Model Set: {related_models}")
#     elif isinstance(value, dict):
#         print(f"\n\nValue that is a dict: {value} for key: {key}")
#         related_model = validate_dict(
#             dictionary=value,
#             parent_key=key,
#             sqlalchemy_model=sqlalchemy_model,
#             session=session,
#         )
#         print(f"\n\nSetting Related Model: {related_model} for {key}")
#         new_model = related_model
#         print(f"\n\nSQLAlchemy Dict Model Set: {related_model}")
#     else:
#         print(f"\n\nImmediately Setting Attribute: {value}")
#         new_model = value
#         print(f"\n\nImmediately Set Attribute: {value}")
#
#     return new_model
#
#
# def validate_list(list_object: List, session) -> List:
#     related_models = [
#         (
#             pydantic_to_sqlalchemy(pydantic_model=item, session=session)
#             if hasattr(item, "Meta") and hasattr(item.Meta, "orm_model")
#             else item
#         )
#         for item in list_object
#     ]
#     print(f"\n\nRelated models: {related_models}")
#     return related_models
#
#
# def validate_dict(
#     dictionary: Dict, parent_key: str, sqlalchemy_model: Any, session=None
# ) -> Any:
#     related_sqlalchemy_model = None
#     mapper = class_mapper(sqlalchemy_model)
#     for prop in mapper.iterate_properties:
#         if prop.key == parent_key:
#             related_sqlalchemy_model = prop.mapper.class_
#     if not related_sqlalchemy_model:
#         raise ValueError(f"Unable to find related model for key: {parent_key}")
#     print(f"\n\nRelated instance: {related_sqlalchemy_model}")
#     # # Special handling for labels
#     if related_sqlalchemy_model == LabelsDBModel:
#         labels = []
#         for label in dictionary["labels"]:
#             labels.append(LabelDBModel(**label))
#         if labels:
#             labels_model = LabelsDBModel(labels=labels)
#         else:
#             labels_model = None
#         return labels_model
#     # Special handling for tags
#     if related_sqlalchemy_model == TagsDBModel:
#         tags = []
#         scan_tags = []
#         if "tags" in dictionary:
#             scan_tags = dictionary["tags"]
#         elif "tag_list" in dictionary:
#             scan_tags = dictionary["tag_list"]
#         for tag in scan_tags:
#             tag_model = TagDBModel(**tag)
#             print(f"\n\nTAG MODEL: {tag_model}")
#             session.add(tag_model)
#             tags.append(tag_model)
#         if tags:
#             tags_model = TagsDBModel(tags=tags)
#             session.add(tags_model)
#         else:
#             tags_model = None
#         return tags_model
#     if related_sqlalchemy_model == CommitDBModel:
#         parent_ids = []
#         for parent_id in dictionary["parent_ids"]["parent_ids"]:
#             parent_id_model = ParentIDDBModel(**parent_id)
#             parent_ids.append(parent_id_model)
#             session.add(parent_id_model)
#         if parent_ids:
#             parent_ids_model = ParentIDsDBModel(parent_ids=parent_ids)
#             session.add(parent_ids_model)
#         else:
#             parent_ids_model = None
#         dictionary.pop("parent_ids", None)
#         dictionary.pop("trailers", None)
#         dictionary.pop("extended_trailers", None)
#         setattr(related_sqlalchemy_model, "parent_ids", parent_ids_model)
#     if related_sqlalchemy_model == ArtifactsDBModel:
#         artifacts = []
#         for artifact in dictionary["artifacts"]:
#             artifacts.append(ArtifactDBModel(**artifact))
#         if artifacts:
#             artifacts_model = ArtifactsDBModel(artifacts=artifacts)
#         else:
#             artifacts_model = None
#         return artifacts_model
#     value = remove_none_values(dictionary)
#     print(f"\n\nSetting Nested Model ({related_sqlalchemy_model}): {value}")
#     nested_model = related_sqlalchemy_model(**value)
#     print(f"\n\nObtained Nested Model: {nested_model}")
#     related_model = pydantic_to_sqlalchemy(pydantic_model=nested_model, session=session)
#     print(f"\n\nDefined SQLAlchemy: {related_model}")
#     return related_model
#
#
# def pydantic_to_sqlalchemy(pydantic_model, session):
#     # Check if the model is already converted by ensuring the model doesn't have Meta pydantic field,
#     # but does have base_type sqlalchemy field.
#     if (
#         not hasattr(pydantic_model, "Meta")
#         or not hasattr(pydantic_model.Meta, "orm_model")
#     ) and hasattr(pydantic_model, "base_type"):
#         sqlalchemy_instance = pydantic_model
#         print(f"\n\nFound SQLAlchemy Model on First Try: {sqlalchemy_instance}")
#         return sqlalchemy_instance
#     sqlalchemy_model = pydantic_model.Meta.orm_model
#     sqlalchemy_instance = sqlalchemy_model()
#     for key, value in pydantic_model.model_dump(exclude_unset=True).items():
#         if value:
#             new_model = validate(
#                 key=key, value=value, sqlalchemy_model=sqlalchemy_model, session=session
#             )
#             setattr(sqlalchemy_instance, key, new_model)
#             session.commit()
#
#     print(f"\n\nCompleted Conversion for: {sqlalchemy_instance}")
#     return sqlalchemy_instance
#
#
# def upsert(session, response):
#     items = None
#     for attribute_name in dir(response.data):
#         if attribute_name.startswith("_"):
#             continue
#         attribute_value = getattr(response.data, attribute_name)
#
#         if isinstance(attribute_value, list):
#             items = attribute_value
#
#         # TESTING THIS VERSION UNCOMMENT TOP TWO LINES FOR WORKING
#         #if isinstance(attribute_value, list):
#         # items = attribute_value
#     for item in items:
#         print(f"Item: \n{item}\n\n")
#         db_model = pydantic_to_sqlalchemy(pydantic_model=item, session=session)
#         upsert_row(db_model=db_model, session=session)
#     print("Items Added\n\nCommitting Session...")
#     session.commit()
#
#
# def upsert_row(session, db_model, processed_models=None):
#     if db_model is None:
#         return None
#
#     if processed_models is None:
#         processed_models = set()
#
#     model_type = type(db_model)
#     model_identifier = (model_type, db_model.id)
#     print(f"\n\nSearching for {db_model.id} in {model_type}")
#
#     if model_identifier in processed_models:
#         return None
#
#     processed_models.add(model_identifier)
#
#     # Function to upsert nested models
#     def upsert_nested_models(session, db_model):
#         related_models = []
#         for relation in db_model.__mapper__.relationships:
#             related_model = getattr(db_model, relation.key)
#             if isinstance(related_model, InstrumentedList):
#                 for item in related_model:
#                     if item is not None:
#                         related_models.append(item)
#             elif isinstance(related_model, AppenderQuery):
#                 pass
#             elif related_model is not None:
#                 related_models.append(related_model)
#
#         # Recursively upsert nested models first
#         for related_model in related_models:
#             upsert_row(
#                 session=session,
#                 db_model=related_model,
#                 processed_models=processed_models,
#             )
#
#     # Upsert nested models first
#     upsert_nested_models(session, db_model)
#
#     try:
#         existing_model = session.merge(db_model)
#         session.commit()
#         print("Committed Session!")
#         return existing_model
#     except Exception as e:
#         session.rollback()
#         print(
#             f"Error inserting/updating {model_type.__name__} with ID {db_model.id}: {e}"
#         )


def is_pydantic(obj: object):
    """Checks whether an object is pydantic."""
    if hasattr(obj, "Meta") and hasattr(obj.Meta, "orm_model"):
        print(f"\nPydantic True for {obj}")
        return True
    else:
        print(f"\nPydantic False for {obj}")
        return False


# def parse_schema(schema):
#     parsed_schema = schema.model_dump(exclude_unset=True)
#     print(f"\n\nPARSE SINGLE SCHEMA: {parsed_schema} for {schema.__class__.__name__}")
#     for key, value in iter(parsed_schema):
#         try:
#             if isinstance(value, list) and len(value):
#                 if is_pydantic(value[0]):
#                     print(f"\n\nValidating List: {value}")
#                     parsed_schema[key] = [schema.Meta.orm_model(**parsed_schema) for schema in value]
#             else:
#                 if is_pydantic(value):
#                     print(f"\n\nValidating Dict: {value}")
#                     parsed_schema[key] = value.Meta.orm_model(**value.model_dump(exclude_unset=True))
#         except AttributeError:
#             raise AttributeError("Found nested Pydantic model but Meta.orm_model was not specified.")
#     return parsed_schema


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
        print(f"KEY: {key} VALUE: {value}")
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                print(f"\n\nUpdating: {key} {parsed_schema[key]}")
                for item in value:
                    parsed_schema[key] = [
                        item.Meta.orm_model(**pydantic_to_sqlalchemy(item))
                        for item in value
                        if value is not None
                    ]
                print(f"Updated: {key} {parsed_schema[key]}")
            elif is_pydantic(value):
                parsed_schema[key] = value.Meta.orm_model(
                    **pydantic_to_sqlalchemy(value)
                )
        except AttributeError:
            raise AttributeError(
                f"Found nested Pydantic model in {schema.__class__} but Meta.orm_model was not specified."
            )
    return parsed_schema


# def pydantic_to_sqlalchemy(schema):
#     """
#         Iterates through pydantic schema and parses nested schemas
#         to a dictionary containing SQLAlchemy models.
#         Only works if nested schemas have specified the Meta.orm_model.
#     """
#     print(f"\n\nSCHEMA: {schema}")
#     parsed_schemas = []
#     if isinstance(schema, list):
#         for single_schema in schema:
#             parsed_schemas.append(parse_schema(schema=single_schema))
#     else:
#         parsed_schemas.append(parse_schema(schema=schema))
#     print(f"\n\nPARSED SCHEMAS: {parsed_schemas}")
#     return parsed_schemas


def upsert(model: Any, session):
    if isinstance(model, list):
        for item in model:
            session.add(item)
    else:
        session.add(model)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error inserting/updating {model.__name__} with ID {model.id}: {e}")


# def upsert(model: Any, session, indent: int = 0):
#     if isinstance(model, BaseModel):
#         fields = model.model_fields.keys()
#         for field in fields:
#             value = getattr(model, field)
#             if value:
#                 upsert(value, indent + 2)
#         # Print the current object after its fields have been printed
#         print(f"{' ' * indent}{model}")
#     elif isinstance(model, list):
#         for item in model:
#             upsert(item, indent + 2)
#     else:
#         # Print the leaf node (non-BaseModel and non-list value)
#         sqlalchemy_model = pydantic_to_sqlalchemy(schema=model)
#         #session.add(sqlalchemy_model)
#         print(f"{' ' * indent}{model}")
#     #session.commit()


def create_table(db_instance, engine):
    inspector = reflection.Inspector.from_engine(engine)
    table_name = db_instance.__table__.name

    if not inspector.has_table(table_name):
        db_instance.__table__.create(engine)
        print(f"Table {table_name} created.")
    else:
        print(f"Table {table_name} already exists.")
