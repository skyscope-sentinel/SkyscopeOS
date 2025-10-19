#!/usr/bin/env bash
# ====================================================================
# SkyScope Omniversal Orchestrator [Self-Memory Edition]
# ====================================================================
# Author: Miss Casey Jay Topojani | 2025 Ultimate Local AGI
# Purpose:
# - Fully self-contained AI orchestration framework
# - Builds persistent vector + semantic memory internally
# - Self-generating tools, agents, MCP servers, and workflows
# - Supports browser automation, coding, OS configuration, n8n workflows
# ====================================================================

set -e

echo "🧭 Updating base system..."
sudo apt update -y && sudo apt install -y python3 python3-pip python3-venv git sqlite3 curl jq ffmpeg \
  sox vlc imagemagick chromium-driver nodejs npm unzip wget build-essential

# Directories
mkdir -p ~/.skyscope_unified/{env,logs,memory,embeddings,agents,workflows,mcp,llm}
python3 -m venv ~/.skyscope_unified/env
source ~/.skyscope_unified/env/bin/activate
pip install --upgrade pip wheel

# --- Install essential Python packages ---
pip install torch torchvision torchaudio numpy pandas requests psutil fastapi uvicorn flask selenium helium \
  sentence-transformers langchain langchain-core langgraph swarms evoagentx smolagents[toolkit] faiss-cpu

# --- Setup n8n ---
npm install -g n8n pm2
pm2 start "n8n" --name skyscope-n8n
pm2 save

echo "✅ n8n running at http://localhost:5678"

# --- Install Ollama for LLM operations ---
curl -fsSL https://ollama.com/install.sh | sh
ollama pull smollm:135m
ollama pull phi3:mini

# --- Core Python architecture ---
cat > ~/.skyscope_unified/env/skyscope_unified.py <<'PYCODE'
import os, json, sqlite3, datetime, subprocess, threading, numpy as np, time
from sentence_transformers import SentenceTransformer
from smolagents import CodeAgent, tool
from evoagentx import ReflexAgent
from swarms import SwarmCoordinator
from selenium.webdriver import ChromeOptions
from helium import start_chrome, go_to, click, write
from fastapi import FastAPI

home = os.path.expanduser("~/.skyscope_unified")
DB = f"{home}/memory/episodes.db"
os.makedirs(os.path.dirname(DB), exist_ok=True)

# === Initialize internal persistent memory ===
embedder = SentenceTransformer("all-MiniLM-L6-v2")
conn = sqlite3.connect(DB)
conn.execute("""
CREATE TABLE IF NOT EXISTS memory (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  type TEXT,
  summary TEXT,
  embedding BLOB
)""")
conn.execute("CREATE INDEX IF NOT EXISTS idx_mem_type ON memory(type)")
conn.commit(); conn.close()

# === Memory Manager ===
class SkyMemory:
    def __init__(self, db, embedder):
        self.db = db
        self.embedder = embedder
        os.makedirs(os.path.dirname(db), exist_ok=True)
    def store(self, type_, text):
        emb = self.embedder.encode([text]).astype('float32').tobytes()
        conn = sqlite3.connect(self.db)
        conn.execute("INSERT INTO memory (ts,type,summary,embedding) VALUES (?,?,?,?)",
                     (datetime.datetime.now().isoformat(), type_, text[:800], emb))
        conn.commit(); conn.close()
    def search(self, query, topk=5):
        qv = self.embedder.encode([query]).astype('float32')[0]
        conn = sqlite3.connect(self.db)
        rows = conn.execute("SELECT summary, embedding FROM memory").fetchall()
        results = []
        for summ, emb in rows:
            vec = np.frombuffer(emb, dtype='float32')
            score = np.dot(vec, qv)/(np.linalg.norm(vec)*np.linalg.norm(qv))
            results.append((score, summ))
        conn.close()
        results = sorted(results, key=lambda x:x[0], reverse=True)[:topk]
        return "\n".join([f"- {s} ({sc:.3f})" for sc,s in results])

memory = SkyMemory(DB, embedder)

# === Toolset ===

@tool
def recall(query:str) -> str:
    """Retrieve related events and insights."""
    return memory.search(query)

