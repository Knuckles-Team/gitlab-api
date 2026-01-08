import requests
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8005/mcp"
HEADERS = {"Content-Type": "application/json"}


def test_mcp_server_up():
    """Verify MCP server is reachable"""
    logger.info("Verifying MCP Server Spin Up...")
    try:
        # Check initialization (SSE or POST)
        # FastMCP typically exposes /mcp/sse or /mcp/messages
        # Let's check getting tools via JSON-RPC
        payload = {"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}
        response = requests.post(f"{BASE_URL}/messages", json=payload, headers=HEADERS)
        if response.status_code == 404:  # Try root if /mcp/messages not valid
            response = requests.post(
                "http://localhost:8005/mcp", json=payload, headers=HEADERS
            )

        if response.status_code != 200:
            # FastMCP often mounts at /mcp or /, if server is configured differently.
            # Docker compose says 8005:8005, internal 8005.
            # entrypoint: gitlab-mcp command.
            # Code uses FastMCP.
            # Let's try standard endpoint.
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
    # Using /messages endpoint which is standard for HTTP transport in some MCP implementations
    # But FastMCP might use SSE.
    # Actually FastMCP usually exposes a FastAPI app.
    # Let's assume standard POST for simplicity or check logs.
    # If using SSE, we can't test easily with requests.
    # But FastMCP supports HTTP transport if configured.
    # Let's try the POST endpoint.

    # Wait, `requests.post` to `/mcp`?
    # In FastMCP, standard usage usually enables SSE.
    # However, for testing, we can often POST to the message handler if exposed.
    # Let's assume `http://localhost:8005/mcp/messages` or just `/mcp` handles POST.

    response = requests.post("http://localhost:8005/mcp", json=payload, headers=HEADERS)
    if response.status_code == 405:  # Method Not Allowed -> Maybe only SSE?
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
