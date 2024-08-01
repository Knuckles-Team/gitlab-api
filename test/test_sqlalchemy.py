#!/usr/bin/python

import gitlab_api
from gitlab_api.utils import pydantic_to_sqlalchemy
from gitlab_api.gitlab_db_models import BaseDBModel, UserDBModel, MergeRequestDBModel
import urllib3
import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

gitlab_token = os.environ["GITLAB_TOKEN"]
postgres_username = os.environ["POSTGRES_USERNAME"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_db_host = os.environ["POSTGRES_DB_HOST"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_db_name = os.environ["POSTGRES_DB_NAME"]


# def insert_or_update(db_model):
#     # Check if the user with the given ID already exists
#     print(f"\n\nINSERTING FUNCTION: {db_model}")
#     model_instance = type(db_model)
#     print(f"\n\nDB_ID: {db_model.id}")
#     item = session.query(model_instance).filter_by(id=db_model.id).first()
#     print(f"\n\nITEM: {item}")
#     if item:
#         # If the user exists, update its fields
#         print(f"Updated item with ID {db_model.id}")
#     else:
#         # If the user does not exist, create a new record
#         session.add(db_model)
#         print(f"Inserted new item with ID {db_model.id}")
#
#     # Commit the transaction
#     session.commit()

# def insert_or_update_user(user_data):
#     if user_data is None:
#         return None
#
#     user = session.query(UserDBModel).filter_by(id=user_data.id).first()
#
#     if user:
#         for attr, value in merge_request.__dict__.items():
#             if attr != "_sa_instance_state":
#                 setattr(user, attr, value)
#         print(f"Updated user with ID {user.id}")
#     else:
#         user = user_data
#         session.add(user)
#         print(f"Inserted new user with ID {user.id}")
#     session.commit()
#     return user

def insert_or_update(db_model):
    if db_model is None:
        return None
    model_instance = type(db_model)
    print(f"\n\nSearching for {db_model.id}")
    existing_model = session.query(model_instance).filter_by(id=db_model.id).first()
    print(f"\n\nFound Existing Model: {existing_model}")
    if existing_model:
        for attr, value in db_model.__dict__.items():
            if attr != "_sa_instance_state":
                setattr(existing_model, attr, value)
        print(f"Updated {model_instance} with ID {existing_model.id}")
    else:
        existing_model = db_model
        session.add(existing_model)
        print(f"Inserted new {model_instance} with ID {existing_model.id}")
    session.commit()
    return existing_model


def insert_or_update_merge_request(merge_request):
    # Handle User instances
    merge_request.merged_by = insert_or_update(merge_request.merged_by)
    merge_request.merge_user = insert_or_update(merge_request.merge_user)
    merge_request.author = insert_or_update(merge_request.author)
    merge_request.project = insert_or_update(merge_request.project)

    # Check if the merge request already exists
    existing_merge_request = session.query(MergeRequestDBModel).filter_by(id=merge_request.id).first()

    if existing_merge_request:
        # Update existing merge request
        for attr, value in merge_request.__dict__.items():
            if attr != "_sa_instance_state":
                setattr(existing_merge_request, attr, value)
        print(f"Updated merge request with ID {merge_request.id}")
    else:
        # Create a new merge request
        session.add(merge_request)
        print(f"Inserted new merge request with ID {merge_request.id}")

    # Commit the transaction
    session.commit()


if __name__ == "__main__":
    print(f"Creating GitLab Client...")
    client = gitlab_api.Api(
        url="http://gitlab.arpa/api/v4/", token = gitlab_token, verify=False,
    )
    print(f"GitLab Client Created\n\nCreating Engine")

    engine = create_engine(f"postgresql://{postgres_username}:{quote_plus(postgres_password)}@"
                           f"{postgres_db_host}:{postgres_port}/{postgres_db_name}")

    print(f"Engine Created\n\nCreating Tables...")

    BaseDBModel.metadata.create_all(engine)

    print("Tables Created\n\nCreating Session...")

    Session = sessionmaker(bind=engine)
    session = Session()
    print(f"Session Created\n\nFetching GitLab Data...")

    response = client.get_group_merge_requests(argument="state=all",
                                               group_id=2)
    print(f"Merge Requests Fetched - Status: {response.status_code}\n\n"
          f"Inserting Data Into Database...")

    for merge_request in response.data.merge_requests:
        print(f"Merge Request: \n{merge_request}\n\n")
        merge_request_db_model = pydantic_to_sqlalchemy(merge_request)
        insert_or_update_merge_request(merge_request=merge_request_db_model)

    print("Merge Requests Added\n\nCommitting Session...")
    session.commit()

    print("Merge Request Synchronization Complete!")