import os
import sys

from agent_utilities import initialize_graph_from_workspace


def test_template_in_process():
    print("Testing gitlab-api setup for in-process MCP...", file=sys.stderr)

    os.environ.pop("MCP_URL", None)
    os.environ.pop("MCP_CONFIG", None)

    graph, config = initialize_graph_from_workspace()

    mcp_toolsets = config.get("mcp_toolsets", [])
    print(f"Number of toolsets: {len(mcp_toolsets)}", file=sys.stderr)

    if not mcp_toolsets:
        print("FAIL: No toolsets found!", file=sys.stderr)
        sys.exit(1)

    found_fastmcp = False
    for ts in mcp_toolsets:
        if hasattr(ts, "name") and ts.name == "GitLab":
            print(f"SUCCESS: Found in-process toolset: {ts}", file=sys.stderr)
            found_fastmcp = True
            break

    if not found_fastmcp:
        print(
            "FAIL: In-process GitLab MCP toolset not found in config.", file=sys.stderr
        )
        sys.exit(1)
    else:
        print("Template verification PASSED.", file=sys.stderr)


if __name__ == "__main__":
    test_template_in_process()
