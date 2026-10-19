def token_usage(response):

    #Get token ussage metadata from response
    
    usage=response.usage_metadata
    input_tokens = usage.prompt_token_count or 0
    thinking_tokens = usage.thoughts_token_count or 0
    output_tokens = usage.candidates_token_count or 0
    total_tokens = usage.total_token_count or 0

    return (usage,input_tokens,thinking_tokens,output_tokens,total_tokens)

def calculate_cost(response,input_rate_per_million,output_rate_per_million,):

  usage,input_tokens,thinking_tokens,output_tokens,total_tokens=token_usage(response)
  
  if not usage:
    return 0.0

  # Thinking tokens are billed at the output rate
  total_billable_output = output_tokens + thinking_tokens

  # Calculate costs (rates are typically per 1 million tokens)
  input_cost = (input_tokens / 1_000_000) * input_rate_per_million
  output_cost = (total_billable_output / 1_000_000) * output_rate_per_million

  total_cost = input_cost + output_cost
  return total_cost