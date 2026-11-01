# CONN-GITLAB-API quickstart

Run the served proof from a fresh checkout after `uv sync`:

- `PYTHONNOUSERSITE=1 uv run pytest tests/test_merge_request_served.py::test_served_tools_and_normalizer_round_trip -q`
- `PYTHONNOUSERSITE=1 uv run pytest tests/test_merge_request_tools.py -q`
