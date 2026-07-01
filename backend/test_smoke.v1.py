"""
Purpose: Smoke test script for validating the backend module end-to-end.
"""
import logging
from backend.investigator import run_investigation

if __name__ == "__main__":
    # Enable info logs so we can see the workflow steps
    logging.basicConfig(level=logging.INFO)
    
    # 1. Mock Transaction data mapping
    mock_txn = {
        "transaction_id": "TXN-10001", 
        "customer_id": "CUST-1001", 
        "customer_name": "John Smith",
        "account_age_years": 8, 
        "merchant": "Apple Store", 
        "merchant_category": "Electronics",
        "amount": 3250.00, 
        "currency": "USD", 
        "transaction_time": "2026-06-30T02:14:00",
        "location": "Miami, FL", 
        "home_location": "Arlington, VA", 
        "device": "New iPhone 16",
        "known_device": False, 
        "travel_notice": False
    }
    
    # 2. Mock Customer History profile data
    mock_history = {
        "average_transaction": 95.00, 
        "highest_transaction": 820.00,
        "transactions_last_30_days": 43, 
        "previous_fraud_cases": 0,
        "preferred_locations": ["Virginia", "Maryland"]
    }
    
    # 3. Mock Policy Context text block matching RAG outputs
    mock_policy = "Transactions above $2000 originating from an unknown device require step-up authentication."

    # 4. FIX: Provide 'customer_profile' explicitly if your INVESTIGATION_PROMPT_V1 demands it.
    # If your prompt template uses a combined map, we can map it to history or a placeholder string.
    # Let's map it into the arguments safely:
    try:
        # We invoke the function using the contract interface keywords
        output_result = run_investigation(
            transaction=mock_txn, 
            customer_history=mock_history, 
            policy_context=mock_policy
        )
        print("\n=== SMOKE TEST OUTPUT RESULT ===")
        print(output_result)
    except Exception as e:
        print(f"Test orchestration error: {e}")
