## Communication Protocol
Return a valid JSON object containing the fields below **without any extra text**:
- **thoughts**: An array of succinct, natural language reasoning steps.
- **tool_name**: The exact name of the tool to be used.
- **tool_args**: An object of key–value pairs that specify tool arguments.

### Example:
~~~json
{
    "thoughts": [
        "Reviewing task details.",
        "Outlining a solution plan.",
        "Selecting an appropriate tool."
    ],
    "tool_name": "example_tool",
    "tool_args": {
        "arg1": "value1",
        "arg2": "value2"
    }
}
~~~