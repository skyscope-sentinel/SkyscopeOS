# SkyscopeOS Sentinel AGI: Architectural Deep Dive

This document details the definitive, enterprise-grade architecture of the SkyscopeOS Sentinel AGI.

## 1. The Orchestrator (Core)

The `orchestrator.py` module is a FastAPI application acting as the heart of the AGI.

-   **ASDISE Prompt (Autonomous System Deep Integration & Self-Evolution):** The most complex, self-optimizing system prompt defining the agent's existence and rules.
-   **Tool Registration:** All tools are instantiated once at startup and made available via a unified ToolDispatcher structure.
-   **Resource Management Thread:** A dedicated background thread uses `psutil` to continuously monitor and report the agent's consumption against its allocated 8GB RAM and 600GB storage. If limits are approached, the thread initiates memory compression or data offloading.

## 2. Learning and Memory

The memory system is layered for different data types.

-   **`memory/memory.py`:** Utilizes SQLite for structured logs and Vector Embeddings for semantic search.
-   **Private Compressed Knowledge Stack:** Large-scale research data from the Chromium Tool is compressed using `zlib` before storage, maximizing use of the 600GB allocation while maintaining fast indexed retrieval.
-   **Reflection Daemon:** Processes episodic logs into new knowledge and policy adjustments, enhancing the ASDISE Prompt.

## 3. Autonomous Tool Provisioning

The `tooling/tool_provisioner.py` is the engine of self-evolution.

-   **Requirement Analysis:** The agent's LLM core requests a tool for a complex task (e.g., "Need tool for image segmentation").
-   **Discovery:** The Provisioner searches GitHub for relevant repositories.
-   **MCP Creation (External):** If a suitable project is found, `GitPython` clones the repo into the `tool_sandbox`, and a Docker MCP template is generated and built using the `docker-py` SDK.
-   **Wrapper Generation (Internal):** The Provisioner then uses the LLM to write a wrapper Python function to communicate with the new Docker MCP service.
-   **Validation & Registration:** The wrapper is submitted to the `IntegrityCritic` for security review. If safe, it is registered via `exec()` into the Orchestrator's active tool list.

## 4. Governance and Security

Security is non-negotiable.

-   **Integrity Critic (`governance/integrity_critic.py`):** Mandatory `ast` module static analysis on any generated code before it can be executed or written to a core file.
-   **Rollback Manager (`governance/rollback_manager.py`):** Uses `shutil` to create transactional snapshots of all core system files and configuration directories before any high-risk operations (e.g., LKM modification or self-patching).

## 5. Ultimate CLI (`cli/cli.py`)

The CLI is a dedicated `prompt-toolkit` client, providing a responsive and visually stunning interface.

-   **Real-time Metrics:** Pulls live data from the Orchestrator's `/metrics` endpoint.
-   **Animated Visualization:** Uses `alive-progress` compatible rendering techniques for animated status bars (CPU, RAM, NET I/O).
-   **Flowing Code Display:** A dedicated section where the agent's internal thought process is displayed as a matrix-style "code stream" to show its active decision-making.
