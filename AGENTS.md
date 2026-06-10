# AGENTS.md

> Claude Code loads this file via `CLAUDE.md` (`@AGENTS.md` import) — the two stay
> in sync. Edit **this** file, not `CLAUDE.md`.

## Tech Stack & Architecture
- Language/Version: Python 3.10+
- Core Libraries: `agent-utilities`, `fastmcp`, `pydantic-ai`
- Key principles: Functional patterns, Pydantic for data validation, asynchronous tool execution.
- Architecture:
    - `mcp_server.py`: Main MCP server entry point and tool registration.
    - `agent.py`: Pydantic AI agent definition and logic.
    - `skills/`: Directory containing modular agent skills (if applicable).
    - `agent/`: Internal agent logic and prompt templates.

### Architecture Diagram
```mermaid
graph TD
    User([User/A2A]) --> Server[A2A Server / FastAPI]
    Server --> Agent[Pydantic AI Agent]
    Agent --> Skills[Modular Skills]
    Agent --> MCP[MCP Server / FastMCP]
    MCP --> Client[API Client / Wrapper]
    Client --> ExternalAPI([External Service API])
```

### Workflow Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant S as Server
    participant A as Agent
    participant T as MCP Tool
    participant API as External API

    U->>S: Request
    S->>A: Process Query
    A->>T: Invoke Tool
    T->>API: API Request
    API-->>T: API Response
    T-->>A: Tool Result
    A-->>S: Final Response
    S-->>U: Output
