"""
Department Router for Activity 3 - 311 Triage Engine

Routes classified Memphis 311 requests to the correct city department
based on category and routing rules.
"""

import json
import os


def load_routing_rules(path: str | None = None) -> dict:
    """Load department routing rules from JSON file.

    Args:
        path: Path to routing_rules.json. Defaults to data/routing_rules.json
              relative to the project root.

    Returns:
        dict mapping category names to routing info (department, sla_hours, priority).
    """
    # TODO: Step 2.1 - Implement this function
    #   1. Default path to ../data/routing_rules.json relative to this file
    #   2. Open and parse the JSON file
    #   3. Return the parsed dict
    #   4. Handle FileNotFoundError gracefully (return empty dict)
    raise NotImplementedError("Implement load_routing_rules in Step 2")


def route_request(classification: dict, rules: dict | None = None) -> dict:
    """Route a classified request to the correct Memphis department.

    Takes a classification dict (from the model) and looks up the routing
    info from the rules. Merges classification + routing into a single dict.

    Args:
        classification: dict with keys: category, confidence, reasoning
        rules: Optional routing rules dict. If None, loads from file.

    Returns:
        dict with keys: category, confidence, reasoning, department,
        sla_hours, priority. Falls back to General Services if category
        not found in rules.
    """
    # TODO: Step 2.2 - Implement routing logic
    #
    # 1. If rules is None, call load_routing_rules()
    # 2. Look up classification["category"] in the rules dict
    # 3. If found, merge the routing info into the classification dict:
    #    - department: from rules
    #    - sla_hours: from rules
    #    - priority: from rules
    # 4. If NOT found, use the "Other" fallback:
    #    - department: "General Services"
    #    - sla_hours: 120
    #    - priority: "low"
    # 5. Return the merged dict
    raise NotImplementedError("Implement route_request in Step 2")


def escalate_priority(routing: dict, reason: str) -> dict:
    """Escalate a routed request's priority by one level.

    Priority levels (lowest to highest): low -> standard -> high -> critical

    Args:
        routing: A routing dict (output of route_request).
        reason: A string explaining why the priority was escalated.

    Returns:
        Updated routing dict with escalated priority and adjusted SLA.
        Adds an 'escalation_reason' field.
    """
    # TODO: Step 2 (Stretch) - Implement escalation logic
    #
    # Priority escalation ladder:
    #   low -> standard (SLA = SLA * 0.75)
    #   standard -> high (SLA = SLA * 0.5)
    #   high -> critical (SLA = SLA * 0.25)
    #   critical -> critical (no change, already max)
    #
    # 1. Determine the current priority
    # 2. Escalate to the next level
    # 3. Adjust SLA hours accordingly
    # 4. Add "escalation_reason" field
    # 5. Return updated dict
    raise NotImplementedError("Implement escalate_priority (Stretch)")
