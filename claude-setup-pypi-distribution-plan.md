# Claude Setup CLI - PyPI Distribution Plan

## Executive Summary

This plan outlines the comprehensive setup for packaging and distributing the `claude-setup` CLI application to PyPI using GitHub Actions as the CI/CD pipeline. The current project is well-structured with Click framework, pipenv dependency management, comprehensive test suite (98% coverage), and existing Makefile build targets.

**Key Objectives:**
- Automated PyPI publishing via GitHub Actions
- Secure credential management and release workflow
- Comprehensive testing and quality gates
- Semantic versioning and automated version management
- Professional package metadata and documentation

**Timeline:** 2-3 days for full implementation and testing

## Current Project Assessment

**Strengths:**
- Well-structured Python package with `src/` layout
- Comprehensive test suite with 98% coverage
- Existing Makefile with build/upload targets
- Click CLI framework properly configured
- pipenv for dependency management

**Areas Needing Enhancement:**
- Missing GitHub Actions workflows
- Basic setup.py needs enhancement for PyPI
- No automated version management
- Missing security configurations
- Documentation needs PyPI-specific updates

## Detailed Implementation Plan

### Phase 1: Foundation Setup (Day 1)

#### 1.1 Enhanced Package Configuration

**Update setup.py for PyPI distribution:**

```python
from setuptools import setup, find_packages
import os

# Read version from __init__.py
def get_version():
    with open("src/claude_setup/__init__.py", "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    raise RuntimeError("Version not found")

# Read README for long description
def get_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

setup(
    name="claude-setup",
    version=get_version(),
    author="Your Name",
    author_email="your.email@example.com",
    description="CLI tool to configure Claude for AWS Bedrock",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/claude-setup",
    project_urls={
        "Bug Reports": "https://github.com/your-username/claude-setup/issues",
        "Source": "https://github.com/your-username/claude-setup",
        "Documentation": "https://github.com/your-username/claude-setup/blob/main/README.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords="claude aws bedrock cli setup configuration",
    install_requires=[
        "click>=8.1.0",
        "boto3>=1.34.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "mypy",
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "build",
            "twine",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-setup=claude_setup.cli:cli",
        ],
    },
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
```

**Create pyproject.toml for modern Python packaging:**

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "claude-setup"
dynamic = ["version"]
description = "CLI tool to configure Claude for AWS Bedrock"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"},
]
keywords = ["claude", "aws", "bedrock", "cli", "setup", "configuration"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Systems Administration",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Operating System :: OS Independent",
    "Environment :: Console",
]
requires-python = ">=3.8"
dependencies = [
    "click>=8.1.0",
    "boto3>=1.34.0",
    "rich>=13.7.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "black",
    "flake8",
    "mypy",
    "pytest",
    "pytest-cov",
    "pytest-mock",
    "build",
    "twine",
]

[project.urls]
Homepage = "https://github.com/your-username/claude-setup"
Repository = "https://github.com/your-username/claude-setup"
Documentation = "https://github.com/your-username/claude-setup/blob/main/README.md"
"Bug Reports" = "https://github.com/your-username/claude-setup/issues"
Changelog = "https://github.com/your-username/claude-setup/blob/main/CHANGELOG.md"

[project.scripts]
claude-setup = "claude_setup.cli:cli"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.dynamic]
version = {attr = "claude_setup.__version__"}

