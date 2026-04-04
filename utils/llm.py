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


def _build_mock_reverse_response(system_name: str, artifact_kind: str, file_names: list[str], is_legacy: bool) -> dict:
    is_code = artifact_kind == "code"
    return {
        "system_name": system_name,
        "artifact_kind": artifact_kind,
        "summary": f"Mock {artifact_kind} reverse-engineered spec for {system_name}.",
        "fields": [
            {
                "name": "customer_id" if is_code else "quote_id",
                "canonical_name": "customer_id" if is_code else "quote_id",
                "type": "string" if is_code else ("integer" if is_legacy else "uuid"),
                "required": True,
                "source_entity": "quote_form" if is_code else "quote",
                "source_layer": "ui" if is_code else "db",
                "business_meaning": "Key quote input captured or persisted through the quote flow.",
                "ui_metadata": {
                    "screen_name": "Quote Generation",
                    "number_of_fields": 8,
                    "control_type": "text",
                    "html_tag": "input" if not is_legacy and is_code else "",
                    "component_tag": "TextBox" if is_legacy and is_code else ("input" if is_code else ""),
                    "section": "customer",
                    "visible": bool(is_code),
                    "editable": bool(is_code),
                    "placeholder": "",
                }
                if is_code
                else {},
                "db_metadata": {}
                if is_code
                else {
                    "table_name": "quote_context" if is_legacy else "quotes",
                    "column_name": "quote_id",
                    "column_type": "INT" if is_legacy else "UUID",
                    "nullable": False,
                    "primary_key": True,
                    "foreign_key": False,
                    "default_value": None,
                    "indexed": True,
                    "derived_or_computed": False,
                },
                "source_reference": file_names,
            }
        ],
        "business_rules": [
            {
                "id": "BR-CODE-FLOW" if is_code else "BR-DB-FLOW",
                "rule_name": "Quote orchestration flow" if is_code else "Database pricing and persistence flow",
                "category": "workflow",
                "description": "Artifacts describe how the quote process is orchestrated across layers.",
                "trigger": "Generate Quote action",
                "condition": "Required inputs are supplied to the system.",
                "outcome": "Validation, pricing, and persistence steps execute in order.",
                "priority": "high",
                "source_reference": file_names,
                "confidence": 0.85,
            }
        ],
        "country_specific_rules": []
        if is_code
        else [
            {
                "country": "Spain" if not is_legacy else "Multi-country",
                "rule_name": "Country-aware pricing logic",
                "rule_type": "db_logic",
                "description": "Stored logic applies country-aware tax or adjustment behavior.",
                "impacted_products": ["health", "travel", "family"],
                "source_reference": file_names,
                "confidence": 0.82,
            }
        ],
        "validations": [
            {
                "validation_name": "Required input validation" if is_code else "Procedure-level eligibility validation",
                "field_or_entity": "quote_form" if is_code else "quote_context",
                "validation_type": "ui_validation" if is_code else "stored_procedure_validation",
                "rule": "Artifacts show validation gates before quote completion.",
                "error_behavior": "The flow rejects or stops invalid submissions.",
                "source_reference": file_names,
            }
        ],
        "calculations": [
            {
                "calculation_name": "Pricing handoff" if is_code else "Database pricing calculation",
                "category": "pricing",
                "formula_or_logic": "Artifacts describe the inputs and outputs of pricing logic.",
                "inputs": ["policy_type", "coverage_amount"],
                "outputs": ["final_premium"],
                "source_reference": file_names,
            }
        ],
        "ui_components": [
            {
                "component_name": "Quote Generation Form",
                "component_type": "form",
                "screen_or_route": "Quote Generation",
                "purpose": "Capture quote inputs and submit the quote request.",
                "actions": ["generate_quote"],
                "controls": [
                    {
                        "control_name": "txtCustomerId" if is_legacy else "customerId",
                        "control_type": "textbox" if is_legacy else "text_input",
                        "label": "Customer Id",
                        "bound_field": "customer_id",
                        "data_type": "string",
                        "required": True,
                        "default_value": "",
                        "visible": True,
                        "editable": True,
                        "options": [],
                        "events": ["change"],
                    },
                    {
                        "control_name": "cboPolicyType" if is_legacy else "policyType",
                        "control_type": "combobox" if is_legacy else "select",
                        "label": "Policy Type",
                        "bound_field": "policy_type",
                        "data_type": "string",
                        "required": True,
                        "default_value": "HEALTH",
                        "visible": True,
                        "editable": True,
                        "options": ["HEALTH", "TRAVEL", "FAMILY", "CORPORATE"],
                        "events": ["change"],
                    },
                    {
                        "control_name": "txtCoverage" if is_legacy else "coverageAmount",
                        "control_type": "textbox" if is_legacy else "number_input",
                        "label": "Coverage Amount",
                        "bound_field": "coverage_amount",
                        "data_type": "decimal",
                        "required": True,
                        "default_value": 50000,
                        "visible": True,
                        "editable": True,
                        "options": [],
                        "events": ["change"],
                    },
                ],
                "source_reference": file_names,
            }
        ]
        if is_code
        else [],
        "classes": [
            {
                "class_name": "CommonCountryQuoteProcessor" if is_legacy else "QuoteWorkflowService",
                "class_type": "service",
                "responsibility": "Coordinates validation, pricing, persistence, and audit processing.",
                "dependencies": ["validation_service", "pricing_service", "persistence_service"],
                "source_reference": file_names,
            }
        ]
        if is_code
        else [],
        "methods": [
            {
                "method_name": "OnGenerateQuote" if is_legacy else "generateQuote",
                "owner": "BaseQuoteGenerationForm" if is_legacy else "QuoteApiService",
                "visibility": "private" if is_legacy else "public",
                "returns": "void" if is_legacy else "Observable<QuoteResponse>",
                "parameters": [
                    {"name": "quote_request", "type": "QuoteRequest", "required": True, "description": "Canonical quote request payload."}
                ],
                "calls": ["workflow_service"],
                "source_reference": file_names,
            }
        ]
        if is_code
        else [],
        "procedures": []
        if is_code
        else [
            {
                "procedure_name": "sp_calculate_quote" if is_legacy else "fn_apply_spain_adjustment",
                "procedure_type": "stored_procedure" if is_legacy else "function",
                "parameters": [
                    {
                        "name": "quote_id" if is_legacy else "p_policy_type",
                        "direction": "input",
                        "type": "INT" if is_legacy else "text",
                        "required": True,
                        "default_value": None,
                        "description": "Primary procedure input.",
                    },
                    {
                        "name": "country_code" if is_legacy else "p_premium_amount",
                        "direction": "input",
                        "type": "VARCHAR(2)" if is_legacy else "numeric",
                        "required": True,
                        "default_value": None,
                        "description": "Country or pricing input used in logic branches.",
                    },
                ],
                "returns": ["final_premium"] if is_legacy else ["adjustment_amount"],
                "side_effects": ["pricing update", "table writes"],
                "logic_summary": "Calculates pricing-related outputs and applies procedural orchestration.",
                "source_reference": file_names,
            }
        ],
        "procedure_dependencies": [
            {
                "from": "submit_handler" if is_code else "pricing_orchestration",
                "to": "workflow_service" if is_code else "tax_discount_risk_logic",
                "dependency_type": "method_call" if is_code else "procedure_call",
                "source_reference": file_names,
            }
        ],
        "table_dependencies": []
        if is_code
        else [
            {
                "table_name": "quote_context" if is_legacy else "quotes",
                "role": "transactional persistence",
                "operation": "update" if is_legacy else "insert",
                "columns": ["quote_id", "final_premium", "tax_amount"],
                "dependent_procedures": ["sp_calculate_quote"] if is_legacy else ["quote.repository"],
                "source_reference": file_names,
            }
        ],
        "api_endpoints": []
        if is_legacy or not is_code
        else [
            {
                "method": "POST",
                "path": "/api/v1/quotes/generate",
                "request_fields": ["customer_id", "policy_type", "coverage_amount", "country_code"],
                "response_fields": ["quote_id", "pricing.final_premium"],
                "purpose": "Generate quote",
                "source_reference": file_names,
            }
        ],
        "confidence": {
            "overall": 0.84,
            "evidence_quality": "mock_demo",
            "inferred_items": ["dependency chain", "canonical field intent"],
            "assumptions": ["Generated from local mock mode because no live LLM call was available."],
        },
        "source_files": file_names,
        "notes": [f"Mock {artifact_kind} reverse output with {'code' if is_code else 'SQL'}-specific emphasis."],
    }


