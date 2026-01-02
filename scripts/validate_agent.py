#!/usr/bin/env python3
import asyncio
import sys

# Attempt to import assuming dependencies are installed
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from gitlab_api.gitlab_a2a import create_gitlab_agent
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please install dependencies via `pip install .[all]`")
    sys.exit(1)


async def main():
    print("Initializing GitlabA2A Agent...")
    try:
        # Connect to real Ollama service
        # Using localhost because this script runs on the host (or same network stack)
        # where port 11434 is mapped.
        agent = await create_gitlab_agent(
            provider="openai",
            model_id="qwen3:4b",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            mcp_url="http://localhost:8005/mcp",
        )

        print("Agent initialized successfully.")

        # Define sample questions
        questions = [
            "Can you create a merge request for project id 171 with a title of 'Test Merge Request' from the 'validate' to 'main' branch? For the description please put 'this is a test merge request'.",
            "Can you run the pipeline for project id 171 on the 'main' branch?",
            "Can you create a branch called 'test' from the 'main' branch for project id 171?",
        ]

        print("\n--- Starting Sample Chat Validation ---\n")

        for q in questions:
            print(f"\n\n\nUser: {q}")
            try:
                result = await agent.run(q)
                print(f"\n\nAgent Result: {result.output}\n")
                if hasattr(agent, "tools"):
                    print(f"Agent Tools: {[t.__name__ for t in agent.tools]}")
                elif hasattr(agent, "_tools"):
                    print(f"Agent Tools: {[t.__name__ for t in agent._tools]}")

            except Exception as e:
                print(f"\n\nError processing question '{q}': {e}")

    except Exception as e:
        print(f"Validation failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
