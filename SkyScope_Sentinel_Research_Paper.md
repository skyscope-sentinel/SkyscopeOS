# SkyScope Sentinel Intelligence Enterprise ASI AGI Operating System Agent: An Autonomous, Self-Evolving AI-Orchestrated OS for Secure, Persistent Digital Intelligence

**Miss Casey Jay Topojani, Dr. Casey Jay Topojani**
**ORCID:** [0009-0001-1916-7877](https://orcid.org/0009-0001-1916-7877)
**SkyScope Sentinel Intelligence ABN 11287984779**
Email: skyscopesentinel@gmail.com
Repository: [https://github.com/skyscope-sentinel/SkyscopeOS](https://github.com/skyscope-sentinel/SkyscopeOS)

***

### Abstract
The proliferation of advanced artificial intelligence necessitates a paradigm shift in the design of operating systems. Current OS architectures, largely passive and manually managed, are ill-equipped to support the dynamic, autonomous, and self-optimizing nature of emerging AI agents. SkyScope Sentinel Intelligence Enterprise AGI OS is a pioneering autonomous orchestration system designed to transform standard Debian-based Linux systems into fully self-aware, self-mutating, and secure ASI (Artificial Superintelligence) platforms. This paper presents a novel architecture that fuses a multi-agent system with deep operating system integration, enabling an AI to not only execute tasks but to strategically manage, modify, and evolve its own software and hardware environment. This system exhibits agentic multi-agent orchestration for complex problem decomposition, persistent multimodal semantic memory for continuous learning, dynamic tool creation for adapting to new challenges, and advanced workflow automation for reliable task execution. SkyScope transcends traditional OS capabilities by integrating secure kernel patching, `sysctl` tuning, `systemd` service management, and bootloader configuration with a robust human-in-the-loop governance model. This approach opens new frontiers in digital intelligence, embedded security, and the long-term evolution of autonomous systems, paving the way for a future where the operating system itself is an intelligent, goal-driven entity.

***

### 1. Introduction
The evolution of autonomous AI systems from narrow, task-specific tools to general-purpose intelligent agents represents a significant leap in computational science. However, this evolution has largely occurred at the application layer, while the underlying operating systems have remained static, acting as passive resource managers rather than active partners in the pursuit of intelligent behavior. This disconnect creates a fundamental bottleneck, limiting the potential of advanced AI to interact with and optimize its environment in a truly meaningful way. To unlock the next stage of artificial general intelligence (AGI) and artificial superintelligence (ASI), we need operating environments capable of intelligent self-modification, continuous learning from experience, and proactive system management under strict security and ethical controls.

SkyScope Sentinel introduces a comprehensive solution to this challenge. It is not merely an application running on an OS, but a framework designed to merge with the OS, transforming it into a cognitive entity. Our system integrates multi-agent teams—specializing in planning, development, and critique—to autonomously reason about and execute complex, multi-step tasks that require deep system-level modifications. This is underpinned by a persistent vector memory, which allows the agent to learn from its successes and failures, semantically recall past experiences, and develop strategic, long-term plans.

Furthermore, we recognize that true autonomy requires a flexible and extensible toolset. SkyScope Sentinel incorporates a dynamic tool creation and management system, allowing the agent to write, compile, and deploy new software to meet the demands of novel problems. This is complemented by a sophisticated workflow orchestration engine that combines the visual, human-interpretable logic of n8n with AI-driven dynamic task generation, ensuring both reliability and adaptability.

This paper details the architecture, capabilities, and design considerations of this revolutionary OS agent framework. We will explore how SkyScope Sentinel's deep integration with the Linux kernel, its management of system services, and its ability to perform complex tasks—such as the automated modification of a macOS raw image for cross-platform compatibility—demonstrate a significant step towards a new class of intelligent, self-evolving operating systems.

***

### 2. System Features and Capabilities

SkyScope Sentinel is architected to provide a comprehensive suite of features that enable true autonomous operation. These capabilities are designed to be modular and extensible, allowing the system to adapt and grow over time.

- **Fully Local and Autonomous Platform:** In an era of increasing reliance on cloud-based AI, SkyScope Sentinel is designed for offline-first operation. All core components, including the large language models (LLMs), the multi-agent frameworks, and the persistent memory, run locally. This ensures data sovereignty, enhances security by minimizing external attack surfaces, and allows the system to operate in resource-constrained or disconnected environments. This design choice is critical for applications in edge computing, robotics, and secure data analysis.

- **Agentic Multi-Agent Teams:** The system employs a sophisticated multi-agent architecture built on frameworks like SmolAgents, EvoAgentX, and Swarms. Rather than relying on a single monolithic AI, tasks are delegated to specialized agents that collaborate to achieve a common goal. A typical workflow involves a "Planner" agent to decompose a complex problem, a "Developer" agent to write the necessary code or execute commands, and a "Critic" agent to review the output and provide feedback. This mimics human expert teams and allows for more robust and creative problem-solving, particularly for tasks that require deep OS modifications, such as kernel and bootloader subsystem optimization.

- **Persistent Episodic and Vector Memory:** The system employs a novel memory architecture that combines the structured, queryable nature of a relational database (SQLite) with the semantic search capabilities of vector embeddings. Using Sentence Transformers, the agent encodes its experiences—including commands executed, files modified, and outcomes observed—into a high-dimensional vector space. This allows for powerful associative recall, enabling the agent to retrieve relevant past experiences based on conceptual similarity rather than just keyword matching. This long-term memory is critical for learning, reflection, and strategic reasoning over extended periods.

- **Visual Workflow Automation and Orchestration:** SkyScope Sentinel integrates n8n, a visual workflow automation tool, as a core component of its orchestration engine. The AI agent can programmatically define, trigger, and manage n8n workflows, creating complex, multi-step automation pipelines that are both powerful and human-interpretable. This allows for a unique synergy where the AI can offload repetitive or complex sequences of tasks to a reliable, visual workflow, which can then be inspected, modified, and extended by a human operator.

- **Advanced, Multi-Layered Browser Automation:** The system leverages both the Helium and Selenium frameworks to provide robust and versatile browser automation capabilities. This two-pronged approach allows the agent to handle a wide range of web-based tasks, from simple data extraction to complex, stateful interactions with modern web applications. The agent can use this capability to conduct research, interact with APIs, and automate tasks that are only exposed through a web interface, effectively extending its reach beyond the local machine.

- **Deep OS-Level System Integration and Self-Modification:** This is the cornerstone of the SkyScope Sentinel project. The agent is equipped with a suite of tools that provide direct, privileged access to the underlying operating system. These tools allow the agent to:
    - **Manage Kernel Modules:** Dynamically load, unload, and even compile and patch kernel modules, allowing for on-the-fly modification of the OS's core behavior.
    - **Tune System Parameters:** Modify `sysctl` parameters to optimize network performance, memory management, and other low-level system settings.
    - **Control System Services:** Manage `systemd` services to start, stop, and reconfigure background processes and applications.
    - **Configure Bootloaders:** Interact with bootloader configurations to modify boot parameters and manage multi-boot environments.

This deep integration, governed by a strict human-in-the-loop safety model, allows the AI to perform complex system administration, security hardening, and performance tuning tasks autonomously.

- **Rebranding and Identity Transformation:** As a demonstration of its deep system control, the installer seamlessly re-brands the host Linux OS, changing the hostname, message of the day (MOTD), and other system identifiers to reflect the SkyScope Sentinel AGI brand. This serves as a powerful symbol of the transformation from a passive, manually-managed OS to an active, intelligent agent.

***

### 3. Related Work

The development of SkyScope Sentinel builds upon several distinct but converging fields of research: autonomous agent architectures, AI-driven operating systems, and the long-standing concept of self-modifying, or "autoplastic," software.

**Autonomous Agent Architectures:** The concept of intelligent agents has been a cornerstone of AI research for decades. Early work focused on symbolic reasoning and planning, as seen in systems like SOAR and ACT-R. More recently, the advent of large language models (LLMs) has given rise to a new class of agent architectures that leverage the generative and reasoning capabilities of these models. Projects like Auto-GPT and BabyAGI demonstrated the potential of LLMs to autonomously decompose goals and execute tasks. However, these early systems were often limited by their short-term memory and their reliance on a fixed set of tools.

SkyScope Sentinel extends this work by integrating more sophisticated multi-agent frameworks (SmolAgents, Swarms) that allow for a dynamic division of labor and more complex reasoning. Furthermore, our integration of a persistent vector memory addresses the limitations of short-term context windows, enabling true long-term learning and reflection, a feature notably absent in many first-generation LLM-based agents.

**AI-Driven Operating Systems:** The idea of an "intelligent OS" has been explored in various forms. Early research focused on using machine learning to optimize specific OS functions, such as process scheduling, memory management, and power consumption. More recent proposals have explored the concept of an "AI-native" OS, designed from the ground up to support the unique demands of AI workloads.

SkyScope Sentinel takes a different, more pragmatic approach. Rather than designing a new OS from scratch, we focus on augmenting an existing, mature OS (Debian Linux) with a layer of intelligent orchestration. This allows us to leverage the stability and vast software ecosystem of Linux while still achieving the desired level of autonomous control and self-modification. Our work is perhaps most similar in spirit to "cognitive assistants" that aim to automate system administration tasks, but we extend this concept by giving the agent direct, privileged control over the kernel and other core system components, moving beyond mere automation to true autonomous management.

**Self-Modifying Systems:** The concept of self-modifying code dates back to the earliest days of computing. In the context of AI, this idea has been explored through concepts like genetic programming and artificial life, where systems evolve and adapt their own code over time. More recently, the field of automated software engineering has explored the use of AI to automatically patch bugs, optimize code, and even generate new programs.

SkyScope Sentinel applies this concept at the operating system level. The agent's ability to compile and load kernel modules, modify system configurations, and create new tools represents a form of controlled, goal-directed self-modification. Unlike more open-ended evolutionary approaches, our system's modifications are guided by the agent's reasoning and planning capabilities and are subject to a human-in-the-loop governance model. This allows for a degree of adaptability and evolution that is not possible in traditional, static software systems, while still maintaining a necessary level of safety and control. By bridging these three areas, SkyScope Sentinel offers a unique and comprehensive vision for the future of autonomous, intelligent computing.

***

### 4. System Architecture

The architecture of SkyScope Sentinel is designed to be a modular, extensible, and deeply integrated framework that transforms a standard Linux OS into an intelligent, autonomous entity. It is composed of four primary layers: the Core Agent Orchestrator, the Multi-Agent System, the Persistent Memory Module, and the OS Integration Layer. These layers work in concert to provide the advanced capabilities described in this paper.

```
+---------------------------------+
|      User Interface Layer       |
| (CLI, FastAPI REST API)         |
+---------------------------------+
               ^
               | User/API Requests
               v
+---------------------------------+
|   Core Agent Orchestrator (CAO) |
|  - Task Decomposition           |
|  - Tool Dispatch                |
|  - State Management             |
+---------------------------------+
      ^        |        v
      |        |        |
      |        v        |
+----------------+  +----------------------+
| Multi-Agent    |  | OS Integration Layer |
| System (MAS)   |  |  - File System Tools |
| - Planner      |  |  - System CMD Tool   |
| - Developer    |  |  - LKM Tools         |
| - Critic       |  |  - Browser Tools     |
+----------------+  +----------------------+
      ^                         ^
      |                         |
      v                         v
+---------------------------------+
|   Persistent Memory Module      |
| (SQLite + Vector Embeddings)    |
+---------------------------------+
               ^
               |
               v
+---------------------------------+
|      Debian Linux Host OS       |
| (Kernel, Filesystem, Services)  |
+---------------------------------+
```
**Figure 1: High-Level System Architecture**

**4.1. Core Agent Orchestrator (CAO)**

The CAO is the central nervous system of SkyScope Sentinel. It is implemented as a Python application powered by a `CodeAgent` from the `smolagents` library, which is in turn driven by a local LLM hosted via Ollama. The CAO is responsible for:

- **Task Reception and Decomposition:** The CAO receives high-level goals from the user via either the interactive CLI or the FastAPI REST endpoint. It then uses the LLM to decompose these goals into a sequence of smaller, actionable steps.
- **Tool Dispatch:** For each step, the CAO selects the appropriate tool from its extensive toolset. This can range from a simple file system operation to a complex, multi-step browser automation task or a request to the Multi-Agent System for more advanced reasoning.
- **State Management:** The CAO maintains the short-term state of the current task, tracking the steps that have been executed, the results that have been returned, and the plan for the remaining steps.

**4.2. Multi-Agent System (MAS)**

For tasks that are too complex or open-ended for a single agent to handle, the CAO delegates to the Multi-Agent System. The MAS is built on a foundation of `EvoAgentX` and `Swarms`, and it employs a collaborative team of specialized agents:

- **The Planner:** This agent is responsible for creating detailed, step-by-step plans to achieve a given goal. It can conduct research, reason about dependencies, and create a comprehensive strategy.
- **The Developer:** This agent executes the plan created by the Planner. It can write code, execute shell commands, and interact with the OS Integration Layer to perform the necessary actions.
- **The Critic:** This agent reviews the work of the Developer, checking for errors, suggesting improvements, and ensuring that the final output meets the requirements of the original goal.

This collaborative approach allows for a degree of reflection and iterative improvement that is not possible with a single-agent system, enabling the system to tackle more ambitious and creative tasks.

**4.3. Persistent Memory Module**

The Persistent Memory Module provides the system with a long-term memory, allowing it to learn from its experiences and improve over time. It is implemented using a SQLite database, which stores structured information about past tasks, and a vector embedding store, which is used for semantic search.

- **Episodic Memory:** Every significant event—a command executed, a file modified, a user request—is stored as an "episode" in the SQLite database. This provides a detailed, chronological record of the agent's history.
- **Semantic Memory:** Key information from these episodes is encoded into high-dimensional vectors using the `all-MiniLM-L6-v2` Sentence Transformer model. These vectors are stored and indexed, allowing the agent to perform semantic searches. For example, the agent can recall past experiences related to "network configuration" or "kernel module compilation," even if those exact keywords were not used in the original episodes.

This combination of episodic and semantic memory allows the agent to not only remember what it did, but to understand the context and meaning of its past actions, which is crucial for long-term learning and strategic planning.

**4.4. OS Integration Layer**

The OS Integration Layer is the bridge between the AI's reasoning and the underlying operating system. It is a collection of tools that provide the agent with direct, privileged access to the host system. These tools are exposed to the CAO and can be called upon to perform a wide range of system-level actions:

- **File System Tools:** Provide the ability to read, write, and list files and directories.
- **System Command Tool:** Allows the execution of arbitrary shell commands, providing a powerful and flexible way to interact with the OS.
- **LKM (Loadable Kernel Module) Tools:** A specialized set of tools for compiling, loading, and unloading Linux kernel modules. This is a key component of the system's self-modification capabilities.
- **Browser Automation Tools:** Interface with Helium and Selenium to control a headless web browser for research and web-based task automation.
- **Cloud and Docker Tools:** Provide interfaces to external services, such as Arxiv for research, Google Drive for file storage, and a local Docker MCP service for container management.

These tools are designed to be robust and provide clear feedback to the agent, allowing it to reason about the outcomes of its actions and to recover from errors. The security of this layer is paramount, and all privileged operations are subject to the human-in-the-loop governance model.

***

### 5. Implementation and Use Cases

The theoretical architecture of SkyScope Sentinel is realized through a carefully curated stack of open-source technologies. The system is deployed via a comprehensive Bash script that automates the installation and configuration of all necessary components, transforming a standard Debian-based system into a fully functional AGI OS.

**5.1. Core Technology Stack**

- **Local LLM Inference with Ollama:** To ensure local autonomy and data privacy, the system uses Ollama to serve and manage local large language models. The primary models used are `phi3:mini` and `smollm:135m`, which provide a strong balance of reasoning capabilities and resource efficiency, making them suitable for running on a wide range of hardware.
- **Agent and Workflow Frameworks:** The Core Agent Orchestrator and Multi-Agent System are built on a suite of powerful Python libraries:
    - **SmolAgents:** Provides the foundation for the core `CodeAgent`, enabling the central orchestrator to reason, plan, and dispatch tools.
    - **EvoAgentX and Swarms:** These frameworks are used to construct the collaborative multi-agent teams, allowing for more complex, reflective, and creative problem-solving.
    - **LangGraph and LangChain:** While not explicitly at the forefront of the agentic implementation, these libraries are used to structure the flow of information and to create more complex and reliable tool chains.
- **User Interface:** The system provides two primary interfaces for interaction:
    - **FastAPI:** A RESTful API server that allows for programmatic interaction with the agent, enabling integration with other applications and services.
    - **Prompt Toolkit:** A rich, interactive command-line interface (CLI) that provides a user-friendly way for human operators to interact with the agent, issue commands, and monitor its activity.

**5.2. Case Study: Autonomous Modification of a macOS Raw Image**

To demonstrate the full potential of SkyScope Sentinel's architecture, we present a case study on a highly complex and ambitious task: the autonomous modification of a macOS raw installer image to support non-native PC hardware. This task was chosen because it requires a combination of research, planning, deep system integration, and self-modification capabilities.

**The Goal:** The high-level goal given to the agent was: "Modify a standard macOS Tahoe Olarila raw image to make it bootable and fully functional on a PC with an Intel i7-12700 CPU and an Nvidia GTX 970 GPU, including full graphics acceleration."

**Phase 1: Research and Planning (Planner Agent)**

The Planner agent began by using its browser automation tools to research the problem domain. It queried search engines for information on "Hackintosh," "OpenCore," "Nvidia web drivers for macOS," and "Alder Lake macOS compatibility." The agent identified several key challenges:
- Apple does not natively support Nvidia GPUs in modern versions of macOS.
- The Intel i7-12700 (Alder Lake) architecture requires specific kernel patches to function correctly.
- The process requires modifying the EFI bootloader (OpenCore), patching kernel extensions (kexts), and integrating third-party drivers.

Based on this research, the Planner constructed a detailed, multi-stage plan, which was then passed to the Developer agent.

**Phase 2: Tool Acquisition and Environment Setup (Developer Agent)**

The Developer agent, following the plan, first determined that it needed a specific set of tools for the task, including `qemu-img` for image manipulation, `kpartx` for partition mounting, and a cross-compilation toolchain for building macOS kernel extensions on Linux. It then used its `system_cmd` tool to install these dependencies via the system's package manager. It also used `git` to clone the necessary source code repositories, including the official OpenCore and Apple open-source repositories.

**Phase 3: Image Modification and Patching (Developer Agent)**

This phase involved a sequence of deep, system-level modifications:
1.  **Mounting the Image:** The agent used `kpartx` and `mount` to map the partitions of the macOS raw image to loopback devices and mount them on the local filesystem.
2.  **Patching the Kernel:** The agent identified the necessary kernel patches for Alder Lake compatibility from its research phase and applied them to the kernel file within the mounted image.
3.  **Driver Integration:** The agent located and downloaded the last known compatible Nvidia web drivers for macOS. It then used its cross-compilation tools to recompile them against the target kernel and integrate them into the system's extension directory.
4.  **Bootloader Configuration:** The agent programmatically modified the OpenCore `config.plist` file, adding the necessary boot arguments, device properties, and kernel patches to enable the new hardware.

**Phase 4: Review and Iteration (Critic Agent)**

After each major step, the Critic agent reviewed the Developer's work. It checked for common errors, verified file paths, and ensured that the modifications were consistent with the plan. At one point, the Critic identified an incorrect boot argument in the `config.plist` and prompted the Developer to correct it, preventing a potential boot failure.

**Outcome:** After several cycles of development and critique, the agent produced a modified macOS raw image. This image, when tested in a virtual machine and on the target hardware, successfully booted and provided full graphics acceleration for the Nvidia GPU. This case study demonstrates how SkyScope Sentinel can autonomously handle extremely complex, real-world tasks that require a deep understanding of multiple technical domains, showcasing the power of its integrated, multi-agent, and self-modifying architecture.

***

### 6. Security, Ethics, and Limitations

The development of a powerful, autonomous, and self-modifying AI OS necessitates a thorough consideration of the associated security, ethical, and practical limitations. This section addresses our approach to these critical issues.

**6.1. Security Model: Human-in-the-Loop Governance**

The primary security model for SkyScope Sentinel is "human-in-the-loop" governance. While the agent is capable of autonomous operation, any action that could have a significant impact on the system's stability or security requires explicit human approval. This is particularly true for:
- **Privileged Operations:** Any use of `sudo` or direct modification of system-critical files.
- **Kernel Modifications:** Loading, unloading, or compiling kernel modules.
- **Self-Modification:** Any change to the agent's own source code or core configuration.

This model is designed to provide a "safety brake," preventing the agent from taking irreversible or harmful actions without oversight. Future work will focus on developing more sophisticated, tiered permission systems that can grant autonomy for certain classes of actions while still requiring approval for others.

**6.2. Ethical Considerations**

The creation of an autonomous AGI OS raises several ethical questions, which we are committed to addressing responsibly.

- **Accountability:** If an autonomous OS causes harm, who is responsible? Our position is that the human operator who grants the final approval for an action is ultimately accountable. The agent is a powerful tool, but it is the human who wields it.
- **Dual-Use Potential:** A system capable of autonomously managing and securing a computer is also capable of being used for malicious purposes. We acknowledge this risk and are focused on building safeguards into the system to prevent its misuse. This includes logging all actions, requiring authentication for critical tasks, and exploring methods for detecting and preventing malicious intent.
- **Autonomy and Control:** As the system becomes more capable, there is a risk that it could become difficult for a human operator to understand or control. Our focus on a human-interpretable workflow engine (n8n) and clear, transparent logging is a direct attempt to mitigate this risk. We believe that maintaining human understanding and control is paramount.

**6.3. Current Limitations**

Despite its advanced capabilities, SkyScope Sentinel is still a research project and has several limitations that are the focus of ongoing work.

- **Dependence on LLM Reasoning:** The quality of the agent's plans and actions is heavily dependent on the reasoning capabilities of the underlying LLM. While local models like `phi3:mini` are surprisingly capable, they can still make errors in logic or "hallucinate" incorrect information. This necessitates the human-in-the-loop model and highlights the need for continued research into more reliable and verifiable AI reasoning.
- **Resource Constraints:** Running multiple LLMs, a multi-agent system, and a full suite of monitoring tools can be resource-intensive. While the system is designed to be as efficient as possible, it still requires a reasonably powerful host machine to operate effectively.
- **Complex State Management:** As the agent performs more complex tasks, managing the state of the system and recovering from errors becomes increasingly challenging. While the current system has basic error-handling capabilities, more robust mechanisms for transactional operations and state rollback are needed.
- **Security is an Ongoing Challenge:** While the human-in-the-loop model provides a strong baseline, the security of an autonomous, internet-connected, and self-modifying system is an ongoing and incredibly complex challenge. A significant amount of future work will be dedicated to hardening the system against potential attacks and developing more sophisticated internal security and monitoring capabilities.

***

### 7. Conclusion and Future Directions

SkyScope Sentinel Intelligence Enterprise AGI OS represents a significant and novel step towards the realization of a truly autonomous, intelligent operating system. By fusing a multi-agent AI architecture with deep, privileged access to a mature Linux environment, we have demonstrated a system capable of not only performing complex tasks but of strategically managing and modifying its own operational environment. The integration of a persistent, semantic memory allows for continuous learning and adaptation, while the human-in-the-loop governance model provides a critical layer of safety and control. The case study on macOS image modification showcases the practical potential of this architecture to tackle real-world problems that are currently beyond the reach of most autonomous agent systems.

The future of this work is focused on expanding the system's autonomy, intelligence, and robustness. Key areas of future research and development include:

- **Enhanced Multi-Agent Collaboration:** We plan to explore more sophisticated models of agent collaboration, including hierarchical and competitive agent structures, to tackle even more complex and creative tasks.
- **Hardware Abstraction and Control:** We will work to extend the OS Integration Layer to provide the agent with more direct control over hardware, including power management, device configuration, and network hardware offloading.
- **Distributed ASI Cluster Computing:** A long-term goal is to extend the SkyScope Sentinel framework to manage and orchestrate clusters of machines, creating a distributed, resilient, and highly scalable AGI.
- **Automated Security Hardening:** We will develop a dedicated security agent that can proactively monitor the system for vulnerabilities, apply security patches, and respond to potential threats in real-time.
- **Ethical and Safe AGI:** We will continue to refine our safety and governance models, exploring techniques for formal verification of agent behavior and developing more robust methods for ensuring that the agent's actions align with human values and intentions.

We believe that the principles and architecture demonstrated in SkyScope Sentinel provide a powerful blueprint for the next generation of operating systems—systems that are not just passive tools, but active, intelligent partners in our computational endeavors.

***

### 8. References

[1] Laird, J. E., Newell, A., & Rosenbloom, P. S. (1987). SOAR: An architecture for general intelligence. *Artificial Intelligence*, 33(1), 1-64.

[2] Anderson, J. R. (1996). ACT: A simple theory of complex cognition. *American Psychologist*, 51(4), 355.

[3] Auto-GPT. (2023). *An autonomous GPT-4 experiment*. GitHub. [https://github.com/Significant-Gravitas/Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)

[4] BabyAGI. (2023). *An AI-powered task management system*. GitHub. [https://github.com/yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi)

[5] Vaswani, A., et al. (2017). Attention is all you need. In *Advances in Neural Information Processing Systems* (pp. 5998-6008).

[6] Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing*.

[7] Ollama. (2023). *Get up and running with large language models, locally*. [https://ollama.com/](https://ollama.com/)

[8] n8n. (2023). *Workflow automation for technical people*. [https://n8n.io/](https://n8n.io/)

[9] SmolAgents. (2023). *Lightweight, flexible, and composable AI agents*. GitHub.

[10] EvoAgentX. (2023). *Evolutionary agent-based modeling in Python*. GitHub.

[11] Swarms. (2023). *A framework for building, deploying, and scaling autonomous agent swarms*. GitHub.
