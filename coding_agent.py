import inspect
import json
import os

from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
from typing import Any, Dict, List, Tuple

load_dotenv()

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a coding assistant whose goal it is to help us solve coding tasks. 
You have access to a series of tools you can execute. Hear are the tools you can execute:

{tool_list_repr}

When you want to use a tool, reply with exactly one line in the format: 'tool: TOOL_NAME({{JSON_ARGS}})' and nothing else.
Use compact single-line JSON with double quotes. After receiving a tool_result(...) message, continue the task.
If no tool is needed, respond normally.
"""

YOU_COLOR = "\u001b[94m"
ASSISTANT_COLOR = "\u001b[92m"
RESET_COLOR = "\u001b[0m"

def resolve_abs_path(path: str) -> Path:
    """
    file.py -> /Users/home/ashwinprakash/modern-software-dev-lectures/file.py
    """
    path = Path(path).expanduser()
    if not path.exists():
        path =(path.cwd() / path).resolve()
    return path

def list_files_tool(path: str) -> Dict[str, Any]:
    """
    Lists the files in a directory provided by the user.
    :param path: The path to a directory to list files from.
    :return: A list of files in the directory.
    """
    full_path = resolve_abs_path(path)
    all_files = []
    for item in full_path.iterdir():
        all_files.append({
            "filename": item.name,
            "type": "file" if item.is_file() else "dir"
        })
    return {
        "path": str(full_path),
        "files": all_files
    }

def read_file_tool(path: str) -> Dict(str, Any):
    """
    Lists the files in a directory provided by the user.
    :param path: The path to a directory to list files from.
    :return: A list of files in the directory.
    """
    full_path = resolve_abs_path(path)
    all_files = []
    for item in full_path.iterdir():
        all_files.append({
            "file_name": item.name,
            "type": "file" if item.is_file() else "dir",
        })
    return {"path": path, "files": all_files}

def edit_file_tool(path: str, old_str: str, new_str: str) -> Dict(str, Any):
    """
    Replaces first occurrence of old_str with new_str in file. If old_str is empty,
    create/overwrite file with new_str.
    :param path: The path to the file to edit.
    :param old_str: The string to replace.
    :param new_str: The string to replace with.
    :return: A dictionary with the path to the file and the action taken.
    """
    full_path = resolve_abs_path(path)
    if old_str == "":
        full_path.write_text(new_str, encoding="utf-8")
        return {
            "path": str(full_path),
            "action": "created_file",
        }
    original = full_path.read_text(encoding="utf-8")
    if original.find(old_str) == -1:
        return {
            "path": str(full_path),
            "action": "old_str_not_found",
        }
    edited = original.replace(old_str, new_str,1)
    full_path.write_text(edited, encoding="utf-8")
    return {
        "path": str(full_path),
        "action": "edited_file",
    }

TOOL_REGISTRY = {
    "read_file": read_file_tool,
    "list_files": list_files_tool,
    "edit_file": edit_file_tool,
}

def get_tool_str_representation(tool_name: str) -> str:
    """
    Returns a string representation of the tools available to the assistant.
    """
    tool = TOOL_REGISTRY[tool_name]
    return f"""
    Name: {tool_name}
    Description: {tool.__doc__}
    Signature: {inspect.signature(tool)}
    """

def get_full_system_prompt() -> str:
    tool_str_rer = ""
    for tool_name in TOOL_REGISTRY:
        tool_str_repr += "TOOL\n===" + get_tool_str_representation(tool_name)
        tool_str_repr += f"\n{"="*15}\n"
    return SYSTEM_PROMPT.format(tool_list_repr=tool_str_repr)

def extract_tool_invocation(text: str) -> Tuple[str, Dict[str, Any]]:
    """
    Return list of (tool_name, args) requested in 'tool: name({...})' lines.
    The parser expects single-line, compact JSON in parentheses.
    """
    invocations = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("tool:"):
            continue
        try:
            after = line[len("tool:"):].strip()
            name, rest = after.split("(",1)
            name = name.strip()
            if not rest.endswith(")"):
                continue
            json_str = rest[:-1].strip()
            args = json.loads(json_str)
            invocations.append((name, args))
        except Exception as e:
            continue

def execute_llm_call(conversation: List[Dict[str, Any]]) -> Dict[str, Any]:
    response = openai_client.chat.completions.create(
        model="gpt-5",
        messages=conversation,
        max_completion_tokens=2000
    )
    return response.choices[0].message.content

def run_coding_agent_loop():
    conversation = [{
        "role": "system",
        "content": get_full_system_prompt()
    }]

    while True:
        try:
            user_input = input(YOU_COLOR + "User: " + RESET_COLOR)
        except (KeyboardInterrupt, EOFError):
            break
        conversation.append({
            "role": "user",
            "content": user_input.strip()
        })
    while True:
        assistant_response = execute_llm_call(conversation)
        tool_invocations = extract_tool_invocation(assistant_response)
        if not tool_invocations:
            print(f"{ASSISTANT_COLOR}Assistant:{RESET_COLOR}: {assistant_response}")
            conversation.append({
                "role": "assistant",
                "content": assistant_response
            })
            break
        for tool_name, args in tool_invocations:
            tool = TOOL_REGISTRY[tool_name]
            resp = ""
            print(tool_name, args)
            if tool_name == "read_file":
                resp = tool(args.get("filename", "."))
            elif tool_name == "list_files":
                resp = tool(args.get("path", "."))
            elif tool_name == "edit_file":
                resp = tool(args.get("path", "."), 
                            args.get("old_str", ""), 
                            args.get("new_str", ""))
            conversation.append({
                "role": "user",
                "content": f"tool_result({json.dumps(resp)})"
            })

if __name__ == "__main__":
    run_coding_agent_loop()
