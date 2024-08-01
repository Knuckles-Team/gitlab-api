#!/usr/bin/python
# coding: utf-8
import logging
from typing import Union, List, Any, Dict
from sqlalchemy.orm import class_mapper
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
        LabelsDBModel, LabelDBModel,
)
except ModuleNotFoundError:
    from gitlab_db_models import (
        LabelsDBModel, LabelDBModel,
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
    if key == 'labels':
        label_entries = value.get('labels', [])

        label_instances = []
        for label_entry in label_entries:
            label_instance = LabelDBModel(
                name=label_entry['name'],
                color=label_entry.get('color', 'default_color'),  # Default color if not provided
                text_color=label_entry.get('text_color', 'default_text_color'),  # Default text color if not provided
                description=label_entry.get('description', ''),
                description_html=label_entry.get('description_html', ''),
                open_issues_count=label_entry.get('open_issues_count', 0),
                closed_issues_count=label_entry.get('closed_issues_count', 0),
                open_merge_requests_count=label_entry.get('open_merge_requests_count', 0),
                subscribed=label_entry.get('subscribed', False),
                priority=label_entry.get('priority', None),
                is_project_label=label_entry.get('is_project_label', True)
            )
            label_instances.append(label_instance)
            labels_collection = LabelsDBModel(base_type="Labels", labels=label_instances)
        return LabelsDBModel

    # Dynamically determine the related model based on the attribute
    mapper = class_mapper(sqlalchemy_model)
    for prop in mapper.iterate_properties:
        if prop.key == key:
            return prop.mapper.class_
    raise ValueError(f"Unable to find related model for key: {key}")


# def pydantic_to_sqlalchemy(pydantic_model):
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
#         if isinstance(value, list):
#             if len(value) > 0:
#                 print(f"\n\nValue that is a list: {value} for key: {key}")
#                 related_instances = [
#                     (
#                         pydantic_to_sqlalchemy(item)
#                         if hasattr(item, "Meta") and hasattr(item.Meta, "orm_model")
#                         else item
#                     )
#                     for item in value
#                 ]
#                 print(f"\n\nRelated instances: {related_instances}")
#                 setattr(sqlalchemy_instance, key, related_instances)
#         elif isinstance(value, dict):
#             print(f"\n\nValue that is a dict: {value} for key: {key}")
#             related_sqlalchemy_model = get_related_model(sqlalchemy_model, key, value)
#             print(f"\n\nRelated instance: {related_sqlalchemy_model}")
#             value = remove_none_values(value)
#             nested_model = related_sqlalchemy_model(**value)
#             print(f"\n\nObtained Nested Model: {nested_model}")
#             related_instance = pydantic_to_sqlalchemy(nested_model)
#             print(f"\n\nDefined SQLAlchemy: {related_instance}")
#             setattr(sqlalchemy_instance, key, related_instance)
#             print(f"\n\nSQLAlchemy Model Set: {related_instance}")
#         else:
#             if value:
#                 print(f"\n\nImmediately Setting Attribute: {value}")
#                 setattr(sqlalchemy_instance, key, value)
#                 print(f"\n\nImmeidately Set Attribute: {value}")
#
#     print(f"\n\nCompleted Conversion for: {sqlalchemy_instance}")
#     return sqlalchemy_instance


def validate_list(list_object: List) -> List:
    related_models = [
        pydantic_to_sqlalchemy(item)
        if hasattr(item, "Meta") and hasattr(item.Meta, "orm_model")
        else item
        for item in list_object
    ]
    print(f"\n\nRelated models: {related_models}")
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
        for label in dictionary['labels']:
            labels.append(LabelDBModel(**label))
        labels_model = LabelsDBModel(labels=labels)
        return labels_model
    value = remove_none_values(dictionary)
    nested_model = related_sqlalchemy_model(**value)
    print(f"\n\nObtained Nested Model: {nested_model}")
    related_model = pydantic_to_sqlalchemy(nested_model)
    print(f"\n\nDefined SQLAlchemy: {related_model}")
    return related_model


def pydantic_to_sqlalchemy(pydantic_model):
    # Check if the model is already converted by ensuring the model doesn't have Meta pydantic field,
    # but does have base_type sqlalchemy field.
    if (
            not hasattr(pydantic_model, "Meta")
            or not hasattr(pydantic_model.Meta, "orm_model")
    ) and hasattr(pydantic_model, "base_type"):
        sqlalchemy_instance = pydantic_model
        print(f"\n\nFound SQLAlchemy Model on First Try: {sqlalchemy_instance}")
        return sqlalchemy_instance
    sqlalchemy_model = pydantic_model.Meta.orm_model
    sqlalchemy_instance = sqlalchemy_model()
    for key, value in pydantic_model.model_dump(exclude_unset=True).items():
        if value:
            if isinstance(value, list):
                print(f"\n\nValue that is a list: {value} for key: {key}")
                related_models = validate_list(list_object=value)
                setattr(sqlalchemy_instance, key, related_models)
                print(f"\n\nSQLAlchemy Model Set: {related_models}")
            elif isinstance(value, dict):
                print(f"\n\nValue that is a dict: {value} for key: {key}")
                related_model = validate_dict(dictionary=value, parent_key=key, sqlalchemy_model=sqlalchemy_model)
                setattr(sqlalchemy_instance, key, related_model)
                print(f"\n\nSQLAlchemy Model Set: {related_model}")
            else:
                print(f"\n\nImmediately Setting Attribute: {value}")
                setattr(sqlalchemy_instance, key, value)
                print(f"\n\nImmediately Set Attribute: {value}")

    print(f"\n\nCompleted Conversion for: {sqlalchemy_instance}")
    return sqlalchemy_instance
