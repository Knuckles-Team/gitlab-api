import requests
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:9000"
ENDPOINT = "/"


def send_rpc(method, params, id=1):
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": id}
    try:
        response = requests.post(f"{BASE_URL}{ENDPOINT}", json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"RPC {method} failed: {e}")
        return None


def poll_task(task_id, timeout=120, interval=1):
    start = time.time()
    logger.info(f"Polling task {task_id}...")
    while time.time() - start < timeout:
        res = send_rpc("tasks/get", {"id": task_id}, id=99)
        if res:
            logger.debug(
                f"Full poll response: {json.dumps(res, indent=2)}"
            )  # Log EVERY poll
            if "error" in res:
                logger.error(f"RPC error: {res['error']}")
            if "result" in res:
                state = res["result"].get("status", {}).get("state")
                logger.info(f"Task State: {state}")
                if state in ["completed", "failed"]:
                    if state == "failed" and "error" in res["result"]:
                        logger.error(f"Task error details: {res['result']['error']}")
                    return res["result"]
        time.sleep(interval)
    return None


def run_query(query, description):
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
        return

    task_id = res.get("result", {}).get("id")
    if not task_id:
        logger.error("No task ID returned")
        return

    final_result = poll_task(task_id)
    if final_result:
        # Extract the final answer if possible (requires parsing result history/steps)
        # Usually checking the last message in history or an 'output' field if A2A provided it
        # FastA2A history is list of messages.
        history = final_result.get("history", [])
        last_msg = history[-1] if history else {}

        # Check if last msg is from assistant
        if last_msg.get("role") == "model":
            content = last_msg.get("parts", [{}])[0].get("text", "")
            logger.info(f"Result: {content}")
        else:
            logger.info(f"Result (Raw): {final_result}")
    else:
        logger.warning("Timed out or failed to get result.")


if __name__ == "__main__":
    # 1. Validate Graphiti Ingestion
    run_query(
        "Does the documentation saying anything about how to create a branch? Please summarize.",
        "Validating Graphiti Ingestion",
    )

    # 2. Validate Create Branch (Delegation)
    timestamp = int(time.time())
    branch_name = f"test-agent-{timestamp}"
    run_query(
        f"Create a branch called '{branch_name}' in project id 202 from 'main'.",
        "Validating Create Branch (Delegation)",
    )
    # 2b. Verify Branch Creation
    run_query(
        f"List branches for project id 202 and check if '{branch_name}' exists.",
        "Verifying Branch Creation",
    )

    # 3. Validate Run Pipeline
    run_query(
        "Run a pipeline for project id 202 on the 'main' branch.",
        "Validating Run Pipeline",
    )
    # 3b. Verify Pipeline Run
    run_query(
        "List the most recent pipelines for project id 202.",
        "Verifying Pipeline Execution",
    )

    # 4. Other Read Queries
    run_query("List all projects available.", "Validating Get Projects")
