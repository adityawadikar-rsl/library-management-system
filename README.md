# Library Inventory System - AI Artifacts Playground

This is a lightweight Python project built entirely with the Python standard library. No virtual environments or external dependencies (like `pip install ...`) are required. 

This repository serves as a sandbox for practicing how to manage AI coding assistants (like GitHub Copilot, Cursor, Windsurf, or Claude Code). 
You will use this codebase to test project-wide instructions, folder-scoped rules, and reusable AI skills without getting bogged down in complex application logic.

## Project Structure

The codebase is intentionally separated into distinct architectural layers to help you test directory-specific AI rules:

*   `src/models/`: Contains the data structures (`Book` and `Member`).
*   `src/services/`: Contains the business logic and state management (`LibraryManager`).
*   `src/reports/`: Contains safe, tuple-returning functions for formatting output strings.
*   `src/main.py`: The interactive command-line interface.
*   `tests/`: Pytest coverage for services and report formatters.

```
library_management_system
├── .github
│   ├── instructions
│   │   ├── reports.instructions.md
│   │   └── services.instructions.md
│   └── skills
│       └── book-crud
│           └── SKILL.md
├── AGENTS.md
├── README.md
├── src
│   ├── main.py
│   ├── models
│   │   ├── book.py
│   │   ├── category.py
│   │   ├── exceptions.py
│   │   ├── member.py
│   │   └── publisher.py
│   ├── reports
│   │   ├── formatter.py
│   │   ├── search_formatter.py
│   │   └── utils.py
│   └── services
│       ├── fine_calculator.py
│       ├── library_manager.py
│       ├── publisher_repository.py
│       └── search_service.py
└── tests
    ├── README.md
    ├── test_category.py
    ├── test_fine_calculator.py
    ├── test_formatter.py
    ├── test_library_manager.py
    ├── test_publisher_repository.py
    ├── test_search_formatter.py
    └── test_search_service.py                        
```

The scoped instruction files live under `.github/instructions/`; the reusable CRUD skill lives under `.github/skills/book-curd/`.

## How to Run

Navigate to the root directory of the project in your terminal and execute the main script using Python:

```bash
python3 src/main.py
```

Tests
```bash
PYTHONPATH=src python3 -m pytest -q
```