```

## Commands (run these exactly)
# Installation
pip install .[all]

# Quality & Linting (run from project root)
pre-commit run --all-files

# Execution Commands
# gitlab-mcp
gitlab_api.mcp_server:mcp_server
# gitlab-agent
gitlab_api.agent_server:agent_server

## Project Structure Quick Reference
- MCP Entry Point → `mcp_server.py`
- Agent Entry Point → `agent.py`
- Source Code → `gitlab_api/`
- Skills → `skills/` (if exists)

### File Tree
```text
├── .bumpversion.cfg
├── .codespellignore
├── .dockerignore
├── .env
├── .env.example
├── .gitattributes
├── .github
│   └── workflows
│       ├── docs.yml
│       ├── pages.yml
│       └── pipeline.yml
├── .gitignore
├── .mypy_cache
│   ├── .gitignore
│   ├── 3.10
│   │   ├── @plugins_snapshot.json
│   │   ├── __future__.data.json
│   │   ├── __future__.meta.json
│   │   ├── _ast.data.json
│   │   ├── _ast.meta.json
│   │   ├── _asyncio.data.json
│   │   ├── _asyncio.meta.json
│   │   ├── _blake2.data.json
│   │   ├── _blake2.meta.json
│   │   ├── _codecs.data.json
│   │   ├── _codecs.meta.json
│   │   ├── _collections_abc.data.json
│   │   ├── _collections_abc.meta.json
│   │   ├── _contextvars.data.json
│   │   ├── _contextvars.meta.json
│   │   ├── _ctypes.data.json
│   │   ├── _ctypes.meta.json
│   │   ├── _decimal.data.json
│   │   ├── _decimal.meta.json
│   │   ├── _frozen_importlib.data.json
│   │   ├── _frozen_importlib.meta.json
│   │   ├── _frozen_importlib_external.data.json
│   │   ├── _frozen_importlib_external.meta.json
│   │   ├── _hashlib.data.json
│   │   ├── _hashlib.meta.json
│   │   ├── _io.data.json
│   │   ├── _io.meta.json
│   │   ├── _operator.data.json
│   │   ├── _operator.meta.json
│   │   ├── _pickle.data.json
│   │   ├── _pickle.meta.json
│   │   ├── _queue.data.json
│   │   ├── _queue.meta.json
│   │   ├── _random.data.json
│   │   ├── _random.meta.json
│   │   ├── _sitebuiltins.data.json
│   │   ├── _sitebuiltins.meta.json
│   │   ├── _socket.data.json
│   │   ├── _socket.meta.json
│   │   ├── _ssl.data.json
│   │   ├── _ssl.meta.json
│   │   ├── _thread.data.json
│   │   ├── _thread.meta.json
│   │   ├── _typeshed
│   │   ├── _warnings.data.json
│   │   ├── _warnings.meta.json
│   │   ├── _weakref.data.json
│   │   ├── _weakref.meta.json
│   │   ├── _weakrefset.data.json
│   │   ├── _weakrefset.meta.json
│   │   ├── abc.data.json
│   │   ├── abc.meta.json
│   │   ├── annotated_types
│   │   ├── ast.data.json
│   │   ├── ast.meta.json
│   │   ├── asyncio
│   │   ├── base64.data.json
│   │   ├── base64.meta.json
│   │   ├── binascii.data.json
│   │   ├── binascii.meta.json
│   │   ├── builtins.data.json
│   │   ├── builtins.meta.json
│   │   ├── cache.db
│   │   ├── codecs.data.json
│   │   ├── codecs.meta.json
│   │   ├── collections
│   │   ├── colorsys.data.json
│   │   ├── colorsys.meta.json
│   │   ├── concurrent
│   │   ├── contextlib.data.json
│   │   ├── contextlib.meta.json
│   │   ├── contextvars.data.json
│   │   ├── contextvars.meta.json
│   │   ├── copy.data.json
│   │   ├── copy.meta.json
│   │   ├── copyreg.data.json
│   │   ├── copyreg.meta.json
│   │   ├── ctypes
│   │   ├── dataclasses.data.json
│   │   ├── dataclasses.meta.json
│   │   ├── datetime.data.json
│   │   ├── datetime.meta.json
│   │   ├── decimal.data.json
│   │   ├── decimal.meta.json
│   │   ├── dis.data.json
│   │   ├── dis.meta.json
│   │   ├── email
│   │   ├── enum.data.json
│   │   ├── enum.meta.json
│   │   ├── errno.data.json
│   │   ├── errno.meta.json
│   │   ├── fractions.data.json
│   │   ├── fractions.meta.json
│   │   ├── functools.data.json
│   │   ├── functools.meta.json
│   │   ├── genericpath.data.json
│   │   ├── genericpath.meta.json
│   │   ├── gitlab_api
│   │   ├── hashlib.data.json
│   │   ├── hashlib.meta.json
│   │   ├── hmac.data.json
│   │   ├── hmac.meta.json
│   │   ├── http
│   │   ├── importlib
│   │   ├── inspect.data.json
│   │   ├── inspect.meta.json
│   │   ├── io.data.json
│   │   ├── io.meta.json
│   │   ├── ipaddress.data.json
│   │   ├── ipaddress.meta.json
│   │   ├── itertools.data.json
│   │   ├── itertools.meta.json
│   │   ├── json
│   │   ├── keyword.data.json
│   │   ├── keyword.meta.json
│   │   ├── logging
│   │   ├── math.data.json
│   │   ├── math.meta.json
│   │   ├── mimetypes.data.json
│   │   ├── mimetypes.meta.json
│   │   ├── multiprocessing
│   │   ├── numbers.data.json
│   │   ├── numbers.meta.json
│   │   ├── opcode.data.json
│   │   ├── opcode.meta.json
│   │   ├── operator.data.json
│   │   ├── operator.meta.json
│   │   ├── os
│   │   ├── pathlib.data.json
│   │   ├── pathlib.meta.json
│   │   ├── pickle.data.json
│   │   ├── pickle.meta.json
│   │   ├── posixpath.data.json
│   │   ├── posixpath.meta.json
│   │   ├── pydantic
│   │   ├── pydantic_core
│   │   ├── queue.data.json
│   │   ├── queue.meta.json
│   │   ├── random.data.json
│   │   ├── random.meta.json
│   │   ├── re.data.json
│   │   ├── re.meta.json
│   │   ├── requests
│   │   ├── resource.data.json
│   │   ├── resource.meta.json
│   │   ├── select.data.json
│   │   ├── select.meta.json
│   │   ├── selectors.data.json
│   │   ├── selectors.meta.json
│   │   ├── signal.data.json
│   │   ├── signal.meta.json
│   │   ├── socket.data.json
│   │   ├── socket.meta.json
│   │   ├── sre_compile.data.json
│   │   ├── sre_compile.meta.json
│   │   ├── sre_constants.data.json
│   │   ├── sre_constants.meta.json
│   │   ├── sre_parse.data.json
│   │   ├── sre_parse.meta.json
│   │   ├── ssl.data.json
│   │   ├── ssl.meta.json
│   │   ├── string.data.json
│   │   ├── string.meta.json
│   │   ├── subprocess.data.json
│   │   ├── subprocess.meta.json
│   │   ├── sys
│   │   ├── tempfile.data.json
│   │   ├── tempfile.meta.json
│   │   ├── test_gitlab_a2a_validation.data.json
│   │   ├── test_gitlab_a2a_validation.meta.json
│   │   ├── test_gitlab_mcp_validation.data.json
│   │   ├── test_gitlab_mcp_validation.meta.json
│   │   ├── test_setup.data.json
│   │   ├── test_setup.meta.json
│   │   ├── test_verify_agent.data.json
│   │   ├── test_verify_agent.meta.json
│   │   ├── tests
│   │   ├── textwrap.data.json
│   │   ├── textwrap.meta.json
│   │   ├── threading.data.json
│   │   ├── threading.meta.json
│   │   ├── time.data.json
│   │   ├── time.meta.json
│   │   ├── traceback.data.json
│   │   ├── traceback.meta.json
│   │   ├── types.data.json
│   │   ├── types.meta.json
│   │   ├── typing.data.json
│   │   ├── typing.meta.json
│   │   ├── typing_extensions.data.json
│   │   ├── typing_extensions.meta.json
│   │   ├── typing_inspection
│   │   ├── unittest
│   │   ├── urllib
│   │   ├── urllib3
│   │   ├── uuid.data.json
│   │   ├── uuid.meta.json
│   │   ├── validate_a2a_agent.data.json
│   │   ├── validate_a2a_agent.meta.json
│   │   ├── validate_agent.data.json
│   │   ├── validate_agent.meta.json
│   │   ├── verify_a2a_queries.data.json
│   │   ├── verify_a2a_queries.meta.json
│   │   ├── warnings.data.json
│   │   ├── warnings.meta.json
│   │   ├── weakref.data.json
│   │   ├── weakref.meta.json
│   │   ├── zipfile
│   │   ├── zlib.data.json
│   │   ├── zlib.meta.json
│   │   └── zoneinfo
│   ├── 3.13
│   │   ├── @plugins_snapshot.json
│   │   ├── __future__.data.json
│   │   ├── __future__.meta.json
│   │   ├── _ast.data.json
│   │   ├── _ast.meta.json
│   │   ├── _asyncio.data.json
│   │   ├── _asyncio.meta.json
│   │   ├── _blake2.data.json
│   │   ├── _blake2.meta.json
│   │   ├── _codecs.data.json
│   │   ├── _codecs.meta.json
│   │   ├── _collections_abc.data.json
│   │   ├── _collections_abc.meta.json
│   │   ├── _contextvars.data.json
│   │   ├── _contextvars.meta.json
│   │   ├── _ctypes.data.json
│   │   ├── _ctypes.meta.json
│   │   ├── _decimal.data.json
│   │   ├── _decimal.meta.json
│   │   ├── _frozen_importlib.data.json
│   │   ├── _frozen_importlib.meta.json
│   │   ├── _frozen_importlib_external.data.json
│   │   ├── _frozen_importlib_external.meta.json
│   │   ├── _hashlib.data.json
│   │   ├── _hashlib.meta.json
│   │   ├── _io.data.json
│   │   ├── _io.meta.json
│   │   ├── _operator.data.json
│   │   ├── _operator.meta.json
│   │   ├── _pickle.data.json
│   │   ├── _pickle.meta.json
│   │   ├── _queue.data.json
│   │   ├── _queue.meta.json
│   │   ├── _random.data.json
│   │   ├── _random.meta.json
│   │   ├── _sitebuiltins.data.json
│   │   ├── _sitebuiltins.meta.json
│   │   ├── _socket.data.json
│   │   ├── _socket.meta.json
│   │   ├── _ssl.data.json
│   │   ├── _ssl.meta.json
│   │   ├── _thread.data.json
│   │   ├── _thread.meta.json
│   │   ├── _typeshed
│   │   ├── _warnings.data.json
│   │   ├── _warnings.meta.json
│   │   ├── _weakref.data.json
│   │   ├── _weakref.meta.json
│   │   ├── _weakrefset.data.json
│   │   ├── _weakrefset.meta.json
│   │   ├── abc.data.json
│   │   ├── abc.meta.json
│   │   ├── annotated_types
│   │   ├── ast.data.json
│   │   ├── ast.meta.json
│   │   ├── asyncio
│   │   ├── base64.data.json
│   │   ├── base64.meta.json
│   │   ├── binascii.data.json
│   │   ├── binascii.meta.json
│   │   ├── builtins.data.json
│   │   ├── builtins.meta.json
│   │   ├── codecs.data.json
│   │   ├── codecs.meta.json
│   │   ├── collections
│   │   ├── colorsys.data.json
│   │   ├── colorsys.meta.json
│   │   ├── concurrent
│   │   ├── contextlib.data.json
│   │   ├── contextlib.meta.json
│   │   ├── contextvars.data.json
│   │   ├── contextvars.meta.json
│   │   ├── copy.data.json
│   │   ├── copy.meta.json
│   │   ├── copyreg.data.json
│   │   ├── copyreg.meta.json
│   │   ├── ctypes
│   │   ├── dataclasses.data.json
│   │   ├── dataclasses.meta.json
│   │   ├── datetime.data.json
│   │   ├── datetime.meta.json
│   │   ├── decimal.data.json
│   │   ├── decimal.meta.json
│   │   ├── dis.data.json
│   │   ├── dis.meta.json
│   │   ├── email
│   │   ├── enum.data.json
│   │   ├── enum.meta.json
│   │   ├── errno.data.json
│   │   ├── errno.meta.json
│   │   ├── fractions.data.json
│   │   ├── fractions.meta.json
│   │   ├── functools.data.json
│   │   ├── functools.meta.json
│   │   ├── genericpath.data.json
│   │   ├── genericpath.meta.json
│   │   ├── gitlab_api
│   │   ├── hashlib.data.json
│   │   ├── hashlib.meta.json
│   │   ├── hmac.data.json
│   │   ├── hmac.meta.json
│   │   ├── http
│   │   ├── importlib
│   │   ├── inspect.data.json
│   │   ├── inspect.meta.json
│   │   ├── io.data.json
│   │   ├── io.meta.json
│   │   ├── ipaddress.data.json
│   │   ├── ipaddress.meta.json
│   │   ├── itertools.data.json
│   │   ├── itertools.meta.json
│   │   ├── json
│   │   ├── keyword.data.json
│   │   ├── keyword.meta.json
│   │   ├── logging
│   │   ├── math.data.json
│   │   ├── math.meta.json
│   │   ├── mimetypes.data.json
│   │   ├── mimetypes.meta.json
│   │   ├── multiprocessing
│   │   ├── numbers.data.json
│   │   ├── numbers.meta.json
│   │   ├── opcode.data.json
│   │   ├── opcode.meta.json
│   │   ├── operator.data.json
│   │   ├── operator.meta.json
│   │   ├── os
│   │   ├── pathlib.data.json
│   │   ├── pathlib.meta.json
│   │   ├── pickle.data.json
│   │   ├── pickle.meta.json
│   │   ├── posixpath.data.json
│   │   ├── posixpath.meta.json
│   │   ├── pydantic
│   │   ├── pydantic_core
│   │   ├── queue.data.json
│   │   ├── queue.meta.json
│   │   ├── random.data.json
│   │   ├── random.meta.json
│   │   ├── re.data.json
│   │   ├── re.meta.json
│   │   ├── requests
│   │   ├── resource.data.json
│   │   ├── resource.meta.json
│   │   ├── select.data.json
│   │   ├── select.meta.json
│   │   ├── selectors.data.json
│   │   ├── selectors.meta.json
│   │   ├── signal.data.json
│   │   ├── signal.meta.json
│   │   ├── socket.data.json
│   │   ├── socket.meta.json
│   │   ├── sre_compile.data.json
│   │   ├── sre_compile.meta.json
│   │   ├── sre_constants.data.json
│   │   ├── sre_constants.meta.json
│   │   ├── sre_parse.data.json
│   │   ├── sre_parse.meta.json
│   │   ├── ssl.data.json
│   │   ├── ssl.meta.json
│   │   ├── string.data.json
│   │   ├── string.meta.json
│   │   ├── subprocess.data.json
│   │   ├── subprocess.meta.json
│   │   ├── sys
│   │   ├── tempfile.data.json
│   │   ├── tempfile.meta.json
│   │   ├── test_gitlab_a2a_validation.data.json
│   │   ├── test_gitlab_a2a_validation.meta.json
│   │   ├── test_gitlab_mcp_validation.data.json
│   │   ├── test_gitlab_mcp_validation.meta.json
│   │   ├── test_setup.data.json
│   │   ├── test_setup.meta.json
│   │   ├── test_verify_agent.data.json
│   │   ├── test_verify_agent.meta.json
│   │   ├── textwrap.data.json
│   │   ├── textwrap.meta.json
│   │   ├── threading.data.json
│   │   ├── threading.meta.json
│   │   ├── time.data.json
│   │   ├── time.meta.json
│   │   ├── traceback.data.json
│   │   ├── traceback.meta.json
│   │   ├── types.data.json
│   │   ├── types.meta.json
│   │   ├── typing.data.json
│   │   ├── typing.meta.json
│   │   ├── typing_extensions.data.json
│   │   ├── typing_extensions.meta.json
│   │   ├── typing_inspection
│   │   ├── urllib
│   │   ├── urllib3
│   │   ├── uuid.data.json
│   │   ├── uuid.meta.json
│   │   ├── validate_a2a_agent.data.json
│   │   ├── validate_a2a_agent.meta.json
│   │   ├── validate_agent.data.json
│   │   ├── validate_agent.meta.json
│   │   ├── verify_a2a_queries.data.json
│   │   ├── verify_a2a_queries.meta.json
│   │   ├── warnings.data.json
│   │   ├── warnings.meta.json
│   │   ├── weakref.data.json
│   │   ├── weakref.meta.json
│   │   ├── zipfile
│   │   ├── zlib.data.json
│   │   ├── zlib.meta.json
│   │   └── zoneinfo
│   └── CACHEDIR.TAG
├── .pre-commit-config.yaml
├── .pytest_cache
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v
│       └── cache
├── .specify
│   └── specs
│       └── code-enhancement-20260512
├── .venv
│   ├── .gitignore
│   ├── .lock
│   ├── CACHEDIR.TAG
│   ├── bin
│   │   ├── activate
│   │   ├── activate-global-python-argcomplete
│   │   ├── activate.bat
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── activate.nu
│   │   ├── activate.ps1
│   │   ├── activate_this.py
│   │   ├── agent-terminal-ui
│   │   ├── cyclopts
│   │   ├── deactivate.bat
│   │   ├── distro
│   │   ├── docutils
│   │   ├── dotenv
│   │   ├── email_validator
│   │   ├── eunomia
│   │   ├── eunomia-mcp
│   │   ├── f2py
│   │   ├── fastapi
│   │   ├── fastmcp
│   │   ├── genai-prices
│   │   ├── gitlab-agent
│   │   ├── gitlab-mcp
│   │   ├── gql-cli
│   │   ├── httpx
│   │   ├── install-skills
│   │   ├── jsonschema
│   │   ├── keyring
│   │   ├── logfire
│   │   ├── markdown-it
│   │   ├── mcp
│   │   ├── normalizer
│   │   ├── numpy-config
│   │   ├── openai
│   │   ├── opentelemetry-bootstrap
│   │   ├── opentelemetry-instrument
│   │   ├── pai
│   │   ├── py.test
│   │   ├── pydoc.bat
│   │   ├── pygmentize
│   │   ├── pyrsa-decrypt
│   │   ├── pyrsa-encrypt
│   │   ├── pyrsa-keygen
│   │   ├── pyrsa-priv2pub
│   │   ├── pyrsa-sign
│   │   ├── pyrsa-verify
│   │   ├── pytest
│   │   ├── python
│   │   ├── python-argcomplete-check-easy-install-script
│   │   ├── python3
│   │   ├── python3.11
│   │   ├── register-python-argcomplete
│   │   ├── rst2html
│   │   ├── rst2html4
│   │   ├── rst2html5
│   │   ├── rst2latex
│   │   ├── rst2man
│   │   ├── rst2odt
│   │   ├── rst2pseudoxml
│   │   ├── rst2s5
│   │   ├── rst2xetex
│   │   ├── rst2xml
│   │   ├── tqdm
│   │   ├── typer
│   │   ├── uvicorn
│   │   ├── watchfiles
│   │   └── websockets
│   ├── include
│   │   └── site
│   ├── lib
│   │   └── python3.11
│   ├── lib64
│   │   └── python3.11
│   └── pyvenv.cfg
├── .vulture_ignore
├── AGENTS.md
├── CHANGELOG.md
├── LICENSE
├── MANIFEST.in
├── README.md
├── a2a.json
├── build-requirements.txt
├── docker
│   ├── Dockerfile
│   ├── compose.yml
│   ├── debug.Dockerfile
│   └── mcp.compose.yml
├── docs
│   ├── index.md
│   └── overview.md
├── gitlab_api
│   ├── __init__.py
│   ├── __main__.py
│   ├── agent_server.py
│   ├── api_client.py
│   ├── auth.py
│   ├── gitlab_gql.py
│   ├── gitlab_input_models.py
│   ├── gitlab_response_models.py
│   ├── main_agent.json
│   ├── mcp_config.json
│   └── mcp_server.py
├── mcp_config.json
├── mkdocs.yml
├── mypy_out.txt
├── opencode.json
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── scripts
│   ├── all_skeletons.py
│   ├── commits_args.txt
│   ├── deploy_tokens_args.txt
│   ├── environments_args.txt
│   ├── extract_args.py
│   ├── generate_table.py
│   ├── groups_args.txt
│   ├── jobs_args.txt
│   ├── merge_requests_args.txt
│   ├── new_table.md
│   ├── pipelines_args.txt
│   ├── projects_args.txt
│   ├── releases_args.txt
│   ├── releases_skeleton.py
│   ├── repositories_args.txt
│   ├── rewrite_commits.py
│   ├── rewrite_deploy_tokens.py
│   ├── rewrite_environments.py
│   ├── rewrite_groups.py
│   ├── rewrite_jobs.py
│   ├── rewrite_merge_requests.py
│   ├── rewrite_pipelines.py
│   ├── rewrite_projects.py
│   ├── rewrite_protected_branches.py
│   ├── rewrite_releases.py
│   ├── rewrite_remaining.py
│   ├── update_readme.py
│   ├── validate_a2a_agent.py
│   └── validate_agent.py
├── starship.toml
├── test-requirements.txt
├── test_setup.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_wrapper.py
│   ├── test_concept_parity.py
│   ├── test_gitlab_a2a_validation.py
│   ├── test_gitlab_api_brute_force_coverage.py
│   ├── test_gitlab_mcp_validation.py
│   ├── test_gitlab_models.py
│   ├── test_verify_agent.py
│   └── verify_a2a_queries.py
└── uv.lock
```

## Code Style & Conventions
**Always:**
- Use `agent-utilities` for common patterns (e.g., `create_mcp_server`, `create_agent`).
- Define input/output models using Pydantic.
- Include descriptive docstrings for all tools (they are used as tool descriptions for LLMs).
- Check for optional dependencies using `try/except ImportError`.

**Good example:**
```python
from agent_utilities import create_mcp_server
from mcp.server.fastmcp import FastMCP

