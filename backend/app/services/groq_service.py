import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM_INSTRUCTIONS = """
You are DisasterGuard AI, an educational disaster-analysis
assistant for an academic software engineering project.

Analyze the supplied simulated disaster information.

Provide:
1. Situation summary
2. Potential hazards
3. General safety precautions
4. Explanation of the supplied evacuation route, if provided

Do not invent real-time disaster conditions, evacuation routes,
shelter availability, or official emergency instructions.

Do not override the existing routing engine's decisions.

Clearly state that the analysis is for an academic simulation
and is not verified emergency guidance.
"""


def analyze_disaster(disaster_details: str, route_details: str = ""):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from .env")

    client = Groq(api_key=api_key)

    prompt = f"""
Simulated disaster information:
{disaster_details}

Existing routing engine result:
{route_details if route_details else "Not provided"}

Generate a concise and understandable disaster analysis.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content