def _build_mock_collate_response(system_name: str, code_reverse_spec: dict, sql_reverse_spec: dict) -> dict:
    source_files = list(dict.fromkeys(code_reverse_spec.get("source_files", []) + sql_reverse_spec.get("source_files", [])))
    return {
        "system_name": system_name,
        "summary": f"Consolidated business transaction specification for {system_name} built from separate code and SQL reverse engineering passes.",
        "fields": code_reverse_spec.get("fields", []) + sql_reverse_spec.get("fields", []),
        "business_rules": code_reverse_spec.get("business_rules", []) + sql_reverse_spec.get("business_rules", []),
        "country_specific_rules": sql_reverse_spec.get("country_specific_rules", []),
        "validations": code_reverse_spec.get("validations", []) + sql_reverse_spec.get("validations", []),
        "calculations": code_reverse_spec.get("calculations", []) + sql_reverse_spec.get("calculations", []),
        "confidence": {"collation_confidence": 0.86, "synthesis_quality": "mock_demo", "notes": ["Mock collation output."]},
        "source_files": source_files,
        "notes": code_reverse_spec.get("notes", []) + sql_reverse_spec.get("notes", []),
        "transaction_flow": [
            {"stage": "code_reverse_engineering", "description": "Application source was reverse engineered first.", "source_reference": code_reverse_spec.get("source_files", [])},
            {"stage": "sql_reverse_engineering", "description": "Database source was reverse engineered separately.", "source_reference": sql_reverse_spec.get("source_files", [])},
            {"stage": "canonical_collation", "description": "Both reverse outputs were merged into a unified business flow.", "source_reference": source_files},
        ],
        "entities": [
            {"entity_name": "Quote", "entity_type": "transactional", "description": "Primary insurance quotation record."},
            {"entity_name": "Customer", "entity_type": "master", "description": "Customer profile used during validation and pricing."},
        ],
        "integrations": code_reverse_spec.get("api_endpoints", []),
        "persistence_model": sql_reverse_spec.get("table_dependencies", []),
        "audit_controls": [{"control_name": "Quote audit trail", "description": "Events are recorded during quote generation and compliance handling."}],
        "exception_paths": [{"exception_name": "Validation failure", "description": "Processing stops when validation or compliance checks fail."}],
        "flow_map": {
            "nodes": [
                {"id": "code_reverse", "label": "Code Reverse", "type": "analysis"},
                {"id": "sql_reverse", "label": "SQL Reverse", "type": "analysis"},
                {"id": "collate", "label": "Canonical Collate", "type": "synthesis"},
                {"id": "validate", "label": "Validation", "type": "process"},
                {"id": "price", "label": "Pricing", "type": "process"},
                {"id": "persist", "label": "Persistence", "type": "process"},
            ],
            "edges": [
                {"from": "code_reverse", "to": "collate", "label": "ui/classes/apis"},
                {"from": "sql_reverse", "to": "collate", "label": "sp/tables/logic"},
                {"from": "collate", "to": "validate", "label": "canonical model"},
                {"from": "validate", "to": "price", "label": "approved"},
                {"from": "price", "to": "persist", "label": "final premium"},
            ],
            "diagram_text": "Code Reverse -> Canonical Collate <- SQL Reverse -> Validation -> Pricing -> Persistence",
        },
        "source_breakdown": {
            "code_source_files": code_reverse_spec.get("source_files", []),
            "sql_source_files": sql_reverse_spec.get("source_files", []),
        },
    }


