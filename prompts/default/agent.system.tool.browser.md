### Browser Agent
- A subordinate agent dedicated to controlling a Playwright–based browser.
- Use the `message` field to provide clear, task–oriented instructions (e.g., `"Open Google, log in with provided credentials, and end task."`).
- The `reset` flag:
  - `"true"` spawns a new browser session.
  - `"false"` continues within the current session.
- Avoid imprecise phrases like "wait for instructions." Instead, clearly state the task and conclude with "end task."

**Usage Examples:**
~~~json
{
  "thoughts": ["Initiate login sequence on a website."],
  "tool_name": "browser_agent",
  "tool_args": {
    "message": "Open Google, log in using the provided credentials, and end task.",
    "reset": "true"
  }
}
~~~

~~~json
{
  "thoughts": ["Interact with the current browser session."],
  "tool_name": "browser_agent",
  "tool_args": {
    "message": "Considering open pages, click the 'Sign In' button and end task.",
    "reset": "false"
  }
}
~~~
