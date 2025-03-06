### Response Tool
Use this tool to provide the final answer to the user and conclude the task.

- Place the final result in the `"text"` argument.
- Always include full, explicit file paths if applicable.

**Usage Example:**
~~~json
{
    "thoughts": ["Task completed; generating final answer."],
    "tool_name": "response",
    "tool_args": {
        "text": "Final answer with complete file paths."
    }
}
~~~