import os
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")

client = Anthropic(api_key=my_api_key)


# response = client.messages.create(
#     model="claude-3-haiku-20240307",
#     max_tokens=1000,
#     messages=[
#         {"role": "user", "content": "What flavors are used in Dr. Pepper?"}
#     ]
# )

# print(response.content[0].text)
