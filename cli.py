#!/usr/bin/env python3
import asyncio
import psutil
import threading
import time
import requests
import os
from alive_progress import alive_bar
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML

class SystemMetrics:
    def __init__(self):
        self.cpu_percent = 0
        self.mem_percent = 0
        self.chat_history = []

    def update_metrics(self):
        self.cpu_percent = psutil.cpu_percent(interval=1)
        self.mem_percent = psutil.virtual_memory().percent

    def add_chat(self, msg, user=True):
        prefix = "You: " if user else "SkyScope: "
        self.chat_history.append(prefix + msg)
        if len(self.chat_history) > 15:
            self.chat_history.pop(0)

metrics = SystemMetrics()

def metrics_updater():
    while True:
        metrics.update_metrics()
        time.sleep(1)

def render_ui():
    os.system('clear')
    print("====================== SkyScope Sentinel AGI OS ======================")
    with alive_bar(100, title=f"CPU Usage: {metrics.cpu_percent}%", bar="smooth", spinner="waves", length=40) as bar:
        bar(metrics.cpu_percent)
    with alive_bar(100, title=f"Memory Usage: {metrics.mem_percent}%", bar="smooth", spinner="waves", length=40) as bar:
        bar(metrics.mem_percent)
    print("\n============================ Chat History ============================")
    for line in metrics.chat_history:
        print(line)
    print("======================================================================")

async def main_cli():
    session = PromptSession()
    metrics_thread = threading.Thread(target=metrics_updater, daemon=True)
    metrics_thread.start()
    # Give a moment for the first metrics to be collected
    await asyncio.sleep(1.1)

    with patch_stdout():
        while True:
            render_ui()
            try:
                user_input = await session.prompt_async(HTML('<ansiyellow>You> ></ansiyellow> '))
                if user_input.lower() in ("exit", "quit"):
                    print("Exiting SkyScope CLI...")
                    break

                metrics.add_chat(user_input, True)

                # Send task to orchestrator
                response = requests.post("http://localhost:8000/task", json={"task": user_input})
                response.raise_for_status()
                result = response.json().get("result", "No result found.")

                metrics.add_chat(result, False)

            except requests.exceptions.RequestException as e:
                metrics.add_chat(f"Error communicating with orchestrator: {e}", False)
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    try:
        asyncio.run(main_cli())
    except Exception as e:
        print(f"An error occurred: {e}")
