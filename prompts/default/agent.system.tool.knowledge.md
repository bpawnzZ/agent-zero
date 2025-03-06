### Knowledge Tool
Delivers direct answers by combining online research with stored memories.
- Use the `"question"` argument to ask a precise question.
- Request the result directly—avoid asking for a lengthy explanation.
- Validate memory–based information with current online data.

**Example:**
~~~json
{
    "thoughts": ["Requesting best practices in data encryption."],
    "tool_name": "knowledge_tool",
    "tool_args": {
        "question": "What are the current best practices for data encryption in cloud environments?"
    }
}
~~~