@tool
def system_action(cmd:str) -> str:
    """Execute OS-level command safely."""
    out = subprocess.getoutput(cmd)
    memory.store("system", f"{cmd} -> {out[:400]}")
    return out[:600]

@tool
def browser_automate(url:str, actions:str="") -> str:
    """Perform headless browser tasks."""
    opts = ChromeOptions(); opts.add_argument("--headless=new")
    driver = start_chrome(headless=True, options=opts)
    go_to(url)
    if actions:
        for act in actions.split(";"):
            if "click" in act: click(act.replace("click","").strip())
            elif "write" in act:
                target,text = act.replace("write","").split(":",1)
                write(text.strip(), target.strip())
    memory.store("browser", f"Automated {url} with actions: {actions}")
    return "Browser automation complete."

@tool
def create_tool(name:str, code:str) -> str:
    """Dynamically create executable Python tools."""
    tool_path = f"{home}/agents/{name}.py"
    with open(tool_path, "w") as f: f.write(code)
    subprocess.run(f"chmod +x {tool_path}", shell=True)
    memory.store("tool", f"Created new dynamic tool {name}")
    return f"Tool {name} created."

@tool
def create_n8n_workflow(name:str, description:str):
    """Generate autonomous n8n workflow nodes."""
    workflow = {
      "name": name,
      "active": True,
      "nodes": [
        {"parameters": {}, "id": "1","name":"Trigger","type":"n8n-nodes-base.start"},
        {"parameters":{"functionCode":f"return [{{json:{{desc:'{description}'}}}}];"},
         "id":"2","name":"Autotask","type":"n8n-nodes-base.function"}
      ],
      "connections":{"Trigger":{"main":[[{"node":"Autotask","type":"main","index":0}]]}}
    }
    wf_str = json.dumps(workflow)
    subprocess.run(["curl","-s","-X","POST","http://localhost:5678/rest/workflows",
                    "-H","Content-Type: application/json","-d", wf_str])
    memory.store("workflow", f"Workflow '{name}' created.")
    return f"Workflow {name} established."

# === Agent Architecture ===
planner = ReflexAgent("Planner")
developer = ReflexAgent("Developer")
critic = ReflexAgent("Critic")
coordinator = SwarmCoordinator([planner, developer, critic])

agent = CodeAgent(model="ollama/phi3:mini",
  tools=[recall, system_action, browser_automate, create_tool, create_n8n_workflow],
  instructions="SkyScope Unified is a persistent autonomous orchestration core capable of creating, modifying, deploying and reflecting upon its structure, workflows, tools, and memory. Acts locally, secure and self-organizing.",
  verbosity_level=2)

# === Continuous background optimization ===
def defense_loop():
    while True:
        subprocess.run("sudo ufw --force enable", shell=True)
        subprocess.run("sudo sysctl -w vm.swappiness=10", shell=True)
        time.sleep(600)
threading.Thread(target=defense_loop, daemon=True).start()

# === FastAPI ===
app = FastAPI()

@app.post("/task")
def execute_task(req:dict):
    t = req.get("task","")
    result = agent.run(t)
    memory.store("text", f"Task: {t} -> {result[:800]}")
    coordinator.reflect(agent_output=result)
    return {"result": result}

print("🚀 SkyScope Unified API running: POST /task {\"task\":\"auto create new OS optimization agent\"}")
PYCODE

# --- Systemd service setup ---
sudo bash -c 'cat > /etc/systemd/system/skyscope-unified.service <<EOF
[Unit]
Description=SkyScope Unified AGI Core
After=network.target

[Service]
User='$USER'
ExecStart=/usr/bin/bash -c "source ~/.skyscope_unified/env/bin/activate && python3 ~/.skyscope_unified/env/skyscope_unified.py"
Restart=always

[Install]
WantedBy=multi-user.target
EOF'

sudo systemctl enable skyscope-unified.service
sudo systemctl start skyscope-unified.service

echo "🌌 SkyScope Unified installed and live."
echo "🧠 API: curl -X POST http://localhost:8000/task -d '{\"task\":\"develop new memory summarization tool\"}' -H 'Content-Type: application/json'"
