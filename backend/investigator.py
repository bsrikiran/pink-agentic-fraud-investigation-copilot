"""
Purpose: Primary core execution workflow module orchestration layer engine for Fraud Investigations.
"""

import logging
from backend.config import validate_config
from backend.llm_client import LLMClient
from backend.utils import validate_llm_json_response
from backend.prompts import SYSTEM_PROMPT_V1, INVESTIGATION_PROMPT_V1, JSON_OUTPUT_PROMPT_V1

logger = logging.getLogger("backend.investigator")

def run_investigation(transaction: dict, customer_history: dict, policy_context: str, policy_citations: list | None = None) -> dict:
    """Executes a fraud investigation workflow returning clean JSON matching the target schema contract."""
    logger.info(f"Starting Investigation workflow sequence for Case ID: {transaction.get('transaction_id', 'N/A')}")
    
    if not validate_config():
        return {"status": "error", "message": "Backend engine is unconfigured. Verify environment paths."}
    
    try:
        # Evaluate standard transactional requirements
        if not transaction or "amount" not in transaction:
            return {"status": "error", "message": "Required transaction fields are missing."}
        if not customer_history:
            return {"status": "error", "message": "Required customer historical background parameters are missing."}
            
        # Interpolation mapping matching prompts file parameters exactly
        user_execution_message = INVESTIGATION_PROMPT_V1.format(
            transaction=transaction,
            customer_history=customer_history,
            customer_profile=customer_history,  # Safeguard duplicate prompt parameters safely
            policy_context=policy_context if policy_context else ""
        )
        
        # Request Generation. The exact output schema (JSON_OUTPUT_PROMPT_V1) must be sent -
        # without it the model free-forms key names off the numbered investigation steps
        # (e.g. "step_9_reasoning") instead of the "policy_reference" contract field.
        llm_agent = LLMClient()
        raw_output = llm_agent.call_chat_completion(
            system_message=SYSTEM_PROMPT_V1 + "\n" + JSON_OUTPUT_PROMPT_V1,
            user_message=user_execution_message
        )
        
        # Sanitize and validate fields structure
        is_valid, final_payload = validate_llm_json_response(raw_output)
        if not is_valid:
            return final_payload

        # Replace the model's own (unverifiable) citation text with the actual retrieved
        # source files. If the model judged no policy relevant, keep the citations empty
        # rather than showing sources it never claimed to use.
        final_payload["policy_reference"] = list(policy_citations) if final_payload["policy_reference"] and policy_citations else []

        logger.info("Investigation analysis completely finalized with clean data schema formatting.")
        return final_payload

    except Exception as general_fault:
        logger.critical(f"Critical execution error intercepted: {str(general_fault)}")
        return {"status": "error", "message": f"Internal structural workflow fault: {str(general_fault)}"}
