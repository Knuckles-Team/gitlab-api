#!/usr/bin/python
# coding: utf-8
import logging
import os
import pickle
from typing import Union, Any
from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import reflection
import requests
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.orm import sessionmaker

from gitlab_api.gitlab_response_models import Response


def process_response(response: requests.Response) -> Union[Response, requests.Response]:
    try:
        response.raise_for_status()
    except Exception as response_error:
        logging.error(f"Response Error: {response_error}")
    try:
        status_code = response.status_code
    except Exception as e:
        status_code = None
        logging.error(f"Unable to get status code: {e}")
    try:
        raw_output = response.content
    except Exception as e:
        raw_output = None
        logging.error(f"Unable to get raw output: {e}")
    try:
        headers = response.headers
    except Exception as e:
        headers = {}
        logging.error(f"Unable to get headers: {e}")
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


def process_list_item(item):
    """Helper function to process a single item in a list."""
    new_schema = pydantic_to_sqlalchemy(item)
    return item.Meta.orm_model(**new_schema)


def pydantic_to_sqlalchemy(schema, max_workers: int = 6):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = remove_none_values(dict(schema))
    logging.debug(f"\n\nCleaned Schema: {parsed_schema}")
    if not parsed_schema:
        return parsed_schema

    for key, value in parsed_schema.items():
        if not value:
            continue
        try:
            if isinstance(value, list) and value and is_pydantic(value[0]):
                logging.debug(f"\n\nUpdating List: {key} {parsed_schema[key]}")
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    parsed_schemas = list(executor.map(process_list_item, value))
                logging.debug(
                    f"\nNew Schema List Key: {parsed_schema[key]}\nWith Value: {parsed_schemas}"
                )
                parsed_schema[key] = parsed_schemas
            elif is_pydantic(value):
                new_model = value.Meta.orm_model(
                    **pydantic_to_sqlalchemy(value, max_workers)
                )
                logging.debug(
                    f"\n\nNew Schema Dictionary Key: {parsed_schema[key]} With Value: {new_model}"
                )
                parsed_schema[key] = new_model
        except AttributeError as e:
            error_msg = (
                f"Nested Pydantic model in {schema.__class__} lacks Meta.orm_model. \n"
                f"Parsed Schema: {parsed_schema}\n"
                f"Key: {key}, Value: {value}\n"
                f"Error: {e}"
            )
            logging.error(error_msg)
            # try:
            #     pydantic_to_sqlalchemy_fallback(schema=parsed_schema)
            # except AttributeError as e:
            #     error_msg = (f"Fallback Function Failure\n"
            #                  f"Nested Pydantic model in {schema.__class__} lacks Meta.orm_model. \n"
            #                  f"Parsed Schema: {parsed_schema}\n"
            #                  f"Key: {key}, Value: {value}\n"
            #                  f"Error: {e}")
            #     logging.error(error_msg)
            #     raise ValueError(error_msg)
            raise ValueError(error_msg)
    logging.debug(f"\nReturned Parsed Schema: {parsed_schema}")
    return parsed_schema


def pydantic_to_sqlalchemy_fallback(schema):
    """
    Iterates through pydantic schema and parses nested schemas
    to a dictionary containing SQLAlchemy models.
    Only works if nested schemas have specified the Meta.orm_model.
    """
    parsed_schema = dict(schema)
    parsed_schema = remove_none_values(dictionary=parsed_schema)

    logging.debug(f"\n\nCleaned Schema: {parsed_schema}")
    for key, value in parsed_schema.items():
        if not value:
            continue
        try:
            if isinstance(value, list) and len(value) and is_pydantic(value[0]):
                parsed_schemas = []
                for item in value:
                    new_schema = pydantic_to_sqlalchemy_fallback(item)
                    new_model = item.Meta.orm_model(**new_schema)
                    parsed_schemas.append(new_model)
                    logging.debug(
                        f"\nNew Schema List Key: {parsed_schema[key]}\nWith Value: {parsed_schemas}"
                    )
                parsed_schema[key] = parsed_schemas
            elif is_pydantic(value):
                new_model = value.Meta.orm_model(
                    **pydantic_to_sqlalchemy_fallback(value)
                )
                logging.debug(
                    f"\n\nNew Schema Dictionary Key: {parsed_schema[key]} With Value: {new_model}"
                )
                parsed_schema[key] = new_model
        except AttributeError as e:
            error_msg = (
                f"Fallback Function Failure\n"
                f"Nested Pydantic model in {schema.__class__} lacks Meta.orm_model. \n"
                f"Parsed Schema: {parsed_schema}\n"
                f"Key: {key}, Value: {value}\n"
                f"Error: {e}"
            )
            logging.error(error_msg)
    logging.debug(f"\nFallback Function: Returned Parsed Schema: {parsed_schema}")
    return parsed_schema


