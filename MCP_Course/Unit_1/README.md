# tiny-agents (agent.json) 
In the `agent.json` configuration, we are using the @playwright/mcp MCP server. This is an MCP server that can control a browser with Playwright.

You can run the agent:

```
tiny-agents run agent.json
```

When you run the agent, you’ll see it load, listing the tools it has discovered from its connected MCP servers. Then, it’s ready for your prompts!

Prompt example:

```
do a Web Search for HF inference providers on Brave Search and open the first result and then give me the list of the inference providers supported on Hugging Face
```

# First MCP Server with Gradio (mcp_letter_counter.py)
Running this script, the letter counter function is now accessible through:

- A traditional Gradio web interface for direct human interaction
- An MCP Server that can be connected to compatible clients