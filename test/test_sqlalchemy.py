#!/usr/bin/python

import gitlab_api
from gitlab_api import pydantic_to_sqlalchemy, upsert, save_model, load_model
from gitlab_api.gitlab_db_models import (
    BaseDBModel as Base,
)
import urllib3
import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

gitlab_token = os.environ["GITLAB_TOKEN"]
postgres_username = os.environ["POSTGRES_USERNAME"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_db_host = os.environ["POSTGRES_DB_HOST"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_db_name = os.environ["POSTGRES_DB_NAME"]


if __name__ == "__main__":
    print("Creating GitLab Client...")
    client = gitlab_api.Api(
        url="http://gitlab.arpa/api/v4/",
        token=gitlab_token,
        verify=False,
    )
    print("GitLab Client Created\n\n")

    print("\nFetching User Data...")
    user_response = client.get_users(active=True, humans=True)
    print(
        f"Users ({len(user_response.data)}) Fetched - "
        f"Status: {user_response.status_code}\n"
    )

    print("\nFetching Namespace Data...")
    namespace_response = client.get_namespaces()
    print(
        f"Namespaces ({len(namespace_response.data)}) Fetched - "
        f"Status: {namespace_response.status_code}\n"
    )

    print("\nFetching Project Data...")
    project_response = client.get_nested_projects_by_group(group_id=2, per_page=100)
    print(
        f"Projects ({len(project_response.data)}) Fetched - "
        f"Status: {project_response.status_code}\n"
    )

    print("\nFetching Merge Request Data...")
    merge_request_response = client.get_group_merge_requests(
        argument="state=all", group_id=2
    )

    print(
        f"\nMerge Requests ({len(merge_request_response.data)}) Fetched - "
        f"Status: {merge_request_response.status_code}\n"
    )

    # Pipeline Jobs table
    pipeline_job_response = None
    for project in project_response.data:
        job_response = client.get_project_jobs(project_id=project.id)
        if (
            not pipeline_job_response
            and hasattr(job_response, "data")
            and len(job_response.data) > 0
        ):
            pipeline_job_response = job_response
        elif (
            pipeline_job_response
            and hasattr(job_response, "data")
            and len(job_response.data) > 0
        ):
            pipeline_job_response.data.extend(job_response.data)
            print(
                f"Pipeline Jobs ({len(getattr(pipeline_job_response, 'data', []))}) "
                f"Fetched for Project ({project.id}) - "
                f"Status: {pipeline_job_response.status_code}\n"
            )

    print("Saving Pydantic Models...")
    user_file = save_model(model=user_response, file_name="user_model", file_path=".")
    namespace_file = save_model(
        model=namespace_response, file_name="namespace_model", file_path="."
    )
    project_file = save_model(
        model=project_response, file_name="project_model", file_path="."
    )
    merge_request_file = save_model(
        model=merge_request_response, file_name="merge_request_model", file_path="."
    )
    pipeline_job_file = save_model(
        model=pipeline_job_response, file_name="pipeline_job_model", file_path="."
    )
    print("Models Saved")

    print("Loading Pydantic Models...")
    user_response = load_model(file=user_file)
    namespace_response = load_model(file=namespace_file)
    project_response = load_model(file=project_file)
    merge_request_response = load_model(file=merge_request_file)
    pipeline_job_response = load_model(file=pipeline_job_file)
    print("Models Loaded")

    print("Converting Pydantic to SQLAlchemy model...")
    user_db_model = pydantic_to_sqlalchemy(schema=user_response)
    print(f"Database Models: {user_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    namespace_db_model = pydantic_to_sqlalchemy(schema=namespace_response)
    print(f"Database Models: {namespace_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    project_db_model = pydantic_to_sqlalchemy(schema=project_response)
    print(f"Database Models: {project_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    merge_request_db_model = pydantic_to_sqlalchemy(schema=merge_request_response)
    print(f"Database Models: {merge_request_db_model}\n")

    print("Converting Pydantic to SQLAlchemy model...")
    pipeline_db_model = pydantic_to_sqlalchemy(schema=pipeline_job_response)
    print(f"Database Models: {pipeline_db_model}\n")

    print("Creating Engine")
    engine = create_engine(
        f"postgresql://{postgres_username}:{quote_plus(postgres_password)}@"
        f"{postgres_db_host}:{postgres_port}/{postgres_db_name}"
    )
    print("Engine Created\n\n")

    print("Creating Tables...")
    Base.metadata.create_all(engine)
    print("Tables Created\n\n")

    print("Creating Session...")
    Session = sessionmaker(bind=engine)
    session = Session()
    print("Session Created\n\n")

    print(f"Inserting ({len(user_response.data)}) Users Into Database...")
    upsert(session=session, model=user_db_model)
    print("Users Synchronization Complete!\n")

    print(f"Inserting ({len(namespace_response.data)}) Namespaces Into Database...")
    upsert(session=session, model=namespace_db_model)
    print("Namespaces Synchronization Complete!\n")

    print(f"Inserting ({len(project_response.data)}) Projects Into Database...\n")
    upsert(session=session, model=project_db_model)
    print("Projects Synchronization Complete!\n")

    print(
        f"Inserting ({len(merge_request_response.data)}) Merge Requests Into Database..."
    )
    upsert(session=session, model=merge_request_db_model)
    print("Merge Request Synchronization Complete!\n")

    print(
        f"Inserting ({len(pipeline_job_response.data)}) Pipeline Jobs Into Database..."
    )
    upsert(session=session, model=pipeline_db_model)
    print("Pipeline Jobs Synchronization Complete!\n")

    session.close()
    print("Session Closed")
