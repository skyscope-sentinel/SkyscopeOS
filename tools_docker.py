from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import docker
from smolagents import tool
import requests
import json

class ExecCommand(BaseModel):
    cmd: str

def _get_docker_client():
    """Initializes and returns a Docker client."""
    try:
        return docker.from_env()
    except docker.errors.DockerException:
        return None

@tool
def list_mcp_containers() -> str:
    """Lists running Docker containers that are potential MCP servers (named with 'mcp')."""
    client = _get_docker_client()
    if not client:
        return "Error: Docker daemon is not running or accessible."

    try:
        containers = client.containers.list()
        mcp_containers = []
        for cont in containers:
            if "mcp" in cont.name.lower():
                mcp_containers.append({
                    "id": cont.short_id,
                    "name": cont.name,
                    "image": cont.image.tags[0] if cont.image.tags else "unknown",
                    "status": cont.status,
                })
        if not mcp_containers:
            return "No MCP-named Docker containers found."
        return json.dumps(mcp_containers, indent=2)
    except Exception as e:
        return f"Error listing containers: {str(e)}"

@tool
def exec_in_container(container_id: str, command: str) -> str:
    """Executes a command inside a specific Docker container."""
    client = _get_docker_client()
    if not client:
        return "Error: Docker daemon is not running or accessible."

    try:
        container = client.containers.get(container_id)
        exit_code, output = container.exec_run(command)
        decoded_output = output.decode('utf-8')
        if exit_code == 0:
            return f"Command executed successfully:\n{decoded_output}"
        else:
            return f"Command failed with exit code {exit_code}:\n{decoded_output}"
    except docker.errors.NotFound:
        return f"Error: Container '{container_id}' not found."
    except Exception as e:
        return f"Error executing command in container: {str(e)}"

# Note: The FastAPI server part is removed from this file.
# The tools can be directly imported and used by the orchestrator.
# If a separate service is desired, the FastAPI code from the plan can be added back here
# and the tools would be reimplemented as API clients. This direct-import approach is simpler.
