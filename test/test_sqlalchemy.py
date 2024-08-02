#!/usr/bin/python

import gitlab_api
from gitlab_api.utils import upsert
from gitlab_api.gitlab_db_models import BaseDBModel
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


def get_users():
    response = client.get_users()
    print(
        f"Users Fetched - Status: {response.status_code}\n\n"
        f"Inserting Data Into Database..."
    )
    upsert(session=session, response=response)
    print("Users Synchronization Complete!")


def get_namespaces():
    response = client.get_namespaces()
    print(f"RESPONSE : {response}")
    print(f"RESPONSE DATA: {response.data}")
    print(
        f"Namespaces Fetched - Status: {response.status_code}\n\n"
        f"Inserting Data Into Database..."
    )
    upsert(session=session, response=response)
    print("Namespaces Synchronization Complete!")


def get_projects():
    response = client.get_projects()
    print(
        f"Projects Fetched - Status: {response.status_code}\n\n"
        f"Inserting Data Into Database..."
    )
    upsert(session=session, response=response)
    print("Projects Synchronization Complete!")


def get_merge_requests():
    response = client.get_group_merge_requests(argument="state=all", group_id=2)
    print(
        f"Merge Requests Fetched - Status: {response.status_code}\n\n"
        f"Inserting Data Into Database..."
    )
    upsert(session=session, response=response)
    print("Merge Request Synchronization Complete!")


if __name__ == "__main__":
    print("Creating GitLab Client...")
    client = gitlab_api.Api(
        url="http://gitlab.arpa/api/v4/",
        token=gitlab_token,
        verify=False,
    )
    print("GitLab Client Created\n\nCreating Engine")

    engine = create_engine(
        f"postgresql://{postgres_username}:{quote_plus(postgres_password)}@"
        f"{postgres_db_host}:{postgres_port}/{postgres_db_name}"
    )

    print("Engine Created\n\nCreating Tables...")

    BaseDBModel.metadata.create_all(engine)

    print("Tables Created\n\nCreating Session...")

    Session = sessionmaker(bind=engine)
    session = Session()
    print("Session Created\n\nFetching GitLab Data...")
    # get_users()
    # get_namespaces()
    # get_projects()
    get_merge_requests()
