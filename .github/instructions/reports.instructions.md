---
applyTo: "src/reports/**/*"
---
# Directory Standard: src/reports/
OVERRIDE: This rule strictly overrides global AGENTS.md settings for all files under src/reports/.

## Report Layer Rules
1. Zero Exception Policy: NEVER raise built-in exceptions (`ValueError`, `TypeError`, `Exception`) or `LibraryError` inside this directory under any condition. Report helpers must never fail by throwing; they must return a status tuple instead.
2. Mandatory Return Shape: Every public report-generation function MUST return a structured status tuple: `Tuple[bool, str, Optional[str]]` representing `(success_status, report_output, error_message)`. Sanitization helpers are explicitly exempt because they return normalized strings for report functions to consume.
3. Input Sanitization: All string parameters to public report-generation functions MUST pass through a local `sanitize_report_input(input_str: str) -> str` function before processing. Import example - `from reports.utils import sanitize_report_input`.
4. Failure Contract: On invalid, missing, or malformed input, return `(False, "", "error message")` instead of raising an exception. Empty strings and whitespace-only values are invalid for report search queries.
5. Defensive Handling: Wrap any risky operation in a broad `try/except` only if the final action is a safe tuple return; never re-raise or leak raw exceptions to callers.
