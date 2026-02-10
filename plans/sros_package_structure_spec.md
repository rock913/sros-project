# SROS Package Structure Specification

## 1. Overview

This document defines the standardized package structure for SROS following Python packaging best practices and PEP 561 guidelines. The structure ensures proper distribution, installation, and maintenance of the SROS CLI tool.

## 2. Package Layout

### 2.1 Root Directory Structure
```
sros/
├── pyproject.toml              # Build system configuration
├── README.md                   # Package description
├── LICENSE                     # License information
├── CHANGELOG.md                # Version history
├── .gitignore                  # Git ignore patterns
├── docs/                       # Package documentation
│   ├── installation.md
│   ├── usage.md
│   └── api-reference.md
├── src/
│   └── sros/                   # Main package
│       ├── __init__.py         # Package initialization
│       ├── __about__.py        # Package metadata
│       ├── cli.py              # CLI application entry point
│       ├── constants.py        # Shared constants
│       ├── config/
│       │   ├── __init__.py
│       │   ├── settings.py     # Configuration management
│       │   └── defaults.py     # Default settings
│       ├── core/
│       │   ├── __init__.py
│       │   ├── gateway.py      # Gateway management
│       │   ├── project.py      # Project management
│       │   └── system.py       # System operations
│       ├── gateway/            # Gateway server implementation
│       │   ├── __init__.py
│       │   ├── main.py         # Gateway entry point
│       │   ├── server.py       # Gateway server logic
│       │   └── config.json     # Gateway configuration
│       ├── servers/            # Sub-server implementations
│       │   ├── __init__.py
│       │   ├── federal_academic_search/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   └── config.py
│       │   ├── manuscript_manager/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   └── config.py
│       │   ├── duckdb_memory/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   └── config.py
│       │   ├── context_ingester/
│       │   │   ├── __init__.py
│       │   │   ├── main.py
│       │   │   └── config.py
│       │   └── zotero_expert/
│       │       ├── __init__.py
│       │       ├── main.py
│       │       └── config.py
│       ├── templates/          # Project templates and assets
│       │   ├── __init__.py
│       │   ├── project/
│       │   │   ├── draft.md.j2
│       │   │   ├── ideas.md.j2
│       │   │   ├── .roomodes.j2
│       │   │   └── .env.j2
│       │   └── prompts/
│       │       ├── writer.yaml.j2
│       │       └── researcher.yaml.j2
│       ├── utils/              # Utility functions
│       │   ├── __init__.py
│       │   ├── filesystem.py   # File system operations
│       │   ├── process.py      # Process management
│       │   ├── validation.py   # Input validation
│       │   └── formatting.py   # Output formatting
│       └── exceptions.py       # Custom exceptions
└── tests/                      # Test suite
    ├── __init__.py
    ├── conftest.py             # Test configuration
    ├── unit/
    │   ├── __init__.py
    │   ├── test_cli.py
    │   ├── test_project.py
    │   └── test_gateway.py
    ├── integration/
    │   ├── __init__.py
    │   └── test_full_workflow.py
    └── fixtures/
        ├── __init__.py
        └── sample_configs/
```

## 3. pyproject.toml Configuration

### 3.1 Build System
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "sros"
dynamic = ["version"]
description = "Scientific Research Operating System - AI-powered research assistant"
readme = "README.md"
license = {file = "LICENSE"}
authors = [
    {name = "SROS Development Team", email = "dev@sros.org"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering",
    "Topic :: Text Processing :: Markup :: Markdown"
]
keywords = ["research", "ai", "academic", "writing", "mcp"]

[project.urls]
Homepage = "https://github.com/sros/sros"
Repository = "https://github.com/sros/sros"
Documentation = "https://sros.readthedocs.io"
"Bug Tracker" = "https://github.com/sros/sros/issues"

[project.scripts]
sros = "sros.cli:main"

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "pre-commit>=3.0"
]
docs = [
    "sphinx>=5.0",
    "sphinx-rtd-theme>=1.0"
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
sros = [
    "templates/**/*",
    "gateway/config.json",
    "servers/*/config.json"
]
```

### 3.2 Development Tools Configuration
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --tb=short"
```

## 4. Package Entry Points

### 4.1 CLI Entry Point (`src/sros/cli.py`)
```python
import typer
from rich.console import Console

from sros.core.project import ProjectManager
from sros.core.gateway import GatewayManager
from sros.core.system import SystemChecker

app = typer.Typer(
    name="sros",
    help="Scientific Research Operating System - AI-powered research assistant",
    no_args_is_help=True
)

console = Console()

# Import commands
from sros.commands.init import init_command
from sros.commands.start import start_command
from sros.commands.status import status_command, doctor_command

# Register commands
app.command()(init_command)
app.command()(start_command)
app.command()(status_command)
app.command()(doctor_command)

def main():
    """Entry point for the CLI application."""
    app()

if __name__ == "__main__":
    main()
```

### 4.2 Package Initialization (`src/sros/__init__.py`)
```python
"""Scientific Research Operating System - AI-powered research assistant."""

__version__ = "2.3.0"
__author__ = "SROS Development Team"
__email__ = "dev@sros.org"
__license__ = "MIT"

# Public API
from sros.core.project import ProjectManager
from sros.core.gateway import GatewayManager
from sros.core.system import SystemChecker

__all__ = [
    "ProjectManager",
    "GatewayManager", 
    "SystemChecker",
    "__version__",
    "__author__",
    "__email__",
    "__license__"
]
```

## 5. Resource Management

### 5.1 Template Resources
Templates are stored in `src/sros/templates/` and accessed using `importlib.resources`:

```python
from importlib import resources
from sros import templates

def get_template(template_name: str) -> str:
    """Get template content from package resources."""
    template_path = f"templates/{template_name}"
    return resources.read_text(templates, template_path)
```

### 5.2 Configuration Files
Server configurations are bundled as package data and accessed similarly:

```python
from importlib import resources
from sros.gateway import config

def get_gateway_config() -> dict:
    """Load gateway configuration from package resources."""
    config_content = resources.read_text(config, "config.json")
    return json.loads(config_content)
```

## 6. Testing Structure

### 6.1 Test Organization
Tests follow pytest conventions with clear separation:
- `unit/` - Individual component tests
- `integration/` - Multi-component workflow tests
- `fixtures/` - Test data and configurations

### 6.2 Test Requirements
```python
# tests/conftest.py
import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_workspace():
    """Create temporary workspace for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)
```

## 7. Distribution Considerations

### 7.1 Platform Compatibility
- Cross-platform support (Windows, macOS, Linux)
- Python 3.8+ compatibility
- Proper handling of file paths and permissions

### 7.2 Dependency Management
- Minimal core dependencies
- Optional extras for development/testing
- Clear version pinning where necessary
- Compatibility with major package managers

## 8. Maintenance Guidelines

### 8.1 Versioning
Follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes to public API
- MINOR: New features, backward compatible
- PATCH: Bug fixes, backward compatible

### 8.2 Release Process
1. Update version in `src/sros/__about__.py`
2. Update changelog
3. Run full test suite
4. Build and test distribution packages
5. Upload to PyPI
6. Tag release in version control

This structure ensures SROS follows Python packaging best practices while maintaining the functionality needed for the research automation system.