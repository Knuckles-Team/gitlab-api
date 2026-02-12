import requests
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8005/mcp"
HEADERS = {"Content-Type": "application/json"}


def test_mcp_server_up():
    """Verify MCP server is reachable"""
    logger.info("Verifying MCP Server Spin Up...")
    try:
        payload = {"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}
        response = requests.post(f"{BASE_URL}/messages", json=payload, headers=HEADERS)
        if response.status_code == 404:
            response = requests.post(
                "http://localhost:8005/mcp", json=payload, headers=HEADERS
            )

        if response.status_code != 200:
            logger.warning(
                f"Initial check failed: {response.status_code}. Trying alternate endpoints."
            )
            return False

        logger.info("MCP Server is UP and responding to JSON-RPC.")
        tools = response.json().get("result", {}).get("tools", [])
        logger.info(f"Found {len(tools)} tools.")
        return True
    except Exception as e:
        logger.error(f"MCP Server down: {e}")
        return False


def test_create_branch():
    """Test creating a branch via MCP tool directly"""
    logger.info("Testing 'gitlab_create_branch' tool...")
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "gitlab_create_branch",
            "arguments": {
                "project_id": 202,
                "branch": "test-mcp-validation",
                "ref": "main",
            },
        },
        "id": 2,
    }

    response = requests.post("http://localhost:8005/mcp", json=payload, headers=HEADERS)
    if response.status_code == 405:
        logger.warning("MCP might be SSE only. Cannot validate via simple POST.")
        return

    logger.info(f"Tool Call Response: {response.text}")
    assert response.status_code == 200
    result = response.json()
    assert "error" not in result
    logger.info("Branch creation test passed (or at least returned success).")


if __name__ == "__main__":
    if test_mcp_server_up():
        test_create_branch()
    else:
        sys.exit(1)
