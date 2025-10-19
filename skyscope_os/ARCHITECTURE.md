# SkyscopeOS Sentinel AGI: Architectural Deep Dive

This document details the definitive, enterprise-grade architecture of the SkyscopeOS Sentinel AGI.

## 1. The Orchestrator (`core/orchestrator.py`)

The orchestrator is a FastAPI application that serves as the central nervous system of the AGI.

-   **ASDISE Prompt:** The agent is initialized with an "Autonomous System Deep Integration & Self-Evolution" prompt that defines its core identity and directives.
-   **Tool Registration:** All tools from the various `tooling/` modules are imported and registered with the `CodeAgent` at startup.
-   **Lifecycle Management:** The orchestrator manages the lifecycle of background processes, such as the `SelfReflectionDaemon` and the `ChromiumBrowser` instance.

## 2. Learning and Memory (`memory/` & `learning/`)

The memory system is layered for different types of data and learning.

-   **`memory/memory.py`:**
    -   `SkyMemory`: Manages short-term, episodic memory using a SQLite database and vector embeddings for semantic search of past actions.
    -   `KnowledgeStack`: Manages a long-term, compressed (`zlib`) knowledge base for storing large documents and research findings.
-   **`learning/self_reflection_daemon.py`:** A background thread that periodically analyzes the episodic memory, uses an LLM to generate "lessons learned," and stores these insights back into the memory, enabling continuous self-improvement.

## 3. Autonomous Tool Provisioning (`tooling/tool_provisioner.py`)

This module is the engine of the agent's self-evolution.

-   **Requirement Analysis:** The agent can reason that it needs a new tool for a given task.
-   **Discovery:** The `ProvisionExternalMCP` tool can search GitHub for relevant repositories.
-   **MCP Creation:** It uses `GitPython` to clone the repo and the `DockerTools` module to build and run the project as a containerized Managed Compute Processor (MCP).
-   **Wrapper Generation:** The agent can then generate a new Python tool function to interact with the newly created MCP.

## 4. Governance and Security (`governance/`)

-   **`integrity_critic.py`:** Provides an `IntegrityCritic` class that uses Python's `ast` module to perform static analysis on any LLM-generated code, preventing the execution of syntactically invalid or potentially unsafe code.
-   **`rollback_manager.py`:** Provides a `RollbackManager` class that can create snapshots of critical files before high-risk operations and roll them back in case of failure.

## 5. The Ultimate CLI (`cli/cli.py`)

The CLI is a dedicated `prompt-toolkit` and `alive-progress` application that provides a rich, interactive user experience.

-   **Real-time Metrics:** It fetches live system data from the orchestrator's `/metrics` endpoint.
-   **Animated Visualization:** It uses animated bars and spinners to display CPU, memory, and disk usage.
-   **Agent Insight:** It includes a "flowing code" display to visualize the agent's internal thought process.

## 6. The Installer (`install.sh`)

The installer is a robust Bash script responsible for setting up the entire SkyscopeOS environment.

-   **Dependency Management:** It installs all necessary system packages, Python libraries from `requirements.txt`, and Node.js packages.
-   **Environment Setup:** It clones the git repository, creates a Python virtual environment, and pre-downloads the necessary AI models.
-   **System Integration:** It creates a `skyscope` command for easy CLI access and sets up a `systemd` service for the orchestrator to ensure it runs persistently in the background.
