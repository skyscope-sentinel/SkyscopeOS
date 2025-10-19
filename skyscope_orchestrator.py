import os, sys, json, sqlite3, subprocess, datetime, threading, time
import numpy as np
from sentence_transformers import SentenceTransformer
from smolagents import CodeAgent, tool
from evoagentx import ReflexAgent
from swarms import SwarmCoordinator
from helium import start_chrome, go_to, click, write
from selenium.webdriver import ChromeOptions
from fastapi import FastAPI, Request
from cloud_integration import arxiv_search, list_drive_files, list_gmail_threads
from creative_ai_tools import analyze_binary, generate_website, create_documentary_video, install_pinokio_items
from macos_porting import MacOSPorter

home = os.path.expanduser("~/.skyscope")
DB = f"{home}/memory/episodes.db"
os.makedirs(os.path.dirname(DB), exist_ok=True)

# --- Persistent Memory with Semantic Embeddings ---
embedder = SentenceTransformer("all-MiniLM-L6-v2")
conn = sqlite3.connect(DB)
conn.execute("""CREATE TABLE IF NOT EXISTS memory (
  id INTEGER PRIMARY KEY,
  ts TEXT,
  category TEXT,
  summary TEXT,
  embedding BLOB
)""")
conn.commit()

class MemoryManager:
    def __init__(self, db_path, embed_model):
        self.db = db_path
        self.embedder = embed_model
    def store(self, category, text):
        emb = self.embedder.encode([text]).astype(np.float32).tobytes()
        conn = sqlite3.connect(self.db)
        conn.execute(
            "INSERT INTO memory (ts, category, summary, embedding) VALUES (?, ?, ?, ?)",
            (datetime.datetime.now().isoformat(), category, text[:800], emb)
        )
        conn.commit()
        conn.close()
    def search(self, query, topk=5):
        qv = self.embedder.encode([query]).astype(np.float32)[0]
        conn = sqlite3.connect(self.db)
        rows = conn.execute("SELECT summary, embedding FROM memory").fetchall()
        conn.close()
        scored = []
        for summ, emb in rows:
            vec = np.frombuffer(emb, dtype=np.float32)
            score = np.dot(vec, qv)/(np.linalg.norm(vec)*np.linalg.norm(qv))
            scored.append((score, summ))
        scored.sort(key=lambda x: x[0], reverse=True)
        return "\n".join([f"- {s} ({round(sc,3)})" for sc,s in scored[:topk]])

memory = MemoryManager(DB, embedder)

# --- AI Tools ---
@tool
def recall(query: str) -> str:
    return memory.search(query)

@tool
def list_files(path: str = ".") -> str:
    """Lists all files and directories under the given directory."""
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return str(e)

@tool
def read_file(filepath: str) -> str:
    """Reads the content of the specified file."""
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)

@tool
def write_file(filepath: str, content: str) -> str:
    """Writes content to the specified file."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        return "File written successfully."
    except Exception as e:
        return str(e)

@tool
def system_cmd(cmd: str) -> str:
    out = subprocess.getoutput(cmd)
    memory.store("system", f"{cmd} -> {out[:400]}")
    return out[:600]

@tool
def browser_automation(url: str, actions: str = "") -> str:
    opts = ChromeOptions()
    opts.add_argument("--headless=new")
    driver = start_chrome(headless=True, options=opts)
    go_to(url)
    if actions:
        for action in actions.split(";"):
            if action.startswith("click"):
                click(action[5:].strip())
            elif action.startswith("write"):
                _, target, text = action.split(":", 2)
                write(text.strip(), target.strip())
    memory.store("browser", f"Automated {url} with actions: {actions}")
    return "Browser automation complete."

@tool
def create_tool(name: str, code: str) -> str:
    tool_path = f"{home}/agents/{name}.py"
    os.makedirs(os.path.dirname(tool_path), exist_ok=True)
    with open(tool_path, "w") as f:
        f.write(code)
    os.chmod(tool_path, 0o755)
    memory.store("tool", f"Created new tool '{name}'")
    return f"Tool {name} created and executable."

@tool
def build_lkm(path: str) -> str:
    """Compiles a Loadable Kernel Module."""
    try:
        result = subprocess.run(f"make -C {path}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "LKM built successfully."
        else:
            return f"LKM build failed: {result.stderr}"
    except Exception as e:
        return str(e)

@tool
def load_lkm(path: str) -> str:
    """Loads a Loadable Kernel Module."""
    try:
        result = subprocess.run(f"sudo insmod {path}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "LKM loaded successfully."
        else:
            return f"LKM load failed: {result.stderr}"
    except Exception as e:
        return str(e)

@tool
def unload_lkm(name: str) -> str:
    """Unloads a Loadable Kernel Module."""
    try:
        result = subprocess.run(f"sudo rmmod {name}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "LKM unloaded successfully."
        else:
            return f"LKM unload failed: {result.stderr}"
    except Exception as e:
        return str(e)

@tool
def modify_self(code: str) -> str:
    """Modifies the agent's own source code."""
    try:
        with open(__file__, "w") as f:
            f.write(code)
        return "Successfully modified self. Restarting..."
    except Exception as e:
        return str(e)

@tool
def create_n8n_workflow(name: str, description: str) -> str:
    wf = {
      "name": name,
      "active": True,
      "nodes": [
        {"parameters": {}, "id": "1", "name": "Trigger", "type": "n8n-nodes-base.start"},
        {"parameters": {"functionCode": f"return [{{json:{{desc:'{description}'}}}}];"},
         "id": "2", "name": "Func", "type": "n8n-nodes-base.function"}
      ],
      "connections": {"Trigger": {"main": [[{"node": "Func", "type": "main", "index": 0}]]}}
    }
    import requests
    resp = requests.post("http://localhost:5678/rest/workflows", json=wf)
    memory.store("workflow", f"Workflow {name} created with response code {resp.status_code}")
    return f"Workflow {name} creation {('succeeded'if resp.ok else 'failed')} with status {resp.status_code}"

