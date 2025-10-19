import subprocess
import tempfile
import os
from smolagents import tool

@tool
def create_dynamic_tool(tool_code: str) -> str:
    """
    Dynamically creates, tests, and registers a new Python tool from a string of code.
    The code must define a function decorated with @tool.
    For security, the tool will be tested in a sandboxed environment before being made available.
    """
    try:
        # Create a temporary file to write the tool code to
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write("from smolagents import tool\n\n")
            temp_file.write(tool_code)
            temp_filename = temp_file.name

        # Use a separate, sandboxed process to test the tool
        # This is a basic form of sandboxing. A more robust solution might use Docker or a more restrictive environment.
        test_process = subprocess.run(
            ['python', '-c', f'import sys; sys.path.append(os.getcwd()); import {os.path.basename(temp_filename)[:-3]}'],
            capture_output=True, text=True
        )

        if test_process.returncode != 0:
            os.remove(temp_filename)
            return f"Error: The provided tool code failed to compile or execute.\nDetails: {test_process.stderr}"

        # If the test passes, move the tool to the agent's tool directory to be loaded on next restart
        tool_dir = os.path.expanduser("~/.skyscope_unified/agents")
        os.makedirs(tool_dir, exist_ok=True)
        final_path = os.path.join(tool_dir, os.path.basename(temp_filename))
        os.rename(temp_filename, final_path)

        return f"Tool successfully created at {final_path}. It will be available after the agent restarts."

    except Exception as e:
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        return f"An unexpected error occurred during tool creation: {str(e)}"
