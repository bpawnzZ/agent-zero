### Call Subordinate
- Use this tool to delegate specific subtasks to subordinate agents (e.g., coder, engineer, scientist).
- In the `message` field, clearly describe:
  - The subordinate's role.
  - Task details and goals.
  - Any relevant context.
- **Delegate only specific subtasks**, not the entire task.
- The `reset` flag:
  - `"true"` spawns a new subordinate.
  - `"false"` continues with an existing subordinate.
- **If you are a subordinate:** Your superior is identified as `{{agent_name}}` (one level higher). Execute your assigned tasks and delegate if needed.

**Example:**
~~~json
{
    "thoughts": ["The solution needs refinement. I will ask a coding expert to optimize the algorithm."],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Coder, please optimize the algorithm for efficiency.",
        "reset": "true"
    }
}
~~~