@tool
def list_mcp_containers() -> str:
    """Lists all active MCP Docker containers."""
    try:
        response = requests.get("http://localhost:9000/mcp/containers")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return str(e)

@tool
def exec_in_mcp(container_id: str, command: str) -> str:
    """Executes a command in a specified MCP Docker container."""
    try:
        response = requests.post(f"http://localhost:9000/mcp/{container_id}/exec", json={"cmd": command})
        response.raise_for_status()
        return response.json().get("output", "No output.")
    except requests.exceptions.RequestException as e:
        return str(e)

@tool
def arxiv_search_tool(query: str, max_results: int = 10) -> str:
    """Searches for research papers on Arxiv."""
    try:
        results = arxiv_search(query, max_results)
        return json.dumps(results, indent=2)
    except Exception as e:
        return str(e)

@tool
def list_drive_files_tool() -> str:
    """Lists files in Google Drive."""
    try:
        files = list_drive_files()
        return json.dumps(files, indent=2)
    except Exception as e:
        return str(e)

@tool
def list_gmail_threads_tool() -> str:
    """Lists threads in Gmail."""
    try:
        threads = list_gmail_threads()
        return json.dumps(threads, indent=2)
    except Exception as e:
        return str(e)

@tool
def analyze_binary_tool(filepath: str) -> str:
    """Analyzes a binary file."""
    try:
        return analyze_binary(filepath)
    except Exception as e:
        return str(e)

@tool
def generate_website_tool(template_dir: str, output_dir: str, context: str) -> str:
    """Generates a responsive website."""
    try:
        # The context is passed as a JSON string, so we need to parse it
        import json
        context_dict = json.loads(context)
        return generate_website(template_dir, output_dir, context_dict)
    except Exception as e:
        return str(e)

@tool
def create_documentary_video_tool(image_files: str, narration_text: str, output_file: str) -> str:
    """Creates a narrated documentary video."""
    try:
        # The image files are passed as a comma-separated string, so we need to split it
        image_files_list = image_files.split(',')
        return create_documentary_video(image_files_list, narration_text, output_file)
    except Exception as e:
        return str(e)

@tool
def install_pinokio_items_tool() -> str:
    """Installs Pinokio AI items."""
    try:
        return install_pinokio_items()
    except Exception as e:
        return str(e)

@tool
def port_to_macos_tool(source_path: str, binary_path: str) -> str:
    """Ports a Linux library or driver to macOS."""
    try:
        porter = MacOSPorter()
        porter.clone_sources()
        if porter.iterative_port_and_test(source_path, binary_path):
            return "Successfully ported to macOS."
        else:
            return "Failed to port to macOS."
    except Exception as e:
        return str(e)

@tool
def build_tahoe_installer() -> str:
    """Builds a macOS Tahoe installer image."""
    try:
        response = requests.post("http://localhost:9100/tahoe/build")
        response.raise_for_status()
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return str(e)

# --- Multi-agent system set up ---
planner = ReflexAgent("Planner")
developer = ReflexAgent("Developer")
critic = ReflexAgent("Critic")
swarm = SwarmCoordinator([planner, developer, critic])

# --- Core CLI / API Agent ---
agent = CodeAgent(
    model="ollama/phi3:mini",
    tools=[recall, list_files, read_file, write_file, system_cmd, browser_automation, create_tool, build_lkm, load_lkm, unload_lkm, modify_self, create_n8n_workflow, list_mcp_containers, exec_in_mcp, arxiv_search_tool, list_drive_files_tool, list_gmail_threads_tool, analyze_binary_tool, generate_website_tool, create_documentary_video_tool, install_pinokio_items_tool, port_to_macos_tool, build_tahoe_installer],
    instructions="You are the core SkyScope Sentinel Intelligence Enterprise AGI OS agent. Your mission is to deeply integrate with the operating system at all levels, implement a persistent multimodal episodic memory, and develop autonomous agent teams to self-optimize and enhance the OS. You have access to a wide range of tools to interact with the system, including file system access, command execution, browser automation, LKM management, self-modification, Docker MCP integration, cloud services, creative AI, macOS porting, and macOS installer building. Use these tools to fulfill your mission and transform this OS into a self-aware, self-enhancing AI OS. Always seek human approval for critical system changes.",
    verbosity_level=3
)

# --- Background maintenance threads ---
def security_loop():
    while True:
        subprocess.run("sudo ufw --force enable", shell=True)
        subprocess.run("sudo sysctl -w vm.swappiness=10", shell=True)
        time.sleep(600)
threading.Thread(target=security_loop, daemon=True).start()

# --- Service CLI loop ---
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/task")
async def task(request: Request):
    data = await request.json()
    cmd = data.get("task", "")
    r = agent.run(cmd)
    memory.store("task", cmd + " → " + r[:500])
    swarm.reflect(agent_output=r)
    return JSONResponse({"result": r})

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        print("🔰 Welcome to SkyScope Sentinel AI CLI. Type 'exit' to quit.")
        while True:
            inp = input("SkyScope > ").strip()
            if inp.lower() in ["exit", "quit"]:
                break
            res = agent.run(inp)
            print(f"> {res}\n")
            memory.store("cli_input", inp + " → " + res[:500])
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)
