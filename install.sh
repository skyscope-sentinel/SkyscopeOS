#!/bin/bash
#
# SkyscopeOS Sentinel AGI - Definitive Installation Script (install.sh)
#
# This script performs a robust, end-to-end installation of the SkyscopeOS
# system, ensuring all system dependencies, Python packages, browser binaries,
# and core AI models are fully installed and integrated.

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration ---
REPO_URL="https://github.com/skyscope-sentinel/SkyscopeOS.git"
INSTALL_ROOT_DIR="${HOME}/.skyscopeos"
VENV_PATH="${INSTALL_ROOT_DIR}/venv"
BIN_PATH="/usr/local/bin/skyscope"
PYTHON_DEPS=(
    "fastapi" "uvicorn" "prompt-toolkit" "alive-progress" "requests" "psutil"
    "pydantic" "sqlite-utils" "sentence-transformers" "playwright" "docker"
    "gitpython" "numpy" "smolagents" "evoagentx" "swarms" "langchain"
    "langgraph" "lief" "capstone" "uncompyle6" "pyelftools" "radare2-py" "triton"
    "jinja2" "beautifulsoup4" "moviepy" "gtts" "pyttsx3" "whisper" "ffmpeg-python"
    "transformers" "tqdm" "torch" "torchvision" "torchio" "faiss-cpu"
    "google-auth" "google-auth-oauthlib" "google-api-python-client" "pyyaml" "arxiv"
)

# --- Helper Functions ---

log_success() {
    echo -e "\n\033[32m[SUCCESS]\033[0m $1"
}

log_step() {
    echo -e "\n\033[36m[STEP]\033[0m $1"
}

log_error() {
    echo -e "\n\033[31m[ERROR]\033[0m $1" >&2
    exit 1
}

check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        log_error "$1 is not installed. Please install $1 (git, docker) and try again."
    fi
}

# --- Core Installation Functions ---

install_system_deps() {
    log_step "Checking essential system dependencies (git, docker, python3, pip)..."
    check_dependency "git"
    check_dependency "docker"

    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed or not in PATH."
    fi

    if ! python3 -m ensurepip &> /dev/null; then
        log_error "Python 'pip' is not available. Please install python3-pip."
    fi

    log_step "Updating system and installing base packages..."
    sudo apt-get update -y
    sudo apt-get install -y nodejs npm
    log_success "All system dependencies found and base packages installed."
}

clone_and_setup_dir() {
    log_step "Cloning SkyscopeOS repository and setting up directory structure..."

    if [ -d "$INSTALL_ROOT_DIR" ]; then
        echo "Existing installation found. Backing up and cleaning up dynamic files..."
        TEMP_BACKUP_DIR=$(mktemp -d)

        [ -d "${INSTALL_ROOT_DIR}/memory" ] && mv "${INSTALL_ROOT_DIR}/memory" "$TEMP_BACKUP_DIR"
        [ -d "${INSTALL_ROOT_DIR}/governance/snapshots" ] && mv "${INSTALL_ROOT_DIR}/governance/snapshots" "$TEMP_BACKUP_DIR/snapshots"

        rm -rf "$INSTALL_ROOT_DIR"
    fi

    git clone "$REPO_URL" "$INSTALL_ROOT_DIR" || log_error "Failed to clone repository from $REPO_URL"

    [ -d "$TEMP_BACKUP_DIR/memory" ] && mv "$TEMP_BACKUP_DIR/memory" "${INSTALL_ROOT_DIR}/"
    [ -d "$TEMP_BACKUP_DIR/snapshots" ] && mkdir -p "${INSTALL_ROOT_DIR}/governance" && mv "$TEMP_BACKUP_DIR/snapshots" "${INSTALL_ROOT_DIR}/governance/"
    rm -rf "$TEMP_BACKUP_DIR"

    mkdir -p "${INSTALL_ROOT_DIR}/tool_sandbox"
    log_success "Repository cloned and directory structure prepared."
}

install_python_env() {
    log_step "Creating Python Virtual Environment and installing core dependencies..."

    python3 -m venv "$VENV_PATH"
    source "${VENV_PATH}/bin/activate"

    pip install --upgrade pip
    pip install "${PYTHON_DEPS[@]}"

    log_step "Installing Playwright Chromium browser binaries..."
    python3 -m playwright install chromium

    deactivate
    log_success "Python environment and dependencies installed successfully."
}

initialize_ai_models() {
    log_step "Initializing AI Models (Sentence-Transformer for Vector Store)..."

    source "${VENV_PATH}/bin/activate"
    python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
    deactivate
    log_success "Core AI model ('all-MiniLM-L6-v2') cached for immediate use."
}

create_cli_wrapper() {
    log_step "Creating global 'skyscope' CLI shortcut at $BIN_PATH..."

    CLI_WRAPPER_CONTENT=$(cat << EOF
#!/bin/bash
export SKYSCOPE_ROOT="$INSTALL_ROOT_DIR"
source "$VENV_PATH/bin/activate"
exec python3 "$INSTALL_ROOT_DIR/cli/cli.py" "\$@"
EOF
)

    WRAPPER_PATH="${INSTALL_ROOT_DIR}/skyscope_cli_wrapper.sh"
    echo "$CLI_WRAPPER_CONTENT" > "$WRAPPER_PATH"
    chmod +x "$WRAPPER_PATH"

    if [ -f "$BIN_PATH" ] && [ ! -L "$BIN_PATH" ]; then
        log_error "A file already exists at $BIN_PATH and it's not a symlink. Please remove it manually."
    elif [ -L "$BIN_PATH" ]; then
        rm "$BIN_PATH"
    fi

    if ! ln -s "$WRAPPER_PATH" "$BIN_PATH" 2>/dev/null; then
        echo -e "\033[33m[WARNING]\033[0m Permission denied for /usr/local/bin. Trying with sudo..."
        if ! sudo ln -s "$WRAPPER_PATH" "$BIN_PATH"; then
             log_error "Failed to create global link even with sudo. Please set PATH or link manually."
        fi
    fi

    log_success "Global 'skyscope' command is now available."
}

# --- Main Execution ---

main() {
    echo -e "\033[35m"
    echo "======================================================="
    echo "  SKYSCOPEOS SENTINEL AGI - ULTIMATE INSTALLER START"
    echo "======================================================="
    echo -e "\033[0m"

    install_system_deps
    clone_and_setup_dir
    install_python_env
    initialize_ai_models
    create_cli_wrapper

    log_step "Finalizing Installation."

    START_COMMAND="export SKYSCOPE_ROOT=\"$INSTALL_ROOT_DIR\" && source \"$VENV_PATH/bin/activate\" && nohup uvicorn core.orchestrator:app --host 127.0.0.1 --port 8000 --app-dir $INSTALL_ROOT_DIR > $INSTALL_ROOT_DIR/skyscope.log 2>&1 &"

    echo -e "\n\033[32m"
    echo "======================================================="
    echo "  INSTALLATION COMPLETE! SkyscopeOS is ready."
    echo "======================================================="
    echo -e "\033[0m"
    echo -e "To **START THE ORCHESTRATOR SERVICE** (The AGI Brain):"
    echo -e "  \033[33m\$ $START_COMMAND\033[0m"
    echo
    echo -e "To **LAUNCH THE CLI** and begin interacting:"
    echo -e "  \033[33m\$ skyscope\033[0m"
    echo
    echo "Logs are written to: $INSTALL_ROOT_DIR/skyscope.log"
}

main
