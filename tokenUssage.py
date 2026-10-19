from google import genai
import os
from dotenv import load_dotenv

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

MODEL = "gemini-2.5-flash"

# Gemini 2.5 Flash Standard pricing
# Check Google's current pricing before using this in production.
INPUT_PRICE_PER_1M = 0.30
OUTPUT_PRICE_PER_1M = 2.50


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)


# ============================================================
# USER INPUT
# ============================================================

prompt = "What was my previous question?"


# ============================================================
# COUNT INPUT TOKENS BEFORE REQUEST
# ============================================================

token_count = client.models.count_tokens(
    model=MODEL,
    contents=prompt
)

estimated_input_tokens = token_count.total_tokens


# ============================================================
# GENERATE RESPONSE
# ============================================================

response = client.models.generate_content(
    model=MODEL,
    contents=prompt
)


# ============================================================
# GET ACTUAL USAGE
# ============================================================

usage = response.usage_metadata

input_tokens = usage.prompt_token_count or 0
thinking_tokens = usage.thoughts_token_count or 0
output_tokens = usage.candidates_token_count or 0
total_tokens = usage.total_token_count or 0


# ============================================================
# CALCULATE BILLABLE OUTPUT
# ============================================================

# For Gemini 2.5 Flash, thinking tokens are included
# in the output-token pricing.

billable_output_tokens = thinking_tokens + output_tokens


# ============================================================
# CALCULATE COST
# ============================================================

input_cost = (
    input_tokens / 1_000_000
) * INPUT_PRICE_PER_1M

output_cost = (
    billable_output_tokens / 1_000_000
) * OUTPUT_PRICE_PER_1M

total_cost = input_cost + output_cost


# ============================================================
# PRINT RESPONSE
# ============================================================

print("\n" + "=" * 60)
print("GEMINI RESPONSE")
print("=" * 60)

print(response.text)


# ============================================================
# PRINT TOKEN USAGE
# ============================================================

print("\n" + "=" * 60)
print("TOKEN USAGE")
print("=" * 60)

print(f"Model                    : {MODEL}")

print(f"\nInput tokens             : {input_tokens}")
print(f"Thinking tokens          : {thinking_tokens}")
print(f"Output tokens            : {output_tokens}")

print(f"\nBillable output tokens   : {billable_output_tokens}")

print(f"Total tokens             : {total_tokens}")


# ============================================================
# PRINT TOKEN COUNT COMPARISON
# ============================================================

print("\n" + "=" * 60)
print("TOKEN COUNT CHECK")
print("=" * 60)

print(f"Counted before request   : {estimated_input_tokens}")
print(f"Actual input tokens      : {input_tokens}")


# ============================================================
# PRINT COST
# ============================================================

print("\n" + "=" * 60)
print("ESTIMATED API COST")
print("=" * 60)

print(f"Input price / 1M tokens : ${INPUT_PRICE_PER_1M}")
print(f"Output price / 1M tokens: ${OUTPUT_PRICE_PER_1M}")

print(f"\nInput cost               : ${input_cost:.8f}")
print(f"Output cost              : ${output_cost:.8f}")

print(f"\nTOTAL COST               : ${total_cost:.8f}")

print("=" * 60)



def calculate_cost(
    response,
    input_rate_per_million,
    output_rate_per_million,
):
    usage = token_usage(response)

    if usage is None:
        return 0.0

    input_tokens, thinking_tokens, output_tokens, total_tokens = usage

    # Thinking tokens are billed as output tokens
    billable_output_tokens = output_tokens + thinking_tokens

    input_cost = (
        input_tokens / 1_000_000
    ) * input_rate_per_million

    output_cost = (
        billable_output_tokens / 1_000_000
    ) * output_rate_per_million

    total_cost = input_cost + output_cost

    return total_cost