# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Zaim CSV Converter**, a Python tool that converts CSV files from various financial accounts (credit cards, banks, e-money cards) into Zaim's import format. It supports multiple account types including WAON, MUFG Bank, Amazon.co.jp, PayPal, and others.

## Development Commands

### Essential Commands
- **Setup environment**: `uv sync`
- **Run converter**: `uv run convert.py`
- **Run tests**: `uv run invoke test` (fast tests) or `uv run invoke test.all` (all tests)
- **Run tests with coverage**: `uv run invoke test.coverage`
- **Lint code**: `uv run invoke lint` (fast) or `uv run invoke lint.deep` (thorough)
- **Format code**: `uv run invoke style`
- **Build distribution**: `uv run invoke dist`

### Available Invoke Tasks
Run `uv run invoke --list` to see all available tasks. Key collections include:
- `lint.*` - Various linting tools (ruff, flake8, mypy, pylint, etc.)
- `test.*` - Testing with different configurations
- `style.*` - Code formatting
- `clean.*` - Cleanup operations

## Architecture

### Core Structure
- **Entry point**: `convert.py` - Simple wrapper calling `ZaimCsvConverter.execute()`
- **Main package**: `zaimcsvconverter/` - Core conversion logic
- **Configuration**: `config.yml` (copy from `config.yml.dist`)
- **Input/Output directories**: `csvinput/` and `csvoutput/`
- **Conversion tables**: `csvconverttable/` - Store and item mapping definitions

### Key Components

#### Data Flow Architecture
1. **Data Sources** (`inputtooutput/datasources/`): CSV file readers and parsers for each account type
2. **Converters** (`inputtooutput/converters/recordtozaim/`): Transform account-specific records to Zaim format
3. **Exporters** (`inputtooutput/exporters/zaim/`): Output Zaim-compatible CSV files
4. **Error Handling** (`errorhandling/`, `errorreporters/`): Validation and error reporting

#### Account Support Pattern
Each supported account follows a consistent pattern with:
- **Data model** (`data/[account].py`): Pydantic models for CSV structure
- **Record processor** (`records/[account].py`): Raw CSV to structured data
- **Converter** (`converters/recordtozaim/[account].py`): Business logic for Zaim conversion
- **CSV converter** (`datasources/csvfile/converters/[account].py`): File processing

### Configuration System
- Uses `yamldataclassconfig` for YAML configuration loading
- Account-specific settings in `config.yml` (account names, skip rules, transfer settings)
- Conversion tables in CSV format under `csvconverttable/` directory

### Dependencies
- **Core**: SQLAlchemy (database), Pydantic (validation), numpy (data processing)
- **CSV processing**: Custom libraries (`godslayer`, `errorcollector`, `pydantictypes`)
- **Dev tools**: Extensive linting stack (ruff, mypy, pylint, flake8), pytest for testing

## Working with the Codebase

### Adding New Account Support
1. Create data model in `data/[account].py`
2. Add record processor in `inputtooutput/datasources/csvfile/records/[account].py`
3. Implement converter in `inputtooutput/converters/recordtozaim/[account].py`
4. Add CSV file processor in `inputtooutput/datasources/csvfile/converters/[account].py`
5. Update configuration schema and documentation

### Testing
- Tests located in `tests/` with comprehensive coverage requirements
- Use `pytest.mark.slow` for performance-intensive tests
- Factory Boy used for test data generation
- Database fixtures available in `tests/testlibraries/`

### Code Quality Standards
- Strict type checking with mypy
- Comprehensive linting (ruff, flake8, pylint with OpenStack hacking rules)
- Security scanning with bandit and semgrep
- Code complexity monitoring with xenon and radon
- Docstring requirements (Google style, minimum 7 characters)