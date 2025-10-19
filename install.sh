#!/bin/bash
#
# SkyscopeOS Sentinel AGI - Definitive, Robust Installation Script (install.sh)
#
# This script performs a robust, end-to-end installation of the SkyscopeOS
# system, with comprehensive logging and verification.

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration ---
REPO_URL="http://localhost:8888"
INSTALL_ROOT_DIR="${HOME}/.skyscopeos"
LOG_DIR="${INSTALL_ROOT_DIR}/logs"
LOG_FILE="${LOG_DIR}/install.log"
VENV_PATH="${INSTALL_ROOT_DIR}/venv"
BIN_PATH="/usr/local/bin/skyscope"

# --- Helper Functions ---
setup_logging() {
    mkdir -p "$LOG_DIR"
    touch "$LOG_FILE"
    exec &> >(tee -a "$LOG_FILE")
    echo "======================================================="
    echo "  SKYSCOPEOS SENTINEL AGI - ULTIMATE INSTALLER START"
    echo "  Timestamp: $(date)"
    echo "======================================================="
    echo "Full installation log is being saved to: $LOG_FILE"
}

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
        log_error "$1 is not installed. Please install $1 and try again."
    fi
}

# --- Core Installation Functions ---

install_system_deps() {
    log_step "Checking essential system dependencies (git, docker, python3, pip)..."
    check_dependency "git"
    check_dependency "docker"

    if ! command -v python3 &> /dev/null; then log_error "Python 3 is not installed or not in PATH."; fi
    if ! python3 -m ensurepip &> /dev/null; then log_error "Python 'pip' is not available. Please install python3-pip."; fi

    log_step "Updating system and installing base packages..."
    sudo apt-get update -y
    sudo apt-get install -y nodejs npm
    log_success "System dependencies and base packages are in place."
}

copy_local_project() {
    log_step "Copying local SkyscopeOS project to installation directory..."

    if [ -d "$INSTALL_ROOT_DIR" ]; then
        log_step "Existing installation found. Removing old installation..."
        rm -rf "$INSTALL_ROOT_DIR"
    fi

    log_step "Copying new project files..."
    cp -r skyscope_os "$INSTALL_ROOT_DIR" || log_error "Failed to copy local project files."

    mkdir -p "${INSTALL_ROOT_DIR}/tool_sandbox"
    log_success "Project files copied successfully."
}

install_python_env() {
    log_step "Creating Python Virtual Environment and installing dependencies..."
    python3 -m venv "$VENV_PATH"
    source "${VENV_PATH}/bin/activate"
    pip install --upgrade pip

    # Read dependencies from the requirements file in the copied project
    REQUIREMENTS_PATH="${INSTALL_ROOT_DIR}/requirements.txt"
    if [ -f "$REQUIREMENTS_PATH" ]; then
        pip install -r "$REQUIREMENTS_PATH"
    else
        log_error "requirements.txt not found at $REQUIREMENTS_PATH."
    fi

    log_step "Installing Playwright Chromium browser binaries..."
    python3 -m playwright install chromium
    deactivate
    log_success "Python environment and dependencies installed."
}

install_third_party_services() {
    log_step "Installing n8n for local visual workflow orchestration..."
    npm install -g n8n pm2
    pm2 start "n8n" --name skyscope-n8n --update-env || pm2 restart skyscope-n8n
    pm2 save

    log_step "Installing Ollama for local LLM inference..."
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull smollm:135m
    ollama pull phi3:mini
    log_success "Third-party services (n8n, Ollama) installed."
}

create_cli_wrapper() {
    log_step "Creating global 'skyscope' CLI shortcut..."

    CLI_WRAPPER_CONTENT=$(cat << EOF
#!/bin/bash
export SKYSCOPE_ROOT="$INSTALL_ROOT_DIR"
source "$VENV_PATH/bin/activate"
exec python3 "$INSTALL_ROOT_DIR/skyscope_os/cli/cli.py" "\$@"
EOF
)

    WRAPPER_PATH="${INSTALL_ROOT_DIR}/skyscope_cli_wrapper.sh"
    echo "$CLI_WRAPPER_CONTENT" > "$WRAPPER_PATH"
    chmod +x "$WRAPPER_PATH"

    if [ -L "$BIN_PATH" ]; then sudo rm "$BIN_PATH"; fi
    if [ -f "$BIN_PATH" ]; then log_error "A file already exists at $BIN_PATH. Please remove it manually."; fi

    if ! sudo ln -s "$WRAPPER_PATH" "$BIN_PATH"; then
         log_error "Failed to create global link for skyscope command."
    fi

    # --- Shell Profile Update ---
    SHELL_CONFIG=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    fi

    if [ -n "$SHELL_CONFIG" ] && ! grep -q 'export PATH="$HOME/bin:$PATH"' "$SHELL_CONFIG"; then
        echo "Adding ~/bin to your PATH in $SHELL_CONFIG."
        echo '' >> "$SHELL_CONFIG"
        echo '# Added by SkyscopeOS Installer' >> "$SHELL_CONFIG"
        echo 'export PATH="$HOME/bin:$PATH"' >> "$SHELL_CONFIG"
    fi
    log_success "Global 'skyscope' command is now available."
}

verify_installation() {
    log_step "Verifying installation..."
    source "${VENV_PATH}/bin/activate"

    if ! command -v ollama &> /dev/null; then log_error "Ollama command not found after installation."; fi
    if ! [ -x "$HOME/bin/skyscope" ] && ! [ -x "/usr/local/bin/skyscope" ]; then log_error "Skyscope command not found or not executable."; fi

    log_success "Core components verified."
}


# --- Main Execution ---
main() {
    setup_logging
    install_system_deps
    copy_local_project
    install_python_env
    install_third_party_services
    create_cli_wrapper
    verify_installation

    echo -e "\n\033[32m"
    echo "======================================================="
    echo "  INSTALLATION COMPLETE! SkyscopeOS is ready."
    echo "======================================================="
    echo -e "\033[0m"
    echo "Please run the following command to update your current shell session:"
    echo -e "  \033[33msource ~/.bashrc\033[0m (or ~/.zshrc if you use Zsh)"
    echo
    echo "Then, you can launch the CLI by simply typing:"
    echo -e "  \033[33mskyscope\033[0m"
    echo
    echo "The orchestrator service will be started automatically in the background."
    echo "Logs are available at: $LOG_FILE"
}

main
