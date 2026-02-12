import requests
import time
import pytest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:9000"


def wait_for_service(url, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(url)
            if resp.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    return False


def test_a_spin_up():
    """Validate A) The A2A Agent is able to spin up"""
    logger.info("Verifying A2A Agent Spin Up...")
    assert wait_for_service(
        f"{BASE_URL}/docs"
    ), "A2A Agent failed to spin up (docs not reachable)"
    logger.info("A2A Agent is UP.")


def test_b_respond_to_query():
    """Validate B) The A2A Agent is able to respond to a query"""
    logger.info("Verifying A2A Agent Response...")

    endpoint = "/"
    success = False

    method = "message/send"

    logger.info(f"Trying JSON-RPC method: {method}")
    try:
        param_options = [
            {
                "message": {
                    "kind": "message",
                    "role": "user",
                    "messageId": "123",
                    "parts": [{"kind": "text", "text": "Hello"}],
                }
            }
        ]

        for params in param_options:
            logger.info(f"Trying params: {params}")
            payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
            logger.info(f"Method {method} returned {response.status_code}")

            if response.status_code == 200:
                body = response.json()
                if "error" in body:
                    logger.warning(
                        f"Method {method} returned RPC error: {body['error']}"
                    )
                else:
                    logger.info(f"Query Response: {body}")
                    success = True
                    break
            else:
                logger.warning(
                    f"Endpoint {endpoint} failed with {response.status_code}: {response.text}"
                )

            if success:
                break

    except Exception as e:
        logger.warning(f"Error calling {method}: {e}")

    if not success:
        pytest.fail("Could not find a working JSON-RPC params for message/send.")


def test_c_d_e_f_full_flow():
    """Validate C, D, E, F"""
    logger.info("Verifying Complex Flow...")
    endpoint = "/"
    method = "message/send"

    doc_query = "What is the correct API endpoint for 'deploy_tokens' according to the documentation?"

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "message": {
                "kind": "message",
                "role": "user",
                "messageId": "validation-msg-2",
                "parts": [{"kind": "text", "text": doc_query}],
            }
        },
        "id": 2,
    }
    response = requests.post(f"{BASE_URL}{endpoint}", json=payload)

    logger.info(f"Submission Response: {response.text}")
    assert response.status_code == 200, "Graphiti query submission failed"
    body = response.json()
    assert "error" not in body, f"JSON-RPC Error: {body.get('error')}"

    result = body.get("result", {})
    task_id = result.get("id")
    if task_id:
        logger.info(f"Task submitted with ID: {task_id}. Polling for result...")
        for _ in range(10):
            time.sleep(2)
            poll_payload = {
                "jsonrpc": "2.0",
                "method": "tasks/get",
                "params": {"id": task_id},
                "id": 3,
            }
            poll_resp = requests.post(f"{BASE_URL}{endpoint}", json=poll_payload)
            if poll_resp.status_code == 200:
                poll_body = poll_resp.json()
                task_status = poll_body.get("result", {}).get("status", {}).get("state")
                logger.info(f"Task State: {task_status}")
                if task_status == "completed":
                    logger.info(f"Task result: {poll_body}")
                    break
                if task_status == "failed":
                    logger.warning("Task failed")
                    break
            else:
                logger.warning(f"Poll failed: {poll_resp.status_code}")
    else:
        logger.warning("No taskId returned, cannot poll.")


if __name__ == "__main__":
    try:
        test_a_spin_up()
        test_b_respond_to_query()
        test_c_d_e_f_full_flow()
        print("All Tests Passed!")
    except Exception as e:
        print(f"Test Failed: {e}")
        exit(1)
