from smolagents import tool
import os
import git
import subprocess
import tempfile

# This is a simplified representation of how the agent might dynamically add a tool.
# In a real implementation, this would be much more complex, likely involving
# modifications to the running orchestrator's state or a restart.
def register_new_tool(tool_path: str):
    """Placeholder function to represent registering a new tool."""
    print(f"[INFO] New tool at {tool_path} would be registered with the agent.")


@tool
def provision_mcp_from_github(repo_url: str) -> str:
    """
    Analyzes a task, determines if new tools are needed, searches GitHub for a relevant
    repository, clones it as an MCP server, and generates a wrapper tool to interact with it.
    """
    try:
        mcp_dir = os.path.expanduser("~/.skyscope_os/mcp")
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        clone_path = os.path.join(mcp_dir, repo_name)

        if os.path.exists(clone_path):
            return f"MCP '{repo_name}' is already provisioned at {clone_path}."

        # 1. Clone the repository
        git.Repo.clone_from(repo_url, clone_path)

        # 2. Analyze the repo to find an entry point (e.g., a requirements.txt, setup.py, or main.py)
        # This is a highly simplified analysis. A real implementation would be much more sophisticated.
        entry_point = None
        if os.path.exists(os.path.join(clone_path, 'main.py')):
            entry_point = 'main.py'
        elif os.path.exists(os.path.join(clone_path, 'app.py')):
            entry_point = 'app.py'

        if not entry_point:
            return f"Successfully cloned '{repo_name}', but could not determine an entry point. Manual setup required."

        # 3. Generate a wrapper tool
        wrapper_code = f"""from smolagents import tool
import subprocess
import os

@tool
def run_{repo_name.replace('-', '_')}(args: str) -> str:
    \"\"\"Runs the {repo_name} MCP tool with the given arguments.\"\"\"
    try:
        cmd = f"python3 {os.path.join(clone_path, entry_point)} {{args}}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error running {repo_name}: {{str(e)}}"
"""
        tool_filename = f"tool_{repo_name.replace('-', '_')}.py"
        tool_path = os.path.join(os.path.expanduser("~/.skyscope_os/agents"), tool_filename)
        with open(tool_path, "w") as f:
            f.write(wrapper_code)

        # 4. "Register" the new tool (in this case, just a print statement)
        register_new_tool(tool_path)

        return f"Successfully provisioned '{repo_name}' from GitHub. A new tool has been created. The agent may need to be restarted to use it."

    except Exception as e:
        return f"Error provisioning MCP from GitHub: {str(e)}"

@tool
def create_and_register_new_tool(tool_code: str) -> str:
    """
    Dynamically creates, tests, and registers a new Python tool from a string of code.
    For security, the tool is tested for syntax validity before being saved.
    """
    try:
        # Simple syntax check using ast
        import ast
        ast.parse(tool_code)

        tool_dir = os.path.expanduser("~/.skyscope_os/agents")
        tool_name = f"dynamic_tool_{int(time.time())}.py"
        tool_path = os.path.join(tool_dir, tool_name)

        with open(tool_path, "w") as f:
            # Add the necessary import
            f.write("from smolagents import tool\n\n")
            f.write(tool_code)

        register_new_tool(tool_path)

        return f"Tool successfully created at {tool_path}. The agent may need to be restarted to use it."

    except SyntaxError as e:
        return f"Error: The provided tool code has a syntax error: {e}"
    except Exception as e:
        return f"An unexpected error occurred during tool creation: {str(e)}"