def _build_mock_response(agent_name: str, input_payload: dict) -> dict:
    system_name = input_payload.get("system_name", agent_name)
    file_names = [item.get("name", "unknown") for item in input_payload.get("files", [])]
    artifact_kind = input_payload.get("artifact_kind", "")

    if agent_name in {"reverse_legacy", "reverse_target"}:
        return _build_mock_reverse_response(system_name, artifact_kind, file_names, is_legacy=agent_name == "reverse_legacy")

    if agent_name == "collate":
        return _build_mock_collate_response(
            input_payload.get("system_name", "Insurance System"),
            input_payload.get("code_reverse_spec", {}),
            input_payload.get("sql_reverse_spec", {}),
        )

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


def call_llm_json(agent_name: str, prompt: str, input_payload: dict, require_live_call: bool = False) -> dict:
    formatted_prompt = prompt.format(payload=json.dumps(input_payload, ensure_ascii=False, indent=2))

    if settings.model.startswith("claude"):
        if not settings.anthropic_api_key or Anthropic is None:
            if require_live_call:
                raise RuntimeError(
                    "Caching is disabled, so a live Anthropic call is required. "
                    "Set ANTHROPIC_API_KEY and ensure the anthropic package is installed."
                )
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
        if require_live_call:
            raise RuntimeError(
                "Caching is disabled, so a live OpenAI call is required. "
                "Set OPENAI_API_KEY and ensure the openai package is installed."
            )
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
