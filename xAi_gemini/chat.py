# from google import genai
# from xAi_gemini.token_usage import token_usage, calculate_cost

# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Hello",
# )

# print(response.text)

# print(token_usage(response))

# print(
#     calculate_cost(
#         response=response,
#         input_rate_per_million=100,
#         output_rate_per_million=2500,
#     )
# )

# from google import genai
# from xAi_gemini.token_usage import token_usage, calculate_cost

# client = genai.Client()

# image = client.files.upload(file="docs/image.png")

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents=[
#         image,
#         "Describe this image."
#     ],
# )

# print(response.text)
# print(token_usage(response))
# print(
#     calculate_cost(
#         response=response,
#         input_rate_per_million=100,
#         output_rate_per_million=2500,
#     )
# )