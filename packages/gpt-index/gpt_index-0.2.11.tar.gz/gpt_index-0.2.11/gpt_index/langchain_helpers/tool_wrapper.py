"""Langchain tool wrapper."""

from dataclasses import dataclass
from typing import Callable, Optional


def gpt_index_tool_fn(tool_input: str) -> str:
    """Tool function for GPT Index."""

    # return GPTIndex(index).get_prompt_response(prompt)
    name_to_tool_map = {
        "name": "tool",
    }

# @dataclass
# class Tool:
#     """Interface for tools."""

#     name: str
#     func: Callable[[str], str]
#     description: Optional[str] = None
#     return_direct: bool = False