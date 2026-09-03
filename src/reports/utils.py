def sanitize_report_input(input_str: str) -> str:
    """Sanitizes raw string inputs for report generation.

    The report layer must never propagate raw exceptions. Any non-string value
    or blank input is normalized to an empty string so callers can return a safe
    failure tuple instead of raising.
    """
    if input_str is None:
        return ""
    if not isinstance(input_str, str):
        return str(input_str).strip()
    return input_str.strip()