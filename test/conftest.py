import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from gitlab_api.gitlab_db_models import (
    BaseDBModel,
)  # replace 'your_module' with the actual module name

skip_openai = False
skip_redis = False
skip_docker = False
reason = "requested to skip"


# Registers command-line options like '--skip-openai' and '--skip-redis' via pytest hook.
# When these flags are set, it indicates that tests requiring OpenAI or Redis (respectively) should be skipped.
def pytest_addoption(parser):
    parser.addoption(
        "--skip-docker", action="store_true", help="Skip all tests that require docker"
    )


# pytest hook implementation extracting command line args and exposing it globally
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global skip_docker
    skip_docker = config.getoption("--skip-docker", False)


@pytest.fixture(scope="session")
def engine():
    # Use test environment postgres db
    return create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
    )


@pytest.fixture(scope="session")
def tables(engine):
    BaseDBModel.metadata.create_all(engine)
    yield
    BaseDBModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)

    yield Session

    Session.remove()
    transaction.commit()
    # This doesn't work for postgres
    # transaction.rollback()
    connection.close()
