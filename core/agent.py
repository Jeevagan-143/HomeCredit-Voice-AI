

import os
import re
import time

from google import genai
from google.genai import types
from core.prompt import SYSTEM_PROMPT




def get_fallback_response(messages):
    customer_messages = [
        str(m.get("content", "")).strip().lower()
        for m in messages
        if m.get("role") != "assistant"
    ]

    conversation = "\n".join(customer_messages)

    def has(*words):
        return any(word in conversation for word in words)

    # Customer identity confirmation
    if not has(
        "i am the customer",
        "i'm the customer",
        "yes, speaking",
        "yes speaking",
        "this is the customer",
        "yes, i am",
        "yes i am",
    ):
        return (
            "Hello! I'm calling from Home Credit. "
            "May I speak with the intended customer, please?"
        )

    # Qualification checklist
    if not has("residential", "commercial", "industrial"):
        return "What type of property do you own: residential, commercial, or industrial?"

    if not has(
        "solely owned", "sole owner", "jointly owned",
        "joint ownership", "owned by me", "co-owned",
    ):
        return "Is the property solely owned by you, or jointly owned?"

    if not has(
        "original property documents", "original documents",
        "original papers", "photocopies",
    ):
        return "Are the original property documents available?"

    if has("photocopies only", "only photocopies", "no original"):
        return "Original property documents are required. We cannot proceed with photocopies alone."

    if not has("₹", "inr", "loan amount", "lakh", "lakhs"):
        return "What loan amount are you looking for? The maximum offer is ₹75,00,000, subject to assessment."

    if not has("salaried", "self-employed", "self employed", "business owner"):
        return "Are you salaried or self-employed?"

    if not has("bank account", "bank transfer", "credited directly", "salary is credited"):
        return "Is your income credited directly to your bank account?"

    if not has("market value", "property value", "worth", "valued at"):
        return "What is the approximate current market value of your property?"

    if not has("years", "year", "tenure", "loan period"):
        return "What loan tenure would you prefer, between 3 and 15 years?"

    return (
        "Thank you for completing the preliminary screening. "
        "This is not loan approval. A Home Credit specialist must review "
        "your information before any lending decision."
    )
def generate_response(messages):
    # Deterministic screening prevents repeated questions during API outages.
    # The Gemini API can be used after the question-flow is verified.
    return get_fallback_response(messages)