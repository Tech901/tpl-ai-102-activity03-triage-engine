"""
JSON Schema Definitions for Activity 3 - 311 Triage Engine

This module defines the JSON schemas used to validate model outputs
for Memphis 311 request classification and routing.
"""

# ---------------------------------------------------------------------------
# Valid categories
# ---------------------------------------------------------------------------
VALID_CATEGORIES = (
    "Pothole",
    "Noise Complaint",
    "Trash/Litter",
    "Street Light",
    "Water/Sewer",
    "Other",
)

VALID_PRIORITIES = {"low", "standard", "high", "critical"}


# ---------------------------------------------------------------------------
# TODO: Step 2 - Define the CLASSIFICATION_SCHEMA
# ---------------------------------------------------------------------------
# Define a JSON Schema (as a Python dict) that validates the model's
# classification output. The schema must require these fields:
#
#   - category: string, one of the VALID_CATEGORIES
#   - confidence: number between 0.0 and 1.0
#   - reasoning: string, at least 5 characters
#
# Use the jsonschema library format. Example structure:
#
# CLASSIFICATION_SCHEMA = {
#     "type": "object",
#     "properties": {
#         "category": {
#             "type": "string",
#             "enum": [...]
#         },
#         ...
#     },
#     "required": [...],
#     "additionalProperties": False
# }

CLASSIFICATION_SCHEMA = {}


# ---------------------------------------------------------------------------
# TODO: Step 2 - Define the ROUTING_SCHEMA
# ---------------------------------------------------------------------------
# Define a JSON Schema that validates the complete routing decision.
# The schema must require these fields:
#
#   - category: string (same enum as classification)
#   - confidence: number between 0.0 and 1.0
#   - reasoning: string
#   - department: string (the routed department name)
#   - sla_hours: integer, minimum 1
#   - priority: string, one of "low", "standard", "high", "critical"
#
# ROUTING_SCHEMA = { ... }

ROUTING_SCHEMA = {}


# ---------------------------------------------------------------------------
# TODO: Step 2 - Implement validate_against_schema
# ---------------------------------------------------------------------------
def validate_against_schema(data: dict, schema: dict) -> dict:
    """Validate a data dict against a JSON schema.

    Args:
        data: The dictionary to validate.
        schema: The JSON schema to validate against.

    Returns:
        dict with keys:
          - valid: bool
          - errors: list of error message strings (empty if valid)
    """
    # TODO: Step 2.3 - Implement validation using jsonschema.validate()
    #
    # 1. Import jsonschema (at the top of this function or module)
    # 2. Call jsonschema.validate(data, schema)
    # 3. Return {"valid": True, "errors": []} on success
    # 4. Catch jsonschema.ValidationError and return
    #    {"valid": False, "errors": [str(e.message)]}
    # 5. Catch any other exception and return a generic error
    #
    # Hint: You may also want to handle jsonschema.SchemaError for
    # malformed schemas (return valid=False with the schema error message).
    raise NotImplementedError("Implement validate_against_schema in Step 2")
