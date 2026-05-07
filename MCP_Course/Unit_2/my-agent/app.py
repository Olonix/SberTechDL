import asyncio
from huggingface_hub import Agent

async def main():
    async with Agent(
        model="Qwen/Qwen2.5-72B-Instruct",
        provider="auto",
        servers=[
            {
                "type": "sse",
                "url": "https://olonix-mcp-sentiment.hf.space/gradio_api/mcp/sse",
            }
        ],
    ) as agent:

        await agent.load_tools()

        stream = agent.run("сделай анализ тональности фразы 'i love you'")

        async for chunk in stream:
            try:
                delta = chunk.choices[0].delta
                if delta and getattr(delta, "content", None):
                    print(delta.content, end="", flush=True)
            except Exception:
                pass

asyncio.run(main())