[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
namespace_packages = true
```

#### 1.2 Version Management Strategy

**Create version management system:**
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Automated version bumping via GitHub Actions
- Version synchronization across all files

**Enhanced __init__.py with version info:**

```python
"""Claude Setup CLI - AWS Bedrock Configuration Tool."""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "CLI tool to configure Claude for AWS Bedrock"
```

#### 1.3 Project Structure Enhancements

**Create additional required files:**

1. **MANIFEST.in** - Include additional files in distribution
2. **LICENSE** - Choose appropriate license (MIT recommended)
3. **CHANGELOG.md** - Version history tracking
4. **.gitignore** enhancements for packaging
5. **requirements-dev.txt** - Development dependencies

### Phase 2: GitHub Actions CI/CD Pipeline (Day 1-2)

#### 2.1 Core Workflow Structure

**Create `.github/workflows/` directory with multiple workflows:**

1. **ci.yml** - Continuous Integration
2. **release.yml** - Release Management
3. **test-pypi.yml** - TestPyPI Publishing
4. **pypi-publish.yml** - Production PyPI Publishing

#### 2.2 Continuous Integration Workflow

**`.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install pipenv
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
    
    - name: Cache pipenv dependencies
      uses: actions/cache@v3
      with:
        path: ~/.local/share/virtualenvs
        key: ${{ runner.os }}-python-${{ matrix.python-version }}-pipenv-${{ hashFiles('**/Pipfile.lock') }}
        restore-keys: |
          ${{ runner.os }}-python-${{ matrix.python-version }}-pipenv-
    
    - name: Install dependencies
      run: |
        pipenv install --dev --deploy
    
    - name: Lint with flake8
      run: |
        pipenv run flake8 src/ --max-line-length=100 --extend-ignore=E203,W503
    
    - name: Type check with mypy
      run: |
        pipenv run mypy src/ --ignore-missing-imports
    
    - name: Format check with black
      run: |
        pipenv run black --check src/ --line-length=100
    
    - name: Test with pytest
      run: |
        pipenv run pytest --cov=src/claude_setup --cov-report=xml --cov-report=term-missing
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install pipenv
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
    
    - name: Install dependencies
      run: |
        pipenv install --dev --deploy
    
    - name: Security check with pipenv
      run: |
        pipenv check --categories security
    
    - name: Run bandit security linter
      run: |
        pipenv run pip install bandit[toml]
        pipenv run bandit -r src/ -f json -o bandit-report.json || true
    
    - name: Upload bandit report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: bandit-report
        path: bandit-report.json

  build-test:
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: |
        python -m build
    
    - name: Check package with twine
      run: |
        twine check dist/*
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist-files
        path: dist/
```

#### 2.3 Release Management Workflow

**`.github/workflows/release.yml`**

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  create-release:
    runs-on: ubuntu-latest
    outputs:
      upload_url: ${{ steps.create_release.outputs.upload_url }}
    steps:
    - uses: actions/checkout@v4
    
    - name: Create Release
      id: create_release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
        body: |
          ## Changes
          
          See [CHANGELOG.md](https://github.com/${{ github.repository }}/blob/main/CHANGELOG.md) for detailed changes.
          
          ## Installation
          
          ```bash
          pip install claude-setup==${{ github.ref_name }}
          ```

  test-and-build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install pipenv
      run: |
        python -m pip install --upgrade pip
        pip install pipenv
    
    - name: Install dependencies
      run: |
        pipenv install --dev --deploy
    
    - name: Run full test suite
      run: |
        pipenv run pytest --cov=src/claude_setup --cov-report=term-missing --cov-fail-under=95
    
    - name: Build package
      if: matrix.python-version == '3.11'
      run: |
        pip install build
        python -m build
    
    - name: Upload build artifacts
      if: matrix.python-version == '3.11'
      uses: actions/upload-artifact@v3
      with:
        name: release-dist
        path: dist/

  publish-testpypi:
    runs-on: ubuntu-latest
    needs: [create-release, test-and-build]
    environment: test-release
    steps:
    - uses: actions/checkout@v4
    
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: release-dist
        path: dist/
    
    - name: Publish to TestPyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.TEST_PYPI_API_TOKEN }}
        repository_url: https://test.pypi.org/legacy/
        verbose: true

  publish-pypi:
    runs-on: ubuntu-latest
    needs: [publish-testpypi]
    environment: production-release
    steps:
    - uses: actions/checkout@v4
    
    - name: Download build artifacts
      uses: actions/download-artifact@v3
      with:
        name: release-dist
        path: dist/
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
        verbose: true
```

#### 2.4 Automated Version Bumping Workflow

**`.github/workflows/version-bump.yml`**

```yaml
name: Version Bump

on:
  workflow_dispatch:
    inputs:
      version_type:
        description: 'Version bump type'
        required: true
        default: 'patch'
        type: choice
        options:
        - patch
        - minor
        - major

jobs:
  bump-version:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        fetch-depth: 0
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.11"
    
    - name: Install bump2version
      run: |
        pip install bump2version
    
    - name: Configure git
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
    
    - name: Bump version
      run: |
        bump2version ${{ github.event.inputs.version_type }}
    
    - name: Push changes
      run: |
        git push origin main --tags
```

### Phase 3: Security and Quality Assurance (Day 2)

#### 3.1 Security Configuration

**GitHub Secrets Setup:**
- `PYPI_API_TOKEN` - Production PyPI API token
- `TEST_PYPI_API_TOKEN` - TestPyPI API token
- `CODECOV_TOKEN` - Code coverage reporting (optional)

**Security best practices:**
- Use GitHub Environments for release protection
- Require manual approval for production releases
- Use trusted publishers (OIDC) when available
- Implement secret scanning and dependency scanning

#### 3.2 Quality Gates

**Mandatory checks before release:**
1. All tests pass (98%+ coverage maintained)
2. Code linting passes (flake8)
3. Type checking passes (mypy)
4. Code formatting verified (black)
5. Security scan passes (bandit, pipenv check)
6. Package building succeeds
7. Package validation passes (twine check)

#### 3.3 Branch Protection Rules

**Configure branch protection for `main`:**
- Require status checks to pass
- Require branches to be up to date
- Require review from code owners
- Restrict pushes to maintain code quality

### Phase 4: Documentation and Release Process (Day 3)

#### 4.1 Documentation Updates

**README.md enhancements for PyPI:**
- Installation instructions
- Quick start guide
- API documentation
- Contributing guidelines
- License information
- Badges for build status, coverage, PyPI version

**CHANGELOG.md creation:**
- Semantic versioning format
- Automated generation from git commits
- Release notes template

#### 4.2 Release Workflow Process

**Standard Release Process:**
1. Create feature branch from `main`
2. Implement changes with tests
3. Run local quality checks: `make check`
4. Create pull request
5. Automated CI runs all checks
6. Code review and approval
7. Merge to `main`
8. Manual version bump (workflow dispatch)
9. Tag triggers automated release workflow
10. TestPyPI publication (with approval)
11. Production PyPI publication (with approval)

**Hotfix Release Process:**
1. Create hotfix branch from `main`
2. Implement critical fix with tests
3. Emergency review process
4. Direct merge with expedited release

### Phase 5: Monitoring and Maintenance

#### 5.1 Release Monitoring

**Automated monitoring:**
- GitHub Actions workflow status
- PyPI download statistics
- Dependency security alerts
- Test coverage trends

#### 5.2 Maintenance Tasks

**Regular maintenance:**
- Dependency updates (monthly)
- Security vulnerability patches
- Python version compatibility updates
- Documentation updates
- Performance optimizations

## Implementation Checklist

### Prerequisites
- [ ] GitHub repository with admin access
- [ ] PyPI account with 2FA enabled
- [ ] TestPyPI account for testing
- [ ] API tokens for both PyPI and TestPyPI

### Phase 1: Foundation
- [ ] Update setup.py with enhanced metadata
- [ ] Create pyproject.toml
- [ ] Update __init__.py with version info
- [ ] Create MANIFEST.in
- [ ] Add LICENSE file
- [ ] Create CHANGELOG.md
- [ ] Update .gitignore for packaging

### Phase 2: CI/CD Pipeline
- [ ] Create .github/workflows/ directory
- [ ] Implement ci.yml workflow
- [ ] Implement release.yml workflow
- [ ] Implement version-bump.yml workflow
- [ ] Configure GitHub Secrets
- [ ] Set up GitHub Environments

### Phase 3: Security
- [ ] Configure branch protection rules
- [ ] Set up security scanning
- [ ] Implement secret management
- [ ] Configure trusted publishers (if available)

### Phase 4: Documentation
- [ ] Update README.md for PyPI
- [ ] Create comprehensive CHANGELOG.md
- [ ] Add contributing guidelines
- [ ] Update docstrings and type hints

### Phase 5: Testing
- [ ] Test CI/CD pipeline on test branch
- [ ] Verify TestPyPI publication
- [ ] Test package installation from TestPyPI
- [ ] Verify production PyPI publication
- [ ] Test package installation from PyPI

## Risk Assessment and Mitigation

### High Risk Areas
1. **Credential Management**: Use GitHub Secrets, enable 2FA
2. **Accidental Production Release**: Use GitHub Environments with approval
3. **Breaking Changes**: Comprehensive test suite, semantic versioning
4. **Security Vulnerabilities**: Automated scanning, regular updates

### Rollback Procedures

**PyPI Package Rollback:**
1. Immediately yank problematic version from PyPI
2. Create hotfix with version bump
3. Emergency release process
4. Communicate to users via GitHub releases

**CI/CD Pipeline Issues:**
1. Disable problematic workflow
2. Revert workflow changes
3. Fix and test in feature branch
4. Gradual rollout of fixes

## Success Metrics

### Technical Metrics
- Build success rate >99%
- Test coverage maintained >95%
- Release cycle time <30 minutes
- Zero security vulnerabilities in releases

### User Experience Metrics
- Easy installation (`pip install claude-setup`)
- Clear documentation and examples
- Responsive issue resolution
- Regular feature updates

## Conclusion

This comprehensive plan provides a production-ready CI/CD pipeline for the claude-setup CLI application. The implementation focuses on:

- **Security**: Multi-layered security with secret management and scanning
- **Quality**: Comprehensive testing and quality gates
- **Automation**: Fully automated build, test, and release pipeline
- **Reliability**: Rollback procedures and monitoring
- **Maintainability**: Clear documentation and standardized processes

The phased approach allows for incremental implementation and testing, ensuring a smooth transition to automated PyPI distribution while maintaining the high code quality standards already established in the project.