#!/usr/bin/env python3
import asyncio
from alive_progress import alive_bar, Spinner
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.application import create_app_session
import time
import random
import threading
import requests

# Simulated system metrics updater
class SystemMetrics:
    def __init__(self):
        self.cpu = 0
        self.memory = 0
        self.agent_tasks = 0
        self.workflow_progress = 0
        self.chat_history = []

    def update_metrics(self):
        self.cpu = random.randint(1, 100)
        self.memory = random.randint(100, 8000)
        self.agent_tasks = random.randint(0, 10)
        self.workflow_progress = (self.workflow_progress + random.randint(1, 5)) % 100

    def add_chat(self, msg, user=True):
        prefix = "You: " if user else "SkyScope: "
        self.chat_history.append(prefix + msg)
        if len(self.chat_history) > 10:
            self.chat_history.pop(0)

metrics = SystemMetrics()

def metrics_updater():
    while True:
        metrics.update_metrics()
        time.sleep(1)

def render_metrics():
    print_formatted_text(HTML(f"<ansiblue>CPU Usage:</ansiblue> {metrics.cpu}%"))
    print_formatted_text(HTML(f"<ansiblue>Memory Usage:</ansiblue> {metrics.memory} MB"))
    print_formatted_text(HTML(f"<ansiblue>Active Agent Tasks:</ansiblue> {metrics.agent_tasks}"))
    print_formatted_text(HTML(f"<ansiblue>Workflow Progress:</ansiblue> {metrics.workflow_progress}%"))
    print_formatted_text(HTML("\n<ansigreen>Chat history:</ansigreen>"))
    for line in metrics.chat_history:
        print(line)
    print("\n" + "="*60 + "\n")

async def main_cli():
    session = PromptSession()
    threading.Thread(target=metrics_updater, daemon=True).start()

    with patch_stdout():
        while True:
            render_metrics()
            user_input = await session.prompt_async(HTML('<ansiyellow>SkyScope> </ansiyellow>'))
            if user_input.lower() in ("exit", "quit"):
                print("Exiting SkyScope CLI...")
                break
            metrics.add_chat(user_input, True)
            try:
                response = requests.post("http://localhost:8000/task", json={"task": user_input})
                response.raise_for_status()
                result = response.json().get("result", "No result found.")
                metrics.add_chat(result, False)
            except requests.exceptions.RequestException as e:
                metrics.add_chat(f"Error: {e}", False)
            render_metrics()

if __name__=="__main__":
    asyncio.run(main_cli())
