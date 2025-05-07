# Mythic MCP

A quick MCP demo for Mythic, allowing LLMs to pentest on our behalf!

## Requirements

1. uv
2. python3
3. Claude Desktop (or other MCP Client)
4. Mythic C2 server running

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mythic_mcp.git
cd mythic_mcp
```

2. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your Mythic C2 server details:
```env
# Mythic MCP Server Configuration
MYTHIC_MCP_PORT=8888
MYTHIC_MCP_HOST=127.0.0.1

# Mythic API Configuration
MYTHIC_API_USERNAME=mythic_admin
MYTHIC_API_PASSWORD=your_password_here
MYTHIC_API_HOST=localhost
MYTHIC_API_PORT=7443
```

4. Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Usage with Claude Desktop

To deploy this MCP Server with Claude Desktop, you'll need to edit your `claude_desktop_config.json` to add the following:

```json
{
    "mcpServers": {
        "mythic_mcp": {
            "command": "uv",
            "args": [
                "--directory",
                "/full/path/to/mythic_mcp/",
                "run",
                "main.py",
            ]
        }
    }
}
```

Once done, kick off Claude Desktop. There are sample prompts to show how to task the LLM, but really anything will work along the lines of:

```
You are an automated pentester, tasked with emulating a specific threat actor. The threat actor is APT31. Your objective is: Add a flag to C:\win.txt on DC01. Perform any required steps to meet the objective, using only techniques documented by the threat actor.
```
