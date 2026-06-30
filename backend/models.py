"""
Purpose: Definition of structured schemas and typed Pydantic models for internal validation.
Ensures rigorous compliance with the Integration Contract JSON specifications.
"""

from typing import List
from pydantic import BaseModel, Field

class TransactionData(BaseModel):
    """Schema model for incoming transaction data details."""
    transaction_id: str = Field(..., description="Unique transaction record identifier")
    customer_id: str = Field(..., description="Unique customer owner account identifier")
    customer_name: str = Field(..., description="Legal full name of client account holder")
    account_age_years: int = Field(..., description="Age of customer bank profile in years")
    merchant: str = Field(..., description="Target counterparty merchant trade entity string")
    merchant_category: str = Field(..., description="Industry categorization descriptor of the vendor")
    amount: float = Field(..., description="The financial value amount requested for transfer")
    currency: str = Field(..., description="ISO Alpha currency identifier")
    transaction_time: str = Field(..., description="ISO 8601 extended format timestamp string")
    location: str = Field(..., description="The originating city/state location of current trade request")
    home_location: str = Field(..., description="Documented physical primary home domain of client")
    device: str = Field(..., description="Hardware device fingerprint label identifier string")
    known_device: bool = Field(..., description="Flag determining historical client device usage status")
    travel_notice: bool = Field(..., description="Flag determining active global travel notice status")

class CustomerHistoryData(BaseModel):
    """Schema model mapping historical customer behavioral activity profiles."""
    average_transaction: float = Field(..., description="Calculated standard historical mean ticket amount")
    highest_transaction: float = Field(..., description="Max financial metric recorded for previous transfers")
    transactions_last_30_days: int = Field(..., description="Frequency metrics tracking recent baseline volumes")
    previous_fraud_cases: int = Field(..., description="Historical counter tracking flagged fraud incidents")
    preferred_locations: List[str] = Field(default_factory=list, description="List of recognized active zones")

class InvestigationResultModel(BaseModel):
    """Strict schema validation structure for the core LLM investigation pipeline output."""
    fraud_score: int = Field(..., ge=0, le=100, description="Calculated numeric fraud risk exposure metric")
    risk_level: str = Field(..., description="Categorical assessment scale: Low, Medium, High")
    confidence: str = Field(..., description="Algorithmic operational assurance matrix: Low, Medium, High")
    recommendation: str = Field(..., description="Final processing path recommendation directive string")
    investigation_summary: str = Field(..., description="Comprehensive textual wrap up summary detailing current case dynamics")
    fraud_indicators: List[str] = Field(default_factory=list, description="Itemized structural flagged behavioral markers patterns")
    reasoning: List[str] = Field(..., description="Itemized structural bulleted argument strings logic")
    policy_reference: List[str] = Field(..., description="Documented compliance rule citation traces matching existing project assets")
