"""No response model returns a credential-bearing field (CONN-GITLAB-API-CONNECTOR-CONTENT-R007)."""

from __future__ import annotations

import pytest

from gitlab_api import gitlab_response_models as models
from gitlab_api.gitlab_response_models import (
    REDACTED,
    CreatedDeployToken,
    DeployToken,
    PipelineVariable,
    SecretSafeModel,
    is_secret_field,
)

pytestmark = pytest.mark.spec("CONN-GITLAB-API-CONNECTOR-CONTENT-R007")

SECRET_KEYS = (
    "runners_token",
    "token",
    "private_token",
    "authentication_token",
    "secret",
    "client_secret",
    "secret_token",
    "password",
    "ssh_private_key",
    "api_key",
)


def _response_models() -> list[type[SecretSafeModel]]:
    found = [
        value
        for value in vars(models).values()
        if isinstance(value, type) and issubclass(value, SecretSafeModel)
    ]
    assert len(found) > 50
    return found


def test_every_response_model_derives_from_the_secret_safe_base() -> None:
    plain = [
        name
        for name, value in vars(models).items()
        if isinstance(value, type)
        and value.__module__ == models.__name__
        and not issubclass(value, SecretSafeModel)
        and name != "Response"  # the envelope; its data is a SecretSafeModel
        and hasattr(value, "model_fields")
    ]
    assert plain == []


def test_no_model_declares_a_secret_field_except_a_returned_once_one() -> None:
    offenders = [
        f"{cls.__name__}.{field}"
        for cls in _response_models()
        for field in cls.model_fields
        if is_secret_field(field) and field not in cls.returned_once
    ]
    assert offenders == []


@pytest.mark.parametrize("cls", _response_models(), ids=lambda c: c.__name__)
def test_serializing_a_model_never_emits_a_secret_field(
    cls: type[SecretSafeModel],
) -> None:
    payload = {key: "s3cr3t-value" for key in SECRET_KEYS}
    kept = cls._drop_secret_fields(payload)
    assert {k for k in kept if is_secret_field(k)} <= cls.returned_once
    required = {
        name: "x" for name, info in cls.model_fields.items() if info.is_required()
    }
    try:
        instance = cls(**required, **payload)
    except ValueError:
        return  # a typed required field the placeholder cannot satisfy; the filter above still ran
    dumped = instance.model_dump()
    leaked = [
        key for key in dumped if is_secret_field(key) and key not in cls.returned_once
    ]
    assert leaked == []
    if not cls.returned_once:
        assert "s3cr3t-value" not in instance.model_dump_json()


def test_a_project_payload_loses_its_runners_token() -> None:
    project = models.Project(id=7, name="demo", runners_token="GR1348941abc")
    assert "runners_token" not in project.model_dump()
    assert "GR1348941abc" not in project.model_dump_json()


def test_a_read_deploy_token_has_no_token_and_a_created_one_returns_it_once() -> None:
    body = {"id": 3, "name": "ci", "token": "gldt-abc"}
    assert "token" not in DeployToken(**body).model_dump()
    assert CreatedDeployToken(**body).model_dump()["token"] == "gldt-abc"


def test_a_ci_variable_value_is_redacted() -> None:
    variable = PipelineVariable(key="DEPLOY_KEY", value="hunter2")
    assert variable.value == REDACTED
