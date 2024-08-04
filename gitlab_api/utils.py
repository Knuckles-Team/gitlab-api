#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union, List, Any, Dict
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.exc import NoResultFound
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
    )
except ModuleNotFoundError:
    from gitlab_db_models import (
        LabelsDBModel,
        LabelDBModel,
        TagDBModel,
        TagsDBModel,
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


def get_related_model(sqlalchemy_model, key, value):
    """Get the related SQLAlchemy model for a given key."""
    # Handle special cases explicitly
    # if key == "labels":
    #     label_entries = value.get("labels", [])
    #
    #     label_instances = []
    #     for label_entry in label_entries:
    #         label_instance = LabelDBModel(
    #             name=label_entry["name"],
    #             color=label_entry.get(
    #                 "color", "default_color"
    #             ),  # Default color if not provided
    #             text_color=label_entry.get(
    #                 "text_color", "default_text_color"
    #             ),  # Default text color if not provided
    #             description=label_entry.get("description", ""),
    #             description_html=label_entry.get("description_html", ""),
    #             open_issues_count=label_entry.get("open_issues_count", 0),
    #             closed_issues_count=label_entry.get("closed_issues_count", 0),
    #             open_merge_requests_count=label_entry.get(
    #                 "open_merge_requests_count", 0
    #             ),
    #             subscribed=label_entry.get("subscribed", False),
    #             priority=label_entry.get("priority", None),
    #             is_project_label=label_entry.get("is_project_label", True),
    #         )
    #         label_instances.append(label_instance)
    #         labels_collection = LabelsDBModel(
    #             base_type="Labels", labels=label_instances
    #         )
    #     return LabelsDBModel

    # Dynamically determine the related model based on the attribute
    mapper = class_mapper(sqlalchemy_model)
    for prop in mapper.iterate_properties:
        if prop.key == key:
            return prop.mapper.class_
    raise ValueError(f"Unable to find related model for key: {key}")


def validate_list(list_object: List) -> List:
    related_models = [
        (
            pydantic_to_sqlalchemy(item)
            if hasattr(item, "Meta") and hasattr(item.Meta, "orm_model")
            else item
        )
        for item in list_object
    ]
    logging.debug(f"\n\nRelated models: {related_models}")
    return related_models


def validate_dict(dictionary: Dict, parent_key: str, sqlalchemy_model: Any) -> Any:
    related_sqlalchemy_model = None
    mapper = class_mapper(sqlalchemy_model)
    for prop in mapper.iterate_properties:
        if prop.key == parent_key:
            related_sqlalchemy_model = prop.mapper.class_
    if not related_sqlalchemy_model:
        raise ValueError(f"Unable to find related model for key: {parent_key}")
    print(f"\n\nRelated instance: {related_sqlalchemy_model}")
    # Special handling for labels
    if related_sqlalchemy_model == LabelsDBModel:
        labels = []
        for label in dictionary["labels"]:
            labels.append(LabelDBModel(**label))
        labels_model = LabelsDBModel(labels=labels)
        return labels_model
    # Special handling for tags
    if related_sqlalchemy_model == TagsDBModel:
        tags = []
        for tag in dictionary["tags"]:
            tags.append(TagDBModel(**tag))
        tags_model = TagsDBModel(tags=tags)
        return tags_model
    value = remove_none_values(dictionary)
    nested_model = related_sqlalchemy_model(**value)
    logging.debug(f"\n\nObtained Nested Model: {nested_model}")
    related_model = pydantic_to_sqlalchemy(nested_model)
    logging.debug(f"\n\nDefined SQLAlchemy: {related_model}")
    return related_model


def pydantic_to_sqlalchemy(pydantic_model):
    # Check if the model is already converted by ensuring the model doesn't have Meta pydantic field,
    # but does have base_type sqlalchemy field.
    if (
        not hasattr(pydantic_model, "Meta")
        or not hasattr(pydantic_model.Meta, "orm_model")
    ) and hasattr(pydantic_model, "base_type"):
        sqlalchemy_instance = pydantic_model
        logging.debug(f"\n\nFound SQLAlchemy Model on First Try: {sqlalchemy_instance}")
        return sqlalchemy_instance
    sqlalchemy_model = pydantic_model.Meta.orm_model
    sqlalchemy_instance = sqlalchemy_model()
    for key, value in pydantic_model.model_dump(exclude_unset=True).items():
        if value:
            if isinstance(value, list):
                logging.debug(f"\n\nValue that is a list: {value} for key: {key}")
                related_models = validate_list(list_object=value)
                setattr(sqlalchemy_instance, key, related_models)
                logging.debug(f"\n\nSQLAlchemy List Model Set: {related_models}")
            elif isinstance(value, dict):
                print(f"\n\nValue that is a dict: {value} for key: {key}")
                related_model = validate_dict(
                    dictionary=value, parent_key=key, sqlalchemy_model=sqlalchemy_model
                )
                logging.debug(f"\n\nSetting Related Model: {related_model} for {key}")
                setattr(sqlalchemy_instance, key, related_model)
                logging.debug(f"\n\nSQLAlchemy Dict Model Set: {related_model}")
            else:
                logging.debug(f"\n\nImmediately Setting Attribute: {value}")
                setattr(sqlalchemy_instance, key, value)
                logging.debug(f"\n\nImmediately Set Attribute: {value}")

    logging.debug(f"\n\nCompleted Conversion for: {sqlalchemy_instance}")
    return sqlalchemy_instance


def upsert(session, response):
    items = None
    for attribute_name in dir(response.data):
        if attribute_name.startswith("_"):
            continue
        attribute_value = getattr(response.data, attribute_name)
        if isinstance(attribute_value, list):
            items = attribute_value
    for item in items:
        logging.debug(f"Item: \n{item}\n\n")
        db_model = pydantic_to_sqlalchemy(item)
        upsert_row(db_model=db_model, session=session)
    logging.debug("Items Added\n\nCommitting Session...")
    session.commit()


def upsert_row(session, db_model):
    if db_model is None:
        return None
    model_instance_type = type(db_model)
    print(f"\n\nSearching for {db_model.id} in {model_instance_type}")
    try:
        existing_model = (
            session.query(model_instance_type).filter_by(id=db_model.id).first()
        )
        if not existing_model:
            raise NoResultFound
        print(f"\n\nFound Existing Model: {existing_model}")
        for attr, value in db_model.__dict__.items():
            if attr != "_sa_instance_state":
                setattr(existing_model, attr, value)
        print(f"Merged {model_instance_type.__name__} with ID {existing_model.id}")
    except NoResultFound:
        for relation in db_model.__mapper__.relationships:
            related_model = getattr(db_model, relation.key)
            if isinstance(related_model, InstrumentedList):
                for item in related_model:
                    if item is not None:
                        existing_related = session.query(type(item)).get(item.id)
                        if existing_related is None:
                            session.add(item)
                        else:
                            related_model.remove(item)
                            related_model.append(existing_related)
            elif related_model is not None:
                existing_related = session.query(type(related_model)).get(
                    related_model.id
                )
                if existing_related is None:
                    session.add(related_model)
                else:
                    setattr(db_model, relation.key, existing_related)
        # Add the new model instance
        existing_model = db_model
        session.add(existing_model)
        print(
            f"Inserted new {model_instance_type.__name__} with ID {existing_model.id}"
        )

    try:
        session.commit()
        print("Committed Session!")
    except Exception as e:
        session.rollback()
        print(
            f"Error inserting/updating {model_instance_type.__name__} with ID {db_model.id}: {e}"
        )
    return existing_model