def get_related_ids(item):
    """Extract primary and foreign key IDs from any SQLAlchemy model."""
    ids = set()

    # Check if item is a SQLAlchemy model with a mapped table
    if not hasattr(item, "__table__"):
        return ids

    # Use SQLAlchemy inspector to get table metadata
    inspector = inspect(item.__class__)

    # Add primary key
    primary_keys = inspector.primary_key
    for pk in primary_keys:
        pk_value = getattr(item, pk.name, None)
        if pk_value is not None:
            ids.add((item.__class__.__name__, pk_value))

    # Add foreign key IDs
    for column in inspector.columns.values():
        if column.foreign_keys:  # Check if column is a foreign key
            fk_value = getattr(item, column.name, None)
            if fk_value is not None:
                # Use the target table name as a proxy for the related model
                for fk in column.foreign_keys:
                    target_table = fk.target_fullname.split(".")[
                        1
                    ]  # e.g., "commits" from "public.commits"
                    ids.add((target_table, fk_value))

    return ids


def partition_data(data, num_partitions):
    """Partition data considering IDs of parent and direct foreign keys."""
    item_to_ids = {}
    for item in data:
        related_ids = get_related_ids(item)
        item_to_ids[item] = related_ids

    clusters = {}
    for item, ids in item_to_ids.items():
        key = frozenset(ids)
        clusters.setdefault(key, []).append(item)

    cluster_list = list(clusters.values())
    chunk_size = max(1, len(cluster_list) // num_partitions)
    partitioned_data = [
        sum(cluster_list[i : i + chunk_size], [])
        for i in range(0, len(cluster_list), chunk_size)
    ]

    return partitioned_data


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def upsert_chunk(chunk_data: list, engine_url: str, batch_size: int = 1000):
    """Process a chunk of data with nested models."""
    engine = create_engine(engine_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        if not chunk_data:
            logging.debug("Empty chunk received")
            return

        for i in range(0, len(chunk_data), batch_size):
            batch = chunk_data[i : i + batch_size]
            with session.no_autoflush:
                for item in batch:
                    session.merge(item)  # Merge cascades to nested models
            session.commit()

        logging.debug(f"Processed chunk of {len(chunk_data)} records")
    except Exception as e:
        session.rollback()
        logging.error(f"Error processing chunk: {e}")
        raise
    finally:
        session.close()
        engine.dispose()


def upsert(model: Any, engine, batch_size: int = 1000):
    """Parallelized upsert with nested model support."""
    if not model or "data" not in model:
        logging.debug(f"No data in model: {model}")
        return

    data = model["data"]
    if not data:
        logging.debug("No data to process")
        return

    num_processes = cpu_count()
    logging.info(f"Using {num_processes} processes")

    chunks = partition_data(data, num_processes)
    logging.info(f"Partitioned {len(data)} records into {len(chunks)} chunks")

    engine_url = engine.url.render_as_string(hide_password=False)

    with Pool(processes=num_processes) as pool:
        pool.starmap(
            upsert_chunk, [(chunk, engine_url, batch_size) for chunk in chunks if chunk]
        )

    logging.info(f"Completed upsert of {len(data)} records")


def upsert_fallback(model: Any, engine, batch_size: int = 1000):
    if not model or "data" not in model:
        logging.debug(f"No data in model: {model}")
        return

    data = model["data"]
    item_ids = [item.id for item in data if item.id]

    Session = sessionmaker(bind=engine)
    session = Session()
    existing_items = (
        session.query(data[0].__class__)
        .filter(data[0].__class__.id.in_(item_ids))
        .all()
    )
    existing_items_map = {item.id: item for item in existing_items}
    batch_count = 0
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
        batch_count += 1
        if batch_count >= batch_size:
            session.commit()
            logging.debug(f"Committed batch of {batch_size} records")
            batch_count = 0

    if batch_count > 0:
        session.commit()
        logging.debug(f"Committed final batch of {batch_count} records")


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


def run_migrations(
    config: str = "alembic.ini",
    script_location: str = None,
    migration_message: str = None,
    database_url: str = None,
):
    alembic_cfg = Config(config)

    if script_location:
        alembic_cfg.set_main_option("script_location", script_location)

    engine = create_engine(database_url)

    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        try:
            revision = command.revision(
                alembic_cfg, message=migration_message, autogenerate=True
            )
            print(f"Generated migration: {revision.revision}")
        except Exception as e:
            print(f"Failed to generate migration: {e}")
        try:
            command.upgrade(alembic_cfg, "head")
            print("Migrations applied successfully.")
        except Exception as e:
            print(f"An error occurred during migration: {e}")
