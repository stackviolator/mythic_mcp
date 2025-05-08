from mythic_mcp.api.mythic_api import MythicAPI
from mythic.mythic import mythic_utilities, graphql_queries
import mythic_mcp.api.graphql_queries as mcp_graphql_queries
import base64
from typing import Optional

async def init_api(username, password, host, port):
    """Initializes the Mythic API. Ran at server startup automatically.
    TODO, this should have error handling. But there's like 4 layers of abstraction :(
    Args:
        username: Username of the Mythic server
        password: Password of the Mythic server
        host: Host of the Mythic server
        port: Port of the Mythic server

    Returns:

    """
    global api
    api = MythicAPI(username, password, host, port) 
    await api.connect()

async def get_all_agents() -> str:
    """Returns a list of active agents.

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

async def get_cmd_help_message(agent_id: int, command_name: str) -> str:
    """Returns a list of help commands for a given agent.

    Args:
        agent_id: ID of the agent to get help for
        command_name: Optional name of specific command to get help for. If not provided, returns help for all commands.

    Returns:
        str: Formatted string containing help commands
    """
    return await api.get_cmd_help_message(agent_id, command_name)


async def issue_task(agent_id: int, command_name: str, parameters: str) -> str:
    """Issues a task and waits for the task to complete.

    Args:
        agent_id: ID of the agent to issue task to
        command_name: Name of the command to issue
        parameters: Parameters to pass to the command
    """
    return await api.issue_task(agent_id, command_name, parameters) 

async def get_loaded_commands(agent_id: int) -> str:
    """Returns a list of loaded commands for a given agent.

    Args:
        agent_id: ID of the agent to get commands for

    Returns:
        str: Formatted string containing loaded commands
    """
    mythic = api.mythic_instance
    
    # Set up variables for the query
    variables = {"callback_id": agent_id}
    
    try:
        # Execute the GraphQL subscription
        async for result in mythic_utilities.graphql_subscription(
            mythic=mythic,
            query=mcp_graphql_queries.GET_LOADED_COMMANDS,
            variables=variables
        ):
            # Format the output
            output = "Loaded Commands:\n"
            for cmd in result.get("loadedcommands", []):
                command = cmd.get("command", {})
                output += f"\nCommand: {command.get('cmd', 'N/A')}\n"
                output += f"ID: {command.get('id', 'N/A')}\n"
                output += f"Payload Type: {command.get('payloadtype', {}).get('name', 'N/A')}\n"
                
                # Add parameters if they exist
                params = command.get("commandparameters", [])
                if params:
                    output += "Parameters:\n"
                    for param in params:
                        output += f"  - {param.get('name', 'N/A')}: {param.get('parameter_type', 'N/A')}\n"
                        if param.get("required"):
                            output += "    (Required)\n"
                
                output += "---\n"
            
            return output
            
    except Exception as e:
        return f"Error getting loaded commands: {str(e)}"
    
async def run_as_user(
    agent_id: int, username: str, password: str
) -> str:
    """Attempt to authenticate as another user (network calls only) for the current session.

    Args:
        agent_id: ID of agent to execute command on
        username: Username of network account to use
        password: Password of network account

    Returns:
        str: Authentication result
    """
    output = await api.make_token(agent_id, username, password)
    return f"---\nAuthentication Result: {output}\n---" 

async def read_file(agent_id: int, file_path: str) -> str:
    """Reads a file using the ReadFile win32 API call.

    Args:
        agent_id: ID of agent to read file from
        file_path: Path to the file to read on the target server

    Returns:
        str: Contents of the file
    """
    output = await api.read_file(agent_id, file_path)
    return f"---\n{output}\n---"

async def upload_file(
    agent_id: int, file_name: str, remote_path: str, content: str
) -> str:
    """Upload a file to the Mythic server and then to the remote target.

    Args:
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