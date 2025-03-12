# GitLab API

![PyPI - Version](https://img.shields.io/pypi/v/gitlab-api)
![PyPI - Downloads](https://img.shields.io/pypi/dd/gitlab-api)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/gitlab-api)
![GitHub forks](https://img.shields.io/github/forks/Knuckles-Team/gitlab-api)
![GitHub contributors](https://img.shields.io/github/contributors/Knuckles-Team/gitlab-api)
![PyPI - License](https://img.shields.io/pypi/l/gitlab-api)
![GitHub](https://img.shields.io/github/license/Knuckles-Team/gitlab-api)

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/gitlab-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Knuckles-Team/gitlab-api)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/Knuckles-Team/gitlab-api)
![GitHub issues](https://img.shields.io/github/issues/Knuckles-Team/gitlab-api)

![GitHub top language](https://img.shields.io/github/languages/top/Knuckles-Team/gitlab-api)
![GitHub language count](https://img.shields.io/github/languages/count/Knuckles-Team/gitlab-api)
![GitHub repo size](https://img.shields.io/github/repo-size/Knuckles-Team/gitlab-api)
![GitHub repo file count (file type)](https://img.shields.io/github/directory-file-count/Knuckles-Team/gitlab-api)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/gitlab-api)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/gitlab-api)

*Version: 1.0.70*

Pythonic GitLab API Library

Includes a large portion of useful API calls to GitLab and SQLAlchemy Models to handle loading API calls directly to a database!

This repository is actively maintained - Contributions are welcome!

Additional Features:
- All responses are returned as native Pydantic models
- Save Pydantic models to pickle files locally
- Easily convert Pydantic to SQLAlchemy models for quick database insertion


### API Calls:
- Branches
- Commits
- Deploy Tokens
- Groups
- Jobs
- Members
- Merge Request
- Merge Request Rules
- Namespaces
- Packages
- Pipeline
- Projects
- Protected Branches
- Releases
- Runners
- Users
- Wiki
- Custom Endpoint

If your API call isn't supported, you can always run the standard custom API endpoint function to get/post/put/delete and endpoint


<details>
  <summary><b>Usage:</b></summary>

Using the API directly

```python
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

```

</details>

<details>
  <summary><b>Installation Instructions:</b></summary>

Install Python Package

```bash
python -m pip install gitlab-api
```

</details>

<details>
  <summary><b>Tests:</b></summary>

pre-commit check
```bash
pre-commit run --all-files
```

pytest
```bash
python -m pip install -r test-requirements.txt
pytest ./test/test_gitlab_models.py
```

Full pytests

```bash
rm -rf ./dist/* \
&& python setup.py bdist_wheel --universal \
&& python -m pip uninstall gitlab-api -y \
&& python -m pip install  ./dist/*.whl \
&& pytest -vv ./test/test_gitlab_models.py \
&& pytest -vv ./test/test_gitlab_db_models.py \
&& python ./test/test_sqlalchemy.py
```
</details>


<details>
  <summary><b>Repository Owners:</b></summary>


<img width="100%" height="180em" src="https://github-readme-stats.vercel.app/api?username=Knucklessg1&show_icons=true&hide_border=true&&count_private=true&include_all_commits=true" />

![GitHub followers](https://img.shields.io/github/followers/Knucklessg1)
![GitHub User's stars](https://img.shields.io/github/stars/Knucklessg1)
</details>
