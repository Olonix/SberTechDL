#!/usr/bin/env python3
"""
Module 1: Basic MCP Server - Starter Code
TODO: Implement tools for analyzing git changes and suggesting PR templates
"""

import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory (shared across all modules)
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


# TODO: Implement tool functions here
# Example structure for a tool:
# @mcp.tool()
# async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True) -> str:
#     """Get the full diff and list of changed files in the current git repository.
#     
#     Args:
#         base_branch: Base branch to compare against (default: main)
#         include_diff: Include the full diff content (default: true)
#     """
#     # Your implementation here
#     pass

# Minimal stub implementations so the server runs
# TODO: Replace these with your actual implementations

@mcp.tool()
async def analyze_file_changes(base_branch: str = "main", include_diff: bool = True, max_diff_lines: int = 500) -> str:
    """Get the full diff and list of changed files in the current git repository.
    
    Args:
        base_branch: Base branch to compare against (default: main)
        include_diff: Include the full diff content (default: true)
    """
    working_dir = "."
    
    try:
        context = mcp.get_context()
        roots_result = await context.session.list_roots()
        if roots_result.roots:
            working_dir = str(roots_result.roots[0].uri).replace("file://", "")
    except Exception:
        pass
        
    try:
        result = subprocess.run(["git", "diff", f"{base_branch}...HEAD"],
            capture_output=True, text=True, cwd=working_dir
        )
        
        diff_output = str(result.stdout) if result.stdout else ""
        diff_lines = diff_output.split('\n')
        
        if len(diff_lines) > max_diff_lines:
            truncated_diff = '\n'.join(diff_lines[:max_diff_lines])
            truncated_diff += f"\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ..."
            diff_output = truncated_diff
            
        return json.dumps({
            "diff": diff_output if include_diff else "Use include_diff=true to see diff",
            "files_changed": len(diff_lines)
        })
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "diff": f"Error occurred: {str(e)}", 
            "files_changed": 0
        })


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    templates =[
        {"name": "Feature", "description": "New functionality and features"},
        {"name": "Bugfix", "description": "Bug fixes and error corrections"},
        {"name": "Refactoring", "description": "Code cleanup without logic changes"},
        {"name": "Documentation", "description": "Docs, README, and comments updates"},
        {"name": "Hotfix", "description": "Urgent production patches"},
        {"name": "Performance", "description": "Speed and efficiency improvements"},
        {"name": "Tests", "description": "New or improved test coverage"}
    ]
    return json.dumps(templates)


@mcp.tool()
async def suggest_template(changes_summary: str, change_type: str) -> str:
    """Let Claude analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        change_type: The type of change you've identified (bug, feature, docs, refactor, test, etc.)
    """
    return json.dumps({
        "status": "success",
        "analysis_received": changes_summary,
        "recommended_template": change_type
    })


if __name__ == "__main__":
    mcp.run()