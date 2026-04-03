from __future__ import annotations

import json
from pathlib import Path

from config import settings

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - runtime fallback
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:  # pragma: no cover - runtime fallback
    Anthropic = None


def load_prompt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _build_mock_response(agent_name: str, input_payload: dict) -> dict:
    system_name = input_payload.get("system_name", agent_name)
    file_names = [item.get("name", "unknown") for item in input_payload.get("files", [])]

    if agent_name in {"reverse_legacy", "reverse_target"}:
        is_legacy = agent_name == "reverse_legacy"
        country_rules = [
            {"country": "Germany", "rule": "Insurance tax surcharge applied to selected policy types."},
            {"country": "France", "rule": "Regional levy calculated for health-linked riders."},
            {"country": "Italy", "rule": "Stamp-duty adjustment included for qualifying policies."},
        ]
        if not is_legacy:
            country_rules = [{"country": "Global", "rule": "No explicit EU country-specific tax logic identified."}]

        business_rules = [
            {
                "id": "BR-AGE-RISK",
                "rule_name": "Age Risk Loading",
                "category": "risk",
                "description": "Age-based risk loading adjusts premium tiers.",
                "trigger": "Quote rating",
                "condition": "Customer age crosses configured thresholds.",
                "outcome": "Premium multiplier increases.",
                "priority": "high",
                "source_reference": file_names,
                "confidence": 0.84,
            },
            {
                "id": "BR-POLICY-ADJ",
                "rule_name": "Policy Type Adjustment",
                "category": "pricing",
                "description": "Policy type adjustments alter discounts and endorsements.",
                "trigger": "Policy type selected",
                "condition": "Specific product or segment combinations apply.",
                "outcome": "Price and quote structure are adjusted.",
                "priority": "medium",
                "source_reference": file_names,
                "confidence": 0.8,
            },
        ]
        if is_legacy:
            business_rules.append(
                {
                    "id": "BR-GDPR",
                    "rule_name": "GDPR Consent Enforcement",
                    "category": "compliance",
                    "description": "GDPR consent required before data persistence for EU customers.",
                    "trigger": "Quote save or processing for EU customer",
                    "condition": "Consent flag is absent or not granted.",
                    "outcome": "Processing is blocked and audit event may be raised.",
                    "priority": "critical",
                    "source_reference": file_names,
                    "confidence": 0.93,
                }
            )

        return {
            "system_name": system_name,
            "summary": f"Mock reverse-engineered spec for {system_name}.",
            "fields": [
                {
                    "name": "customer_id",
                    "canonical_name": "customer_id",
                    "type": "string",
                    "required": True,
                    "source_entity": "quote",
                    "source_layer": "ui_and_db",
                    "business_meaning": "Unique customer identifier used to rate and persist the quote.",
                    "ui_metadata": {
                        "screen_name": "Quote Form",
                        "number_of_fields": 8 if is_legacy else 9,
                        "control_type": "text",
                        "html_tag": "input",
                        "component_tag": "textbox",
                        "section": "customer",
                        "visible": True,
                        "editable": True,
                        "placeholder": "",
                    },
                    "db_metadata": {
                        "table_name": "quotes",
                        "column_name": "customer_id",
                        "column_type": "TEXT",
                        "nullable": False,
                        "primary_key": False,
                        "foreign_key": False,
                        "default_value": None,
                        "indexed": False,
                        "derived_or_computed": False,
                    },
                    "source_reference": file_names,
                },
                {
                    "name": "policy_type",
                    "canonical_name": "policy_type",
                    "type": "string",
                    "required": True,
                    "source_entity": "quote",
                    "source_layer": "ui_and_db",
                    "business_meaning": "Selected insurance product driving rating and eligibility.",
                    "ui_metadata": {
                        "screen_name": "Quote Form",
                        "number_of_fields": 8 if is_legacy else 9,
                        "control_type": "dropdown",
                        "html_tag": "select",
                        "component_tag": "dropdown",
                        "section": "product",
                        "visible": True,
                        "editable": True,
                        "placeholder": "",
                    },
                    "db_metadata": {
                        "table_name": "quotes",
                        "column_name": "policy_type",
                        "column_type": "TEXT",
                        "nullable": False,
                        "primary_key": False,
                        "foreign_key": False,
                        "default_value": None,
                        "indexed": False,
                        "derived_or_computed": False,
                    },
                    "source_reference": file_names,
                },
                {
                    "name": "country_code",
                    "canonical_name": "country_code",
                    "type": "string",
                    "required": True,
                    "source_entity": "quote",
                    "source_layer": "ui_and_db",
                    "business_meaning": "Country used for eligibility and localization of pricing logic.",
                    "ui_metadata": {
                        "screen_name": "Quote Form",
                        "number_of_fields": 8 if is_legacy else 9,
                        "control_type": "dropdown",
                        "html_tag": "select",
                        "component_tag": "dropdown",
                        "section": "policy",
                        "visible": True,
                        "editable": True,
                        "placeholder": "",
                    },
                    "db_metadata": {
                        "table_name": "quotes",
                        "column_name": "country_code",
                        "column_type": "TEXT",
                        "nullable": False,
                        "primary_key": False,
                        "foreign_key": False,
                        "default_value": None,
                        "indexed": False,
                        "derived_or_computed": False,
                    },
                    "source_reference": file_names,
                },
                {
                    "name": "gdpr_consent",
                    "canonical_name": "privacy_consent_flag",
                    "type": "boolean",
                    "required": is_legacy,
                    "source_entity": "quote",
                    "source_layer": "ui_and_process",
                    "business_meaning": "Indicates whether the customer has granted privacy consent for processing.",
                    "ui_metadata": {
                        "screen_name": "Quote Form",
                        "number_of_fields": 8 if is_legacy else 9,
                        "control_type": "checkbox",
                        "html_tag": "input",
                        "component_tag": "checkbox",
                        "section": "compliance",
                        "visible": is_legacy,
                        "editable": is_legacy,
                        "placeholder": "",
                    },
                    "db_metadata": {
                        "table_name": "quote_context" if is_legacy else "quotes",
                        "column_name": "consent_granted" if is_legacy else "consent_marketing",
                        "column_type": "BOOLEAN",
                        "nullable": not is_legacy,
                        "primary_key": False,
                        "foreign_key": False,
                        "default_value": False,
                        "indexed": False,
                        "derived_or_computed": False,
                    },
                    "source_reference": file_names,
                },
            ],
            "business_rules": business_rules,
            "country_specific_rules": [
                {
                    "country": item["country"],
                    "rule_name": "Country Tax Handling",
                    "rule_type": "tax" if is_legacy else "coverage_gap",
                    "description": item["rule"],
                    "impacted_products": ["health", "travel", "family"],
                    "source_reference": file_names,
                    "confidence": 0.9 if is_legacy else 0.7,
                }
                for item in country_rules
            ],
            "validations": [
                {
                    "validation_name": "Minimum Customer Age",
                    "field_or_entity": "birth_date",
                    "validation_type": "eligibility",
                    "rule": "Customer must be at least 18 years old.",
                    "error_behavior": "Quote processing is blocked with validation error.",
                    "source_reference": file_names,
                },
                {
                    "validation_name": "Supported Country",
                    "field_or_entity": "country_code",
                    "validation_type": "market_eligibility",
                    "rule": "Country must be supported for selected product line.",
                    "error_behavior": "Unsupported market selection is rejected.",
                    "source_reference": file_names,
                },
            ],
            "calculations": [
                {
                    "calculation_name": "Base Premium",
                    "category": "pricing",
                    "formula_or_logic": "base_rate * coverage_amount",
                    "inputs": ["base_rate", "coverage_amount"],
                    "outputs": ["premium_base"],
                    "source_reference": file_names,
                },
                {
                    "calculation_name": "Risk Loaded Premium",
                    "category": "rating",
                    "formula_or_logic": "premium_base * age_risk_factor",
                    "inputs": ["premium_base", "age_risk_factor"],
                    "outputs": ["risk_loaded_premium"],
                    "source_reference": file_names,
                },
            ],
            "confidence": {
                "overall": 0.88 if is_legacy else 0.81,
                "evidence_quality": "mock_demo",
                "inferred_items": ["workflow stages", "canonical entity names"],
                "assumptions": ["Generated from local mock mode because no OpenAI API key was found."],
            },
            "source_files": file_names,
            "notes": [
                "Generated from local mock mode because no OpenAI API key was found.",
                "UI metadata includes sample field counts and generic tag mappings for demo purposes.",
            ],
        }

    if agent_name == "collate":
        reverse_spec = input_payload.get("reverse_spec", {})
        system_name = input_payload.get("system_name", "Insurance System")
        return {
            **reverse_spec,
            "system_name": system_name,
            "summary": f"Consolidated business transaction specification for {system_name}.",
            "transaction_flow": [
                {
                    "stage": "input_capture",
                    "description": "UI captures customer, policy, country, and pricing inputs.",
                    "source_reference": reverse_spec.get("source_files", []),
                },
                {
                    "stage": "validation_and_eligibility",
                    "description": "System applies eligibility and validation controls before pricing.",
                    "source_reference": reverse_spec.get("source_files", []),
                },
                {
                    "stage": "pricing_and_risk",
                    "description": "Risk, discount, and premium calculations are performed in orchestration order.",
                    "source_reference": reverse_spec.get("source_files", []),
                },
                {
                    "stage": "persistence_and_audit",
                    "description": "Final quote data is persisted and audit records may be emitted.",
                    "source_reference": reverse_spec.get("source_files", []),
                },
            ],
            "entities": [
                {"entity_name": "Quote", "entity_type": "transactional", "description": "Primary insurance quotation record."},
                {"entity_name": "Customer", "entity_type": "master", "description": "Customer or insured party context."},
            ],
            "integrations": [
                {"integration_name": "UI to pricing flow", "integration_type": "internal", "description": "User input feeds downstream pricing and validation logic."}
            ],
            "persistence_model": [
                {"store_name": "Quote persistence", "store_type": "table_context", "description": "Stores quote values, derived pricing outputs, and consent indicators."}
            ],
            "audit_controls": [
                {"control_name": "Quote audit trail", "description": "Operational events can be logged during quote processing and exception handling."}
            ],
            "exception_paths": [
                {"exception_name": "Validation failure", "description": "Processing stops when eligibility or compliance conditions are not met."}
            ],
            "confidence": {"collation_confidence": 0.84, "synthesis_quality": "mock_demo", "notes": ["Mock collation output."]},
        }

    return {
        "missing_features": [
            "Germany, France, and Italy policy tax handling is absent in target inputs.",
            "GDPR consent enforcement is not present in the target system.",
        ],
        "incorrect_implementations": [
            "Target validation model does not appear to block policy persistence when privacy consent is missing."
        ],
        "compliance_gaps": [
            "EU privacy consent workflow is missing.",
            "Country-specific insurance taxation controls are incomplete.",
        ],
        "risks": [
            {
                "risk_name": "GDPR non-compliance",
                "category": "regulatory",
                "severity": "High",
                "description": "Missing EU consent enforcement may allow unauthorized processing.",
                "impacted_area": "quote processing",
                "likely_outcome": "Potential fines and compliance breaches.",
                "mitigation_hint": "Implement consent validation and auditable enforcement.",
            },
            {
                "risk_name": "Regional pricing mismatch",
                "category": "financial",
                "severity": "High",
                "description": "Country-specific tax logic is absent from the target flow.",
                "impacted_area": "premium calculation",
                "likely_outcome": "Incorrect premiums and reconciliation issues.",
                "mitigation_hint": "Introduce tax reference data and targeted pricing tests.",
            },
        ],
        "rule_comparison": [
            {
                "rule_id": "BR-GDPR",
                "rule_name": "GDPR Consent Rule",
                "category": "compliance",
                "legacy_status": "Present",
                "target_status": "Missing",
                "gap_type": "compliance_gap",
                "risk_level": "High",
                "description": "Legacy blocks EU processing without consent while target lacks equivalent enforcement.",
                "evidence": ["sp_validate_gdpr_consent.sybase.sql", "quote.validation.js"],
                "recommended_action": "Add consent validation and persistence checks in the target flow.",
                "confidence": 0.95,
            },
            {
                "rule_id": "BR-EU-TAX",
                "rule_name": "EU Tax Logic",
                "category": "tax",
                "legacy_status": "Present",
                "target_status": "Missing",
                "gap_type": "missing_feature",
                "risk_level": "High",
                "description": "Legacy includes country-specific tax calculation and reference data not found in target.",
                "evidence": ["country_tax_rules.sybase.sql", "sp_lookup_country_tax.sybase.sql"],
                "recommended_action": "Port country-specific tax rules and reference tables.",
                "confidence": 0.9,
            },
            {
                "rule_id": "BR-AGE-RISK",
                "rule_name": "Age Risk Loading",
                "category": "risk",
                "legacy_status": "Present",
                "target_status": "Partial",
                "gap_type": "incorrect_implementation",
                "risk_level": "Medium",
                "description": "Both systems apply age-related risk factors but thresholds and loadings differ.",
                "evidence": ["sp_apply_risk_loading.sybase.sql", "rating.service.js"],
                "recommended_action": "Compare thresholds and factor increments line by line.",
                "confidence": 0.76,
            },
        ],
        "confidence": {
            "gap_confidence": 0.87,
            "coverage_of_analysis": {
                "pricing": "covered",
                "compliance": "covered",
                "country_logic": "covered",
                "auditability": "partial",
            },
            "notes": ["Mock gap analysis generated without live LLM execution."],
        },
    }


def call_llm_json(agent_name: str, prompt: str, input_payload: dict) -> dict:
    formatted_prompt = prompt.format(payload=json.dumps(input_payload, ensure_ascii=False, indent=2))

    if settings.model.startswith("claude"):
        if not settings.anthropic_api_key or Anthropic is None:
            return _build_mock_response(agent_name, input_payload)

        client = Anthropic(api_key=settings.anthropic_api_key)
        response = client.messages.create(
            model=settings.model,
            max_tokens=4000,
            system="Return strict JSON only. Do not use markdown fences.",
            messages=[{"role": "user", "content": formatted_prompt}],
        )
        text_parts = [block.text for block in response.content if getattr(block, "type", "") == "text"]
        return {"raw_text": "\n".join(text_parts)}

    if not settings.openai_api_key or OpenAI is None:
        return _build_mock_response(agent_name, input_payload)

    client = OpenAI(api_key=settings.openai_api_key)
    response = client.responses.create(
        model=settings.model,
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": "Return strict JSON only. Do not use markdown fences."}]},
            {"role": "user", "content": [{"type": "input_text", "text": formatted_prompt}]},
        ],
    )
    return {"raw_text": response.output_text}
