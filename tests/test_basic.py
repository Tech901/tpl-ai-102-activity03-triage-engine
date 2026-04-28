"""Visible tests for Activity 3 - 311 Triage Engine.

Students can run these locally to verify their work before submission.
Run with: pytest tests/ -v
"""
import json
import os
import sys

import pytest

# Ensure the activity root is on sys.path so `from app.xxx import ...` works
# regardless of the working directory pytest is invoked from.
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.abspath(PROJECT_ROOT))
RESULT_PATH = os.path.join(PROJECT_ROOT, "result.json")
REPORT_PATH = os.path.join(PROJECT_ROOT, "eval_report.json")
RULES_PATH = os.path.join(PROJECT_ROOT, "data", "routing_rules.json")
EVAL_SET_PATH = os.path.join(PROJECT_ROOT, "data", "eval_set.json")
PRICING_PATH = os.path.join(PROJECT_ROOT, "data", "pricing.json")


# ---------------------------------------------------------------------------
# 0. Environment setup check
# ---------------------------------------------------------------------------

def test_env_configured():
    """Check that .env exists with Azure AI Foundry credentials."""
    env_path = os.path.join(PROJECT_ROOT, ".env")
    if not os.path.exists(env_path):
        pytest.skip(
            ".env file not found — copy .env.example to .env and add your "
            "Azure AI Foundry credentials (see Step 0 in README.md)"
        )
    with open(env_path) as f:
        content = f.read()
    # Check that placeholder values have been replaced
    if "your-api-key-here" in content or "your-resource" in content:
        pytest.skip(
            ".env still contains placeholder values — update with your "
            "actual Azure AI Foundry endpoint and API key (see Step 0)"
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def result():
    """Load the student's result.json."""
    if not os.path.exists(RESULT_PATH):
        pytest.skip("result.json not found - run 'python app/main.py' first")
    with open(RESULT_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 1. Canary: result.json must exist
# ---------------------------------------------------------------------------

def test_result_exists():
    """result.json file must exist."""
    assert os.path.exists(RESULT_PATH), "Run 'python app/main.py' to generate result.json"


# ---------------------------------------------------------------------------
# 2. Contract: required fields, task name, and structure
# ---------------------------------------------------------------------------

def test_result_structure(result):
    """result.json outputs must contain temperature_experiment and evaluation keys."""
    outputs = result["outputs"]
    assert "temperature_experiment" in outputs, \
        "Missing 'temperature_experiment' in outputs - complete Step 4"
    assert "evaluation" in outputs, \
        "Missing 'evaluation' in outputs - complete Step 5"


def test_required_fields(result):
    """result.json must have required top-level fields."""
    for field in ("task", "status", "outputs", "metadata"):
        assert field in result, f"Missing required field: {field}"


def test_task_name(result):
    """Task must be 'triage_engine'."""
    assert result["task"] == "triage_engine"


def test_status_valid(result):
    """Status must be one of the valid values."""
    assert result["status"] in ("success", "partial", "error"), \
        f"Invalid status: {result['status']}"


# ---------------------------------------------------------------------------
# 3. Classification: system message and categories
# ---------------------------------------------------------------------------

def test_system_message_defined():
    """SYSTEM_MESSAGE must be defined and non-empty."""
    from app.main import SYSTEM_MESSAGE

    assert isinstance(SYSTEM_MESSAGE, str), "SYSTEM_MESSAGE must be a string"
    assert len(SYSTEM_MESSAGE.strip()) > 50, \
        "SYSTEM_MESSAGE is too short - include role, categories, and constraints"


def test_system_message_has_categories():
    """SYSTEM_MESSAGE must mention the six 311 categories."""
    from app.main import SYSTEM_MESSAGE

    msg = SYSTEM_MESSAGE.lower()
    required = ["pothole", "noise", "trash", "street light", "water", "other"]
    for term in required:
        assert term in msg, f"SYSTEM_MESSAGE missing category reference: {term}"


def test_prompt_templates_exist():
    """At least 3 prompt template functions must be implemented."""
    from app import prompts

    template_names = ["classify_request", "classify_with_context", "batch_classify"]
    for name in template_names:
        func = getattr(prompts, name, None)
        assert func is not None, f"Missing template function: {name}"
        assert callable(func), f"{name} must be callable"


def test_classify_request_template():
    """classify_request template must return a non-empty string."""
    from app.prompts import classify_request

    result = classify_request("Test pothole on Main Street")
    assert isinstance(result, str), "Template must return a string"
    assert len(result) > 20, "Template output is too short"
    assert "pothole" in result.lower() or "Main Street" in result, \
        "Template must include the request text"


def test_classify_request_returns_category():
    """classify_request must return a dict with a valid category."""
    from app.main import classify_request
    try:
        result = classify_request("Large pothole on Poplar Avenue near the mall")
        assert isinstance(result, dict), "classify_request must return a dict"
        assert "category" in result, "Result must contain 'category'"
        assert result["category"] in {
            "Pothole", "Noise Complaint", "Trash/Litter",
            "Street Light", "Water/Sewer", "Other",
        }, f"Invalid category: {result['category']}"
    except NotImplementedError:
        pytest.fail("classify_request still raises NotImplementedError — complete Step 1")
    except (ConnectionError, TimeoutError, OSError):
        pytest.skip("API unavailable")
    except Exception as e:
        if any(code in str(e) for code in ("401", "404", "429")):
            pytest.skip("API credentials unavailable")
        raise


def test_classify_request_correct_category():
    """classify_request must return the correct category, not just any valid one."""
    from app.main import classify_request
    try:
        result = classify_request(
            "Broken street light on Main Street that has been dark for a week"
        )
        assert isinstance(result, dict), "classify_request must return a dict"
        assert result.get("category") == "Street Light", (
            f"Expected category 'Street Light' for a broken street light request, "
            f"got '{result.get('category')}'. Check your SYSTEM_MESSAGE categories "
            "and prompt template."
        )
    except NotImplementedError:
        pytest.fail("classify_request still raises NotImplementedError — complete Step 1")
    except (ConnectionError, TimeoutError, OSError):
        pytest.skip("API unavailable")
    except Exception as e:
        if any(code in str(e) for code in ("401", "404", "429")):
            pytest.skip("API credentials unavailable")
        raise


def test_parse_response_preserves_valid_category():
    """parse_response must preserve a valid category from well-formed JSON."""
    from app.main import parse_response

    raw = '{"category": "Street Light", "confidence": 0.85, "reasoning": "Light is out"}'
    result = parse_response(raw)
    assert isinstance(result, dict), "parse_response must return a dict"
    assert result["category"] == "Street Light", (
        f"parse_response should preserve valid category 'Street Light', "
        f"got '{result['category']}'. Make sure you are not always defaulting to 'Other'."
    )


def test_parse_response_handles_invalid_json():
    """parse_response must not crash on invalid JSON."""
    from app.main import parse_response

    fallback = parse_response("This is not JSON at all")
    assert isinstance(fallback, dict), "parse_response must return a dict even for invalid JSON"
    assert "category" in fallback, "Fallback dict must contain 'category'"


def test_parse_response_handles_wrong_category():
    """parse_response must handle unknown categories gracefully."""
    from app.main import parse_response

    result = parse_response('{"category": "Alien Invasion", "confidence": 0.9, "reasoning": "test"}')
    assert result["category"] == "Other", \
        f"Unknown category should be mapped to 'Other', got '{result['category']}'"


# ---------------------------------------------------------------------------
# 4. Routing: tool definitions and routing rules
# ---------------------------------------------------------------------------

def test_tool_definitions_exist():
    """TOOL_DEFINITIONS must be a non-empty list."""
    from app.main import TOOL_DEFINITIONS

    assert isinstance(TOOL_DEFINITIONS, list), \
        "TOOL_DEFINITIONS must be a list"
    assert len(TOOL_DEFINITIONS) > 0, \
        "TOOL_DEFINITIONS is empty - define tools in Step 2"


def test_routing_rules_file_exists():
    """data/routing_rules.json must exist."""
    assert os.path.exists(RULES_PATH), \
        "data/routing_rules.json not found"


def test_routing_rules_has_all_categories():
    """Routing rules must cover all six categories."""
    with open(RULES_PATH) as f:
        rules = json.load(f)

    expected = {"Pothole", "Noise Complaint", "Trash/Litter",
                "Street Light", "Water/Sewer", "Other"}
    assert set(rules.keys()) == expected, \
        f"Routing rules missing categories: {expected - set(rules.keys())}"


def test_router_correct_department():
    """Router must map Pothole to Public Works - Streets."""
    try:
        from app.router import route_request
    except NotImplementedError:
        pytest.skip("route_request not yet implemented")

    classification = {
        "category": "Pothole",
        "confidence": 0.95,
        "reasoning": "Road surface damage reported",
    }
    try:
        routing = route_request(classification)
        assert routing["department"] == "Public Works - Streets", \
            f"Pothole should route to 'Public Works - Streets', got '{routing['department']}'"
    except NotImplementedError:
        pytest.skip("route_request not yet implemented")


def test_schema_validates_basic():
    """validate_against_schema must accept valid data and reject invalid data."""
    try:
        from app.schemas import validate_against_schema, CLASSIFICATION_SCHEMA
    except ImportError:
        pytest.fail("Cannot import validate_against_schema from app.schemas")

    if not CLASSIFICATION_SCHEMA:
        pytest.fail("CLASSIFICATION_SCHEMA is empty - define it in Step 2")

    try:
        # Valid data should pass
        valid = validate_against_schema(
            {"category": "Pothole", "confidence": 0.9, "reasoning": "Road damage"},
            CLASSIFICATION_SCHEMA,
        )
        assert valid["valid"] is True, \
            f"Valid data should pass, got errors: {valid['errors']}"

        # Missing required fields should fail
        invalid = validate_against_schema({"category": "Pothole"}, CLASSIFICATION_SCHEMA)
        assert invalid["valid"] is False, \
            "Data missing required fields should fail validation"
    except NotImplementedError:
        pytest.fail("validate_against_schema not yet implemented - complete Step 2")


def test_retry_returns_on_valid():
    """retry_with_correction must return on first try when output is valid."""
    try:
        from app.utils import retry_with_correction
    except ImportError:
        pytest.fail("Cannot import retry_with_correction from app.utils")

    def call_fn(correction=None):
        return {"category": "Pothole", "confidence": 0.9, "reasoning": "test"}

    def validation_fn(response):
        return {"valid": True, "errors": []}

    try:
        result = retry_with_correction(call_fn, validation_fn, max_retries=3)
        assert result["valid"] is True, "Valid output should return valid=True"
        assert result["attempts"] == 1, \
            f"Valid-on-first-try should take 1 attempt, got {result['attempts']}"
    except NotImplementedError:
        pytest.fail("retry_with_correction not yet implemented - complete Step 3")


# ---------------------------------------------------------------------------
# 5. Evaluation: metrics and data
# ---------------------------------------------------------------------------

def test_eval_set_loads():
    """eval_set.json must load and contain 30 balanced cases."""
    assert os.path.exists(EVAL_SET_PATH), "data/eval_set.json not found"
    with open(EVAL_SET_PATH) as f:
        cases = json.load(f)

    assert len(cases) == 30, f"Expected 30 cases, got {len(cases)}"

    from collections import Counter
    cats = Counter(c["expected_category"] for c in cases)
    expected_cats = {"Pothole", "Noise Complaint", "Trash/Litter",
                     "Street Light", "Water/Sewer", "Other"}
    assert set(cats.keys()) == expected_cats, f"Unexpected categories: {set(cats.keys())}"
    for cat, count in cats.items():
        assert count == 5, f"Category '{cat}' has {count} cases, expected 5"


def test_accuracy_correct_values():
    """accuracy() must return correct value for known inputs."""
    from app.metrics import accuracy

    results = [
        {"correct": True},
        {"correct": False},
        {"correct": True},
    ]
    acc = accuracy(results)
    assert isinstance(acc, float), "accuracy() must return a float"
    assert abs(acc - 2 / 3) < 0.001, f"Expected ~0.667, got {acc}"


def test_accuracy_empty_list():
    """accuracy() must return 0.0 for an empty list."""
    from app.metrics import accuracy

    assert accuracy([]) == 0.0


def test_precision_correct_values():
    """precision_per_category() must return correct values for known inputs."""
    from app.metrics import precision_per_category

    results = [
        {"expected": "Pothole", "predicted": "Pothole"},
        {"expected": "Noise Complaint", "predicted": "Pothole"},
        {"expected": "Pothole", "predicted": "Pothole"},
        {"expected": "Trash/Litter", "predicted": "Trash/Litter"},
    ]
    prec = precision_per_category(results)
    assert isinstance(prec, dict), "precision_per_category() must return a dict"
    assert abs(prec["Pothole"] - 2 / 3) < 0.001, \
        f"Expected Pothole precision ~0.667, got {prec['Pothole']}"


def test_cost_calculation():
    """calculate_cost() must return correct value for known token counts."""
    from app.cost_tracker import calculate_cost

    # Expected: 1000/1000 * 0.0025 + 500/1000 * 0.01 = 0.0025 + 0.005 = 0.0075
    cost = calculate_cost(1000, 500, model="gpt-4o")
    assert isinstance(cost, float), "calculate_cost() must return a float"
    assert abs(cost - 0.0075) < 0.0001, f"Expected $0.0075, got ${cost}"


def test_cost_calculation_with_pricing():
    """calculate_cost() must use explicit pricing data correctly."""
    from app.cost_tracker import calculate_cost

    # Expected: 2000/1000 * 0.01 + 1000/1000 * 0.02 = 0.02 + 0.02 = 0.04
    test_pricing = {
        "test-model": {
            "input_per_1k_tokens": 0.01,
            "output_per_1k_tokens": 0.02,
        }
    }
    cost = calculate_cost(2000, 1000, model="test-model", pricing=test_pricing)
    assert abs(cost - 0.04) < 0.0001, f"Expected $0.04, got ${cost}"


def test_pricing_loads():
    """pricing.json must load with gpt-4o and gpt-4o-mini models."""
    assert os.path.exists(PRICING_PATH), "data/pricing.json not found"
    with open(PRICING_PATH) as f:
        pricing = json.load(f)

    assert "gpt-4o" in pricing, "pricing.json missing 'gpt-4o'"
    assert "gpt-4o-mini" in pricing, "pricing.json missing 'gpt-4o-mini'"


# ---------------------------------------------------------------------------
# 6. Input validation from utils
# ---------------------------------------------------------------------------

def test_validate_input_from_utils():
    """validate_input should be importable from utils and reject empty strings."""
    from app.utils import validate_input

    # Empty input should raise ValueError
    with pytest.raises(ValueError):
        validate_input("")

    # Whitespace-only input should raise ValueError
    with pytest.raises(ValueError):
        validate_input("   ")

    # Valid input should be returned stripped and truncated to 1000 chars
    assert validate_input("  hello  ") == "hello"
    assert len(validate_input("x" * 2000)) == 1000


# ---------------------------------------------------------------------------
# 7. No hardcoded keys
# ---------------------------------------------------------------------------

def test_no_hardcoded_keys():
    """Source files must not contain hardcoded API keys."""
    app_dir = os.path.join(PROJECT_ROOT, "app")
    for filename in os.listdir(app_dir):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(app_dir, filename)
        with open(filepath) as f:
            content = f.read()
        assert "sk-" not in content, f"Possible hardcoded key in {filename}"
        assert "AZURE_OPENAI_API_KEY =" not in content.replace(" ", "").replace('"', ""), \
            f"Possible hardcoded key assignment in {filename}"
