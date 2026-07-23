# Use the official Python latest image
FROM python:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    nano \
    sudo \
    lsof \
    psmisc \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install gh -y

# Install Node.js for Claude Code CLI
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y nodejs

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set the working directory
WORKDIR /workspace

# Install Claude Code CLI as root before switching to vscode user
RUN npm install -g @anthropic-ai/claude-code

# Set the default user
USER $USERNAME

# Install uv (fast Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Rust toolchain (for PyO3 examples)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/home/vscode/.local/bin:/home/vscode/.cargo/bin:${PATH}"

# rustup's default profile ships a `rust-analyzer` proxy shim in ~/.cargo/bin
# WITHOUT the component behind it. Editors find that shim on PATH, prefer it
# over their own bundled copy, and it dies with "Unknown binary
# 'rust-analyzer'" — surfacing as "proc-macro-srv is not running", which breaks
# expansion of PyO3's #[pymodule]/#[pyclass] macros. Installing the component
# makes the shim real and version-matched to the toolchain (ABI-compatible with
# the compiler that builds the proc macros). rust-src backs go-to-definition
# into std.
RUN rustup component add rust-analyzer rust-src

# Install standalone CLI tools via uv tool (not project dependencies)
RUN uv tool install ruff && \
    uv tool install maturin

# Expose common ports
EXPOSE 5000 8000 8080