mcp = create_mcp_server("my-agent")

@mcp.tool()
async def my_tool(param: str) -> str:
    """Description for LLM."""
    return f"Result: {param}"
```

## Dos and Don'ts
**Do:**
- Run `pre-commit` before pushing changes.
- Use existing patterns from `agent-utilities`.
- Keep tools focused and idempotent where possible.

**Don't:**
- Use `cd` commands in scripts; use absolute paths or relative to project root.
- Add new dependencies to `dependencies` in `pyproject.toml` without checking `optional-dependencies` first.
- Hardcode secrets; use environment variables or `.env` files.

## Safety & Boundaries
**Always do:**
- Run lint/test via `pre-commit`.
- Use `agent-utilities` base classes.

**Ask first:**
- Major refactors of `mcp_server.py` or `agent.py`.
- Deleting or renaming public tool functions.

**Never do:**
- Commit `.env` files or secrets.
- Modify `agent-utilities` or `universal-skills` files from within this package.

## When Stuck
- Propose a plan first before making large changes.
- Check `agent-utilities` documentation for existing helpers.

## ⛔ No Scratch or Temporary Files in Repository

**NEVER write any of the following to this repository:**
- Temporary test scripts (`test_*.py`, `debug_*.py` outside of `tests/`)
- Scratch scripts or experimental one-off files
- Log files (`.log`, `.txt` command output)
- Random text files with command output or debug dumps
- Any file that is NOT production source code, tests in `tests/`, or documentation

**Why:** These files expose private filesystem paths, credentials, and internal infrastructure details when pushed to GitHub publicly.

**Where to put scratch work instead:**
- Use `~/workspace/scratch/` for temporary scripts and experiments
- Use `~/workspace/reports/` for command output and reports
- Keep test scripts in the `tests/` directory following proper pytest conventions

## ⛔ Keep the Repository Root Pristine — No Scratch / Temp / Debug Files

**The repository ROOT must contain only canonical project files** (packaging,
config, docs, lockfiles). The only hidden directories allowed at root are
`.git/`, `.github/`, and `.specify/` (plus a local, git-ignored `.venv/`).

**NEVER write any of the following — anywhere in the repo, and ESPECIALLY at the root:**
- One-off / debug / migration scripts: `fix_*.py`, `migrate_*.py`, `refactor_*.py`,
  `replace_*.py`, `update_*.py`, `debug_*.py`, or `test_*.py` **at the root**
  (real tests live in `tests/` only).
- Databases / data dumps: `*.db`, `*.db-wal`, `*.sqlite*`, `*.corrupted`.
- Logs / command output: `*.log`, scratch `*.txt`, `*.orig`, `*.rej`, `*.bak`.
- Build artifacts: `*.tsbuildinfo`, compiled binaries, coverage files.
- AI agent scratch directories: `.agent/`, `.agents/`, `.agent_data/`, `.tmp/`,
  `.hypothesis/`, or any per-tool cache committed to git.
- Any file that is NOT production source, a test in `tests/`, documentation, or
  a recognized config/lockfile.

**Why:** scratch at the root leaks private paths/credentials, bloats the tree,
and erodes a pristine codebase.

**Where scratch goes instead:** `~/workspace/scratch/` (experiments),
`~/workspace/reports/` (command output); tests go in `tests/` (pytest).
Before finishing a task, run `git status` and confirm no stray root files were added.

## Quality Bar — Leave the Codebase Clean (REQUIRED)

After completing any code change, run the project's pre-commit suite and drive it
**fully green** before committing:

```bash
pre-commit run --all-files
```

Resolve **every** issue it reports — failures, lint errors, type errors, and
warnings — **including problems that pre-date your change and were not caused by
your edits**. The standing goal is a clean, working codebase with **no errors and
no warnings**. Do not silence checks (`# noqa`, `# type: ignore`, `SKIP=`,
`--no-verify`) to force green unless the exception is already documented in this
file as a known, unavoidable limitation. Only commit once `pre-commit run
--all-files` passes cleanly; if a check legitimately cannot pass, stop and explain
why rather than bypassing it.

## Working with Git Worktrees (multi-session)

Multiple agents/sessions work the `agent-packages/*` repos concurrently. **Do not
edit the canonical checkout** (`/home/apps/workspace/agent-packages/<repo>`) — a
background `repository-manager` sync can reset its working tree and discard
uncommitted edits. Take your own git worktree on your own branch instead:

```bash
# preferred — repository-manager MCP:
rm_worktree add <repo> <your-branch>      # -> /home/apps/worktrees/<repo>/<your-branch>

# raw-git fallback:
git -C agent-packages/<repo> checkout main
git -C agent-packages/<repo> worktree add /home/apps/worktrees/<repo>/<branch> -b <branch>
```

Work in the worktree, **commit often** (commits survive a working-tree reset),
then merge to main locally (`rm_worktree merge <repo> <branch>`, or `git merge
--no-ff`). Each session must use a **distinct branch** — git allows a branch in
only one worktree, which is what keeps concurrent sessions from colliding.
Worktrees live under `/home/apps/worktrees/` (outside the workspace scan, so the
sync leaves them alone). Push only when asked.
