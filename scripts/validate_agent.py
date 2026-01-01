#!/usr/bin/env python3
import asyncio
import sys

# Attempt to import assuming dependencies are installed
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
            #"Can I create a merge request for project id 171?", 
            "How can I run a pipeline for project id 171 on the 'main' branch?",
            "How can I create a branch called 'test' from the 'main' branch for project id 204?"
            # "Hello, who are you?",
        ]
        
        print("\n--- Starting Sample Chat Validation ---\n")
        
        for q in questions:
            print(f"\n\n\nUser: {q}")
            try:
                result = await agent.run(q)
                print(f"\n\nAgent Result: {result.output}\n")
                
                # Check for tool usage in result if possible
                # In pydantic-ai 0.0.x, we might not see tool calls easily without inspecting messages
                # But we can infer from the logs or response if it says "Ingested successfully" or similar.
                
            except Exception as e:
                print(f"\n\nError processing question '{q}': {e}")
            
    except Exception as e:
        print(f"Validation failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
