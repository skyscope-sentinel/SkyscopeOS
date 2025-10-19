# File: docker_mcp_integration.py

import docker
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

client = docker.from_env()
app = FastAPI()

class ExecCommand(BaseModel):
    cmd: str

def list_mcp_containers():
    containers = client.containers.list()
    mcp_containers = []
    for cont in containers:
        if "mcp" in cont.name.lower():
            mcp_containers.append({
                "id": cont.id,
                "name": cont.name,
                "image": cont.image.tags[0] if cont.image.tags else "unknown",
                "status": cont.status,
                "ports": cont.attrs.get('NetworkSettings', {}).get('Ports', {})
            })
    return mcp_containers

@app.get("/mcp/containers")
def api_list_mcp_containers():
    try:
        return {"containers": list_mcp_containers()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/mcp/{container_id}/exec")
def api_execute_command(container_id: str, command: ExecCommand):
    try:
        cont = client.containers.get(container_id)
        exec_result = cont.exec_run(command.cmd, stdout=True, stderr=True)
        return {"output": exec_result.output.decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
