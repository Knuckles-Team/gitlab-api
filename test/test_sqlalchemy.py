#!/usr/bin/python

import gitlab_api
from gitlab_api.utils import pydantic_to_sqlalchemy
from gitlab_api.gitlab_db_models import BaseDBModel as Base
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

    print("Fetching GitLab Data...")
    # User Data table is a dependency table
    user_response = client.get_users()
    user_db_model = pydantic_to_sqlalchemy(schema=user_response.data)
    print(
        f"Users ({len(user_response.data.users)}) Fetched - "
        f"Status: {user_response.status_code}\n"
    )

    # Namespaces table is a dependency table
    namespace_response = client.get_namespaces()
    namespace_model = pydantic_to_sqlalchemy(schema=namespace_response.data)
    print(
        f"Namespaces ({len(namespace_response.data.namespaces)}) Fetched - "
        f"Status: {namespace_response.status_code}\n"
    )

    # Project table requires Users and Namespaces
    project_response = client.get_nested_projects_by_group(group_id=2, per_page=100)
    project_db_model = pydantic_to_sqlalchemy(schema=project_response.data)
    print(
        f"Projects ({len(project_response.data.projects)}) Fetched - "
        f"Status: {project_response.status_code}\n"
    )
    print(f"Project DB Model: {project_db_model}")

    # Merge Requests table requires Users, Namespaces, and Projects
    merge_request_response = client.get_group_merge_requests(
        argument="state=all", group_id=2
    )
    merge_request_db_model = pydantic_to_sqlalchemy(schema=merge_request_response.data)
    print(
        f"Merge Requests ({len(merge_request_response.data.merge_requests)}) Fetched - "
        f"Status: {merge_request_response.status_code}\n\n"
    )

    pipeline_db_models = []
    for project in project_response.data.projects:
        pipeline_job_response = client.get_project_jobs(project_id=project.id)
        pipeline_db_model = pydantic_to_sqlalchemy(schema=pipeline_job_response.data)
        pipeline_db_models.extend(pipeline_db_model)
        print(
            f"Pipeline Jobs ({len(pipeline_job_response.data.jobs)}) Fetched for Project ({project.id}) - "
            f"Status: {pipeline_job_response.status_code}\n\n"
        )
        break

    # print("Inserting Users Into Database...")
    # upsert(session=session, model=user_db_model)
    # print("Users Synchronization Complete!\n")

    # print("Inserting Namespaces Into Database...")
    # upsert(session=session, model=namespace_db_model)
    # print("Namespaces Synchronization Complete!\n")
    #
    # print("Inserting Projects Into Database...\n")
    # upsert(session=session, model=project_db_model)
    # print("Projects Synchronization Complete!\n")
    # #
    # print("Inserting Merge Requests Into Database...")
    # upsert(session=session, model=merge_request_response.data)
    # print("Merge Request Synchronization Complete!\n")

    # print(f"Inserting ({len(pipeline_job_responses)}) Pipeline Jobs Into Database...")
    # for pipeline_job_response in pipeline_job_responses:
    #     upsert(session=session, response=pipeline_job_response.data)
    # print("Pipeline Jobs Synchronization Complete!\n\n\n")

    session.close()
    print("Session Closed")
