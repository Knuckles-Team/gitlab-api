import os
import sys
from gitlab_api.agent_server import agent_template


def test_template_in_process():
    print("Testing gitlab-api agent_template for in-process MCP...")

    # Clear env vars that might force external MCP
    os.environ.pop("MCP_URL", None)
    os.environ.pop("MCP_CONFIG", None)

    graph, config = agent_template()

    mcp_toolsets = config.get("mcp_toolsets", [])
    print(f"Number of toolsets: {len(mcp_toolsets)}")

    if not mcp_toolsets:
        print("FAIL: No toolsets found!")
        sys.exit(1)

    found_fastmcp = False
    for ts in mcp_toolsets:
        # FastMCP instance is what we expect
        if hasattr(ts, "name") and ts.name == "GitLab":
            print(f"SUCCESS: Found in-process toolset: {ts}")
            found_fastmcp = True
            break

    if not found_fastmcp:
        print("FAIL: In-process GitLab MCP toolset not found in config.")
        sys.exit(1)
    else:
        print("Template verification PASSED.")


if __name__ == "__main__":
    test_template_in_process()
