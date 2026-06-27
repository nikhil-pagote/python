# UV Cheatsheet - Python Project Management

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Project Creation & Management](#project-creation--management)
3. [Dependency Management](#dependency-management)
4. [Virtual Environments](#virtual-environments)
5. [Code Quality Tools](#code-quality-tools)
6. [Running & Building](#running--building)
7. [Advanced Usage](#advanced-usage)

## Installation & Setup

### Install uv
```bash
# Install uv using pip
pip install uv

# Install using homebrew (macOS/Linux)
brew install uv

# Install using curl (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Update uv
```bash
uv self update
```

### Check version
```bash
uv --version
```

## Project Creation & Management

### Create a new project
```bash
# Create a new Python project
uv init my-project
cd my-project

# Create project with specific Python version
uv init my-project --python 3.11

# Create application project (with src layout)
uv init my-app --app

# Create library project
uv init my-lib --lib
```

### Initialize existing directory
```bash
# Initialize current directory as uv project
uv init

# Initialize with specific Python version
uv init --python 3.10
```

### Project structure
```
my-project/
├── pyproject.toml
├── README.md
├── src/
│   └── my_project/
│       └── __init__.py
└── tests/
    └── __init__.py
```

## Dependency Management

### Add dependencies
```bash
# Add runtime dependency
uv add requests

# Add development dependency
uv add pytest --dev

# Add optional dependency group
uv add sphinx --group docs

# Add dependency with version constraint
uv add "django>=4.0,<5.0"

# Add from git repository
uv add git+https://github.com/user/repo.git

# Add editable local package
uv add -e ./local-package
```

### Remove dependencies
```bash
# Remove dependency
uv remove requests

# Remove dev dependency
uv remove pytest --dev

# Remove from specific group
uv remove sphinx --group docs
```

### Update dependencies
```bash
# Update all dependencies
uv lock --upgrade

# Update specific dependency
uv lock --upgrade-package requests

# Sync dependencies (install/update based on lock file)
uv sync

# Sync including dev dependencies
uv sync --dev

# Sync specific groups
uv sync --group docs --group test
```

### List dependencies
```bash
# Show dependency tree
uv tree

# Show outdated packages
uv lock --dry-run --upgrade
```

## Virtual Environments

### Create and manage environments
```bash
# Create virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create with custom name
uv venv my-env

# Activate environment (manual)
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows

# Run command in environment
uv run python script.py

# Run with specific Python version
uv run --python 3.11 python script.py
```

### Environment info
```bash
# Show Python path
uv run python -c "import sys; print(sys.executable)"

# Show installed packages
uv pip list
```

## Code Quality Tools

### Ruff - Modern All-in-One Linter & Formatter

**Ruff is an extremely fast linter and formatter written in Rust.**

```bash
# Add ruff as dev dependency
uv add ruff --dev

# Format code (replaces black)
uv run ruff format .

# Check formatting without making changes
uv run ruff format --check .

# Show diff of formatting changes
uv run ruff format --diff .

# Lint code (replaces pylint + isort)
uv run ruff check .

# Lint and auto-fix issues
uv run ruff check --fix .

# Lint specific rules (e.g., import sorting)
uv run ruff check --select I .

# Run both format and lint
uv run ruff format . && uv run ruff check --fix .

# Show all available rules
uv run ruff rule --all

# Generate ruff configuration
uv run ruff init
```

**ruff.toml or pyproject.toml configuration:**
```toml
[tool.ruff]
# Set line length (default is 88, same as black)
line-length = 88

# Target Python version
target-version = "py311"

# Exclude directories
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.lint]
# Enable rule sets
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
]

# Ignore specific rules
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

[tool.ruff.format]
# Use double quotes for strings
quote-style = "double"

# Indent with spaces
indent-style = "space"
```

**Quick Commands:**
```bash
# One command to format and lint
uv run ruff format . && uv run ruff check --fix .

# Create shell alias
alias uv-lint="uv run ruff check --fix . && uv run ruff format ."
```

### Combined Quality Check Script

```bash
# Add ruff
uv add ruff --dev

# Run all quality checks with ruff
uv run ruff check --fix . && uv run ruff format .

# Check without fixing (for CI)
uv run ruff check . && uv run ruff format --check .
```

**pyproject.toml configuration:**
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]

[project.scripts]
format = "ruff format ."
lint = "ruff check --fix ."
check = "bash -c 'ruff check . && ruff format --check .'"
```

### Run quality checks
```bash
# Format code
uv run ruff format .

# Lint and fix
uv run ruff check --fix .

# Check only (for CI, no changes made)
uv run ruff check . && uv run ruff format --check .

# Lint specific rules (e.g., imports only)
uv run ruff check --select I --fix .

# Show what would be fixed without making changes
uv run ruff check --diff .
```

## Running & Building

### Run Python code
```bash
# Run Python script
uv run python script.py

# Run module
uv run -m pytest

# Run with arguments
uv run python app.py --port 8000

# Run in development mode
uv run --dev python script.py
```

### Build project
```bash
# Build wheel and source distribution
uv build

# Build only wheel
uv build --wheel

# Build only source distribution
uv build --sdist
```

### Install project
```bash
# Install in development mode
uv pip install -e .

# Install from built wheel
uv pip install dist/my_project-1.0.0-py3-none-any.whl
```

## Tool Management

### Install and run global tools
```bash
# Install a tool globally (available system-wide)
uv tool install ruff
uv tool install black
uv tool install httpie

# Run a tool without installing it permanently
uv tool run ruff check .
uvx ruff check .         # shorthand for uv tool run

# List installed tools
uv tool list

# Upgrade a tool
uv tool upgrade ruff

# Uninstall a tool
uv tool uninstall ruff
```

> **Note:** `uv tool install` installs CLI tools globally (like `pipx`), while `uv add` adds packages as project dependencies.

## Advanced Usage

### Working with multiple Python versions
```bash
# Install Python version
uv python install 3.11

# List available Python versions
uv python list

# Use specific Python for project
uv init --python 3.11

# Switch Python version for existing project
uv python pin 3.10
```

### Workspace and multi-project management
```bash
# Create workspace with multiple projects
mkdir my-workspace
cd my-workspace
uv init --workspace

# Add member projects
uv init project-a
uv init project-b

# Sync entire workspace
uv sync --workspace
```

### Configuration files

**pyproject.toml example:**
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-project"
version = "0.1.0"
description = ""
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
dependencies = [
    "requests>=2.28.0",
]
requires-python = ">=3.8"

[project.optional-dependencies]
dev = [
    "ruff>=0.8.0",
    "pytest>=7.0.0",
]
docs = [
    "sphinx>=6.0.0",
    "sphinx-rtd-theme>=1.2.0",
]

[tool.uv]
dev-dependencies = [
    "pre-commit>=3.0.0",
]

[tool.ruff]
line-length = 88
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### Pre-commit hooks

```bash
# Add pre-commit
uv add pre-commit --dev

# Create .pre-commit-config.yaml with ruff
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      # Run the linter
      - id: ruff
        args: [--fix]
      # Run the formatter
      - id: ruff-format
EOF

# Install pre-commit hooks
uv run pre-commit install

# Run pre-commit on all files
uv run pre-commit run --all-files
```

### Environment variables and scripts
```bash
# Set environment variables for uv run
UV_PROJECT_ENVIRONMENT=development uv run python script.py

# Create shell alias for common commands
alias uvr="uv run"
alias uvs="uv sync"
alias uva="uv add"
alias uvfmt="uv run ruff format . && uv run ruff check --fix ."
```

## Quick Reference Commands

| Command | Description |
|---------|-------------|
| `uv init` | Create new project |
| `uv add package` | Add dependency |
| `uv remove package` | Remove dependency |
| `uv sync` | Install/update dependencies |
| `uv run cmd` | Run command in project environment |
| `uv build` | Build project |
| `uv lock` | Update lock file |
| `uv tree` | Show dependency tree |
| **Code Quality (Ruff)** | |
| `uv run ruff format .` | Format code |
| `uv run ruff check .` | Lint code |
| `uv run ruff check --fix .` | Lint and auto-fix issues |

## Tips and Best Practices

1. **Use Ruff for code quality** - Fast, all-in-one solution for formatting and linting
2. **Always use `uv run`** instead of activating virtual environments manually
3. **Pin Python version** in pyproject.toml for reproducible environments
4. **Use dependency groups** to separate dev, docs, and test dependencies
5. **Configure ruff** in pyproject.toml for consistent formatting across team
6. **Set up pre-commit hooks** with ruff for automated code quality checks
7. **Use workspaces** for multi-project repositories
8. **Keep uv updated** regularly with `uv self update`
9. **Use `uv sync`** instead of pip install for reproducible installs

## Why Ruff?

- **Speed**: 10-100x faster than traditional tools (written in Rust)
- **All-in-One**: Formatting, linting, import sorting in one tool
- **Modern**: Actively developed by Astral (same team as uv)
- **Simple**: One tool to install, configure, and run
- **Powerful**: Supports 800+ lint rules from popular Python linters