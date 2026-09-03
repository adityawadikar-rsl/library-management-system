# AGENTS.md

# Project: Library Management System
## Core Python Coding Standards

### Stack & Dependencies
- Python 3.10+ (Standard Library only)
- Test Runner: pytest

### 1. Type Hints & Naming
- Every function, method, and return type MUST include explicit Python type annotations.
- Input parameters accepting complex data structures or dictionary payloads MUST use the `Payload` suffix (e.g., `member_payload: Dict[str, Any]`).

### 2. Error Handling & Custom Exceptions
- NEVER raise raw built-in exceptions (`ValueError`, `Exception`, `KeyError`) directly.
- Always import `LibraryError` (or a subclass) from `models.exceptions` (e.g., `from models.exceptions import LibraryError, FineCalculationError`).
- Raise custom exceptions derived from `LibraryError` for all validation and domain errors.

### 3. Automated Test Generation
- Every generated Python file MUST include unit tests.
- Append a standalone `if __name__ == "__main__":` or `pytest` function block at the bottom of the generated file OR create a corresponding file in `tests/test_<module_name>.py`.

### 4. Workspace Context Note
- Pre-existing files (`src/models/*`, `src/services/library_manager.py`) contain legacy patterns. 
- DO NOT replicate legacy exception handling or parameter naming from existing files. ALWAYS strictly follow the rules in this instruction file for all new code.