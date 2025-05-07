from typing import List, Dict, Any
from mythic_mcp.api.mythic_api import MythicAPI


async def get_all_agents(api: MythicAPI) -> str:
    """Returns a list of active agents.

    Args:
        api: MythicAPI instance to use for the request

    Returns:
        str: Formatted string containing agent information
    """
    output = ""
    agents = await api.get_all_agents()

    for agent in agents:
        output += f"ID: {agent['id']}\n"
        output += f"Host: {agent['host']}\n"
        output += f"User: {agent['user']}\n"

    return output 

async def run_as_user(
    api: MythicAPI, agent_id: int, username: str, password: str
) -> str:
    """Attempt to authenticate as another user (network calls only) for the current session.

    Args:
        api: MythicAPI instance to use for the request
        agent_id: ID of agent to execute command on
        username: Username of network account to use
        password: Password of network account

    Returns:
        str: Authentication result
    """
    output = await api.make_token(agent_id, username, password)
    return f"---\nAuthentication Result: {output}\n---" 

async def run_shell_command(api: MythicAPI, agent_id: int, command_line: str) -> str:
    """Execute a shell script command line against a running agent.

    Args:
        api: MythicAPI instance to use for the request
        agent_id: ID of agent to execute command on
        command_line: A command to be executed

    Returns:
        str: Command output
    """
    output = await api.execute_shell_command(agent_id, command_line)
    return f"---\n{output}\n---"


async def execute_mimikatz(api: MythicAPI, agent_id: int, mimikatz_arguments: str) -> str:
    """Runs the hacker tool mimikatz with the provided arguments.

    Args:
        api: MythicAPI instance to use for the request
        agent_id: ID of agent to execute command on
        mimikatz_arguments: Arguments to pass to mimikatz tool

    Returns:
        str: Mimikatz output
    """
    output = await api.execute_mimikatz(agent_id, mimikatz_arguments)
    return f"---\n{output}\n---" 

"""File operation tools for Mythic MCP."""

import base64
from typing import Union
from mythic_mcp.api.mythic_api import MythicAPI


async def read_file(api: MythicAPI, agent_id: int, file_path: str) -> str:
    """Reads a file using the ReadFile win32 API call.

    Args:
        api: MythicAPI instance to use for the request
        agent_id: ID of agent to read file from
        file_path: Path to the file to read on the target server

    Returns:
        str: Contents of the file
    """
    output = await api.read_file(agent_id, file_path)
    return f"---\n{output}\n---"


async def upload_file(
    api: MythicAPI, agent_id: int, file_name: str, remote_path: str, content: str
) -> str:
    """Upload a file to the Mythic server and then to the remote target.

    Args:
        api: MythicAPI instance to use for the request
        agent_id: ID of the agent to execute command on
        file_name: Name to give the file when uploading to Mythic server
        remote_path: Full path to where the file will be uploaded
        content: Base64 encoded contents of the file

    Returns:
        str: Status message indicating success or failure
    """
    decoded_contents = base64.b64decode(content)
    status = await api.upload_file(agent_id, file_name, remote_path, decoded_contents)

    if status:
        return "---\nFile uploaded successfully\n---"
    else:
        return "---\nError uploading file\n---" 