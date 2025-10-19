import json
import subprocess
from smolagents import tool

@tool
def create_n8n_workflow(name: str, nodes_json: str) -> str:
    """
    Creates and activates an n8n workflow from a JSON definition.
    'nodes_json' should be a JSON string representing the 'nodes' and 'connections' objects.
    Example: '{"nodes": [...], "connections": {...}}'
    """
    try:
        workflow_data = json.loads(nodes_json)
        if 'nodes' not in workflow_data or 'connections' not in workflow_data:
            return "Error: JSON must contain 'nodes' and 'connections' keys."

        workflow = {
            "name": name,
            "active": True,
            "nodes": workflow_data['nodes'],
            "connections": workflow_data['connections']
        }

        wf_str = json.dumps(workflow)
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", "http://localhost:5678/rest/workflows",
             "-H", "Content-Type: application/json", "-d", wf_str],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            return f"Error creating workflow: {result.stderr}"

        response_json = json.loads(result.stdout)
        if 'id' in response_json:
            return f"Workflow '{name}' created successfully with ID: {response_json['id']}"
        else:
            return f"Failed to create workflow. Response: {result.stdout}"

    except json.JSONDecodeError:
        return "Error: Invalid JSON provided for nodes_json."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
