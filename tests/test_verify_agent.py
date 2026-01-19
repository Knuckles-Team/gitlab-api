import pytest
import requests
import json
import time
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:9016"
ENDPOINT = "/a2a/"


def send_rpc(method, params, id=1):
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": id}
    try:
        response = requests.post(f"{BASE_URL}{ENDPOINT}", json=payload)
        # response.raise_for_status()
        # We might want to see the error in the response content if 400/500
        try:
            return response.json()
        except Exception:
            logger.error(f"Response text: {response.text}")
            raise
    except Exception as e:
        logger.error(f"RPC {method} failed: {e}")
        return None


def poll_task(task_id, timeout=120):
    start = time.time()
    logger.info(f"Polling task {task_id}...")
    while time.time() - start < timeout:
        res = send_rpc("tasks/get", {"id": task_id}, id=99)
        if res and "result" in res:
            state = res["result"].get("status", {}).get("state")
            logger.info(f"Task State: {state}")
            if state == "completed":
                return res["result"]
            if state == "failed":
                return res["result"]
        time.sleep(2)
    return None


def run_query_and_wait(query, description):
    """
    Submits a query, polls for completion, and returns the final result object.
    """
    logger.info(f"\n--- {description} ---")
    logger.info(f"Query: {query}")

    # Construct FastA2A compatible message
    message = {
        "kind": "message",
        "role": "user",
        "messageId": f"query-{int(time.time())}",
        "parts": [{"kind": "text", "text": query}],
    }

    res = send_rpc("message/send", {"message": message})
    if not res or "error" in res:
        logger.error(f"Submission failed: {res}")
        pytest.fail(f"RPC submission failed: {res}")

    task_id = res.get("result", {}).get("id")
    if not task_id:
        logger.error("No task ID returned")
        pytest.fail("No task ID returned from message/send")

    final_result = poll_task(task_id)
    if not final_result:
        pytest.fail(f"Task {task_id} timed out or could not be retrieved")

    return final_result


def get_assistant_text(final_result):
    history = final_result.get("history", [])
    if not history:
        return None
    last_msg = history[-1]
    if last_msg.get("role") == "model":
        return last_msg.get("parts", [{}])[0].get("text", "")
    return None


def check_container_logs(container_name):
    """
    Checks docker logs for a specific container for errors.
    Returns a list of error lines or empty list if clean.
    """
    try:
        result = subprocess.run(
            ["docker", "logs", container_name], capture_output=True, text=True
        )
        if result.returncode != 0:
            return [f"Failed to get logs for {container_name}: {result.stderr}"]

        logs = result.stdout + result.stderr
        errors = []
        # Filter for relevant error keywords
        # We look for "Traceback", "Error", "Exception" but exclude some common noise if any
        for line in logs.splitlines():
            lower_line = line.lower()
            if (
                "traceback" in lower_line
                or "exception" in lower_line
                or ("error" in lower_line and "debug" not in lower_line)
            ):
                # Basic filter, might need refinement based on actual logs
                errors.append(line)
        return errors
    except Exception as e:
        return [f"Exception checking logs: {e}"]


# --- Tests ---


def test_graphiti_ingestion():
    result = run_query_and_wait(
        "Does the documentation saying anything about how to create a branch? Please summarize.",
        "Validating Graphiti Ingestion",
    )
    # Check if we got a valid response
    text = get_assistant_text(result)
    assert (
        text is not None
    ), f"No response text from assistant. Result: {json.dumps(result, indent=2)}"
    logger.info(f"Graphiti Ingestion Result: {text}")


def test_branch_creation_flow():
    # 1. Create
    result_create = run_query_and_wait(
        "Create a branch called 'test-a2a' in project id 202 from 'main'.",
        "Validating Create Branch (Delegation)",
    )
    text_create = get_assistant_text(result_create)
    assert (
        text_create is not None
    ), f"No response text from assistant. Result: {json.dumps(result_create, indent=2)}"
    logger.info(f"Create Branch Result: {text_create}")

    # 2. Verify
    result_verify = run_query_and_wait(
        "List branches for project id 202 and check if 'test-a2a' exists.",
        "Verifying Branch Creation",
    )
    text_verify = get_assistant_text(result_verify)
    assert (
        text_verify is not None
    ), f"No response text from assistant. Result: {json.dumps(result_verify, indent=2)}"
    logger.info(f"Verify Branch Result: {text_verify}")


def test_pipeline_flow():
    # 1. Run Pipeline
    result_run = run_query_and_wait(
        "Run a pipeline for project id 202 on the 'main' branch.",
        "Validating Run Pipeline",
    )
    text_run = get_assistant_text(result_run)
    assert (
        text_run is not None
    ), f"No response text from assistant. Result: {json.dumps(result_run, indent=2)}"
    logger.info(f"Run Pipeline Result: {text_run}")

    # 2. Verify
    result_verify = run_query_and_wait(
        "List the most recent pipelines for project id 202.",
        "Verifying Pipeline Execution",
    )
    text_verify = get_assistant_text(result_verify)
    assert (
        text_verify is not None
    ), f"No response text from assistant. Result: {json.dumps(result_verify, indent=2)}"
    logger.info(f"Verify Pipeline Result: {text_verify}")


def test_list_projects():
    result = run_query_and_wait(
        "List all projects available.", "Validating Get Projects"
    )
    text = get_assistant_text(result)
    assert (
        text is not None
    ), f"No response text from assistant. Result: {json.dumps(result, indent=2)}"
    logger.info(f"List Projects Result: {text}")


def test_z_validate_service_logs():
    """
    Runs last (alphabetically) to validate logs of mcp and a2a services.
    """
    logger.info("Checking docker logs for errors...")

    services = ["gitlab-mcp", "gitlab-a2a"]
    all_errors = {}

    for service in services:
        errors = check_container_logs(service)
        if errors:
            all_errors[service] = errors

    if all_errors:
        error_msg = json.dumps(all_errors, indent=2)
        pytest.fail(f"Found errors in service logs:\n{error_msg}")

    logger.info("Service logs looked clean (no Traceback/Exception/Error found).")
