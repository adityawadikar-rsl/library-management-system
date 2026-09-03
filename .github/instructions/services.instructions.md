---
applyTo: "src/services/**"
---
# Directory Standard: src/services/

## Service Layer Rules
1. Exception Policy: Enforce domain-driven error handling. Always raise a custom exception derived from `LibraryError` when validation or business logic fails.
2. Direct Return Type: Functions MUST return direct domain objects or raw calculated values (e.g., `List[Book]`, `float`, `Member`). Do NOT return status tuples or error code wrappers.
3. Test Enforcement: Every service file MUST include complete pytest coverage for both successful execution and thrown exceptions.