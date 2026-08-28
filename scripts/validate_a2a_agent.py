#!/usr/bin/env python3
import asyncio
import json
import os
import uuid

import httpx

A2A_URL = os.environ.get("A2A_URL", "http://127.0.0.1:9016/a2a/")

_IN_PROGRESS_STATES = ("submitted", "running", "working")


def _message_payload(question: str) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": "message/send",
        "params": {
            "message": {
                "kind": "message",
                "role": "user",
                "parts": [{"kind": "text", "text": question}],
                "messageId": str(uuid.uuid4()),
            }
        },
        "id": 1,
    }


def _poll_payload(task_id) -> dict:
    return {
        "jsonrpc": "2.0",
        "method": "tasks/get",
        "params": {"id": task_id},
        "id": 2,
    }


def _last_agent_message(history: list):
    for msg in reversed(history):
        if msg.get("role") != "user":
            return msg
    return None


def _print_agent_response(last_msg) -> None:
    if last_msg and "parts" in last_msg:
        print("\n--- Agent Response ---")
        for part in last_msg["parts"]:
            if "text" in part:
                print("Agent response content omitted.")
            elif "content" in part:
                print("Agent response content omitted.")
    elif last_msg:
        print("Final response received without structured parts.")
    else:
        print("\n--- No Agent Response Found in History ---")


def _print_finished_task(state: str, result: dict) -> None:
    print(f"\nTask Finished with state: {state}")
    if "history" in result:
        history = result["history"]
        if history:
            _print_agent_response(_last_agent_message(history))
    print("Validation result received; body omitted.")


async def _poll_once(client: httpx.AsyncClient, url: str, task_id) -> bool:
    """Poll the task once. Return True when polling should stop."""

    await asyncio.sleep(2)
    poll_resp = await client.post(
        url,
        json=_poll_payload(task_id),
        headers={"Content-Type": "application/json"},
    )
    if poll_resp.status_code != 200:
        print(f"Polling Failed: {poll_resp.status_code}")
        print(f"Polling failed with HTTP {poll_resp.status_code}.")
        return True

    poll_data = poll_resp.json()
    if "result" not in poll_data:
        print("Starting polling error key check...")
        if "error" in poll_data:
            print(
                f"Polling JSON-RPC error code: {poll_data['error'].get('code', 'unknown')}"
            )
        return True

    state = poll_data["result"]["status"]["state"]
    print(f"Task State: {state}")
    if state in _IN_PROGRESS_STATES:
        return False

    _print_finished_task(state, poll_data["result"])
    return True


async def _poll_task(client: httpx.AsyncClient, url: str, task_id) -> None:
    print("\nTask submitted; polling for result...")
    while True:
        if await _poll_once(client, url, task_id):
            break


async def _handle_ok_response(client: httpx.AsyncClient, url: str, resp) -> None:
    try:
        data = resp.json()
        print("JSON response received.")

        if "result" in data and "id" in data["result"]:
            await _poll_task(client, url, data["result"]["id"])

        if "error" in data:
            print(f"JSON-RPC error code: {data['error'].get('code', 'unknown')}")
    except json.JSONDecodeError:
        print(f"Response body omitted (HTTP {resp.status_code}).")


async def _submit_question(client: httpx.AsyncClient, url: str, question: str) -> None:
    print("\nSubmitting the configured validation query.")
    print("--- Sending Request ---")

    payload = _message_payload(question)

    try:
        print("Trying the configured endpoint with JSON-RPC (message/send)...")
        resp = await client.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )

        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            await _handle_ok_response(client, url, resp)
        else:
            print(f"Error: {resp.status_code}")
            print(f"Response body omitted (HTTP {resp.status_code}).")

    except httpx.RequestError as e:
        print(f"Operation failed: {type(e).__name__}")


async def main():
    print("Validating the configured A2A agent...")

    questions = [
        os.environ.get(
            "A2A_VALIDATION_QUERY", "Describe your available capabilities."
        )
    ]

    async with httpx.AsyncClient(timeout=10000.0) as client:
        for q in questions:
            await _submit_question(client, A2A_URL, q)


if __name__ == "__main__":
    asyncio.run(main())
