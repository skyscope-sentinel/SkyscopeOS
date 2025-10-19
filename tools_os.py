import os
import subprocess
from smolagents import tool

home = os.path.expanduser("~/.skyscope_unified")

@tool
def list_files(path: str = ".") -> str:
    """Lists all files and directories under the given directory."""
    try:
        if not os.path.isdir(path):
            return f"Error: Path '{path}' is not a valid directory."
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Error listing files: {str(e)}"

@tool
def read_file(filepath: str) -> str:
    """Reads the content of the specified file."""
    try:
        if not os.path.isfile(filepath):
            return f"Error: File '{filepath}' does not exist."
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@tool
def write_file(filepath: str, content: str) -> str:
    """Writes content to the specified file."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return f"File '{filepath}' written successfully."
    except Exception as e:
        return f"Error writing file: {str(e)}"

@tool
def system_cmd(cmd: str) -> str:
    """Executes a shell command and returns its output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        return output[:2000]
    except Exception as e:
        return f"Error executing command: {str(e)}"

@tool
def build_lkm(path: str) -> str:
    """Compiles a Loadable Kernel Module."""
    try:
        if not os.path.isdir(path):
            return f"Error: Path '{path}' is not a valid directory."
        result = subprocess.run(f"make -C {path}", shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return "LKM built successfully."
        else:
            return f"LKM build failed: {result.stderr}"
    except Exception as e:
        return f"Error building LKM: {str(e)}"

@tool
def load_lkm(path: str) -> str:
    """Loads a Loadable Kernel Module. Requires sudo privileges."""
    try:
        if not os.path.isfile(path):
            return f"Error: LKM file '{path}' does not exist."
        result = subprocess.run(f"sudo insmod {path}", shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return "LKM loaded successfully."
        else:
            return f"LKM load failed: {result.stderr}"
    except Exception as e:
        return f"Error loading LKM: {str(e)}"

@tool
def unload_lkm(name: str) -> str:
    """Unloads a Loadable Kernel Module. Requires sudo privileges."""
    try:
        result = subprocess.run(f"sudo rmmod {name}", shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return "LKM unloaded successfully."
        else:
            return f"LKM unload failed: {result.stderr}"
    except Exception as e:
        return f"Error unloading LKM: {str(e)}"

@tool
def modify_self(filepath: str, code: str) -> str:
    """Modifies the agent's own source code at the specified filepath."""
    try:
        # A simple safeguard: only allow modification of files within the agent's home directory
        if not filepath.startswith(home):
            return "Error: For security, can only modify files within the agent's home directory."
        with open(filepath, "w") as f:
            f.write(code)
        return f"Successfully modified {filepath}. A restart may be required for changes to take effect."
    except Exception as e:
        return f"Error modifying self: {str(e)}"
