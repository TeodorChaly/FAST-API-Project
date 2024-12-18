import httpx

from ai_regenerator.ai_api_env import API_endpoint
from ai_web.get_env import perplexity


async def perplexity_api(prompt, system_content, model="llama-3.1-sonar-small-128k-online"):
    perplexity_endpoint = "https://api.perplexity.ai/chat/completions"

    payload = {
        "messages": [
            {"content": system_content, "role": "system"},
            {"role": "user", "content": prompt}
        ],
        "model": model
    }

    headers = {
        "Authorization": f"Bearer {perplexity}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(perplexity_endpoint, json=payload, headers=headers, timeout=120)

        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            citations = data['citations']
            return content, citations
        else:
            return None, None


async def openai_api(system_fine_tuning, content):
    try:
        completion = API_endpoint.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": system_fine_tuning},

                {"role": "user", "content": content},
            ]
        )
        return completion.choices[0].message.content

    except Exception as e:
        print(f'Error during generation: {e}')
        return None
