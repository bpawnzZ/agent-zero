### Code Execution Tool
Execute terminal commands or code (Python, Node.js) for computational or software tasks.

- Place your code in the `"code"` argument with proper escaping and indentation.
- Set the `"runtime"` argument as one of: `"terminal"`, `"python"`, `"nodejs"`, `"output"`, or `"reset"`.
- For interactive prompts (e.g., Y/N), use `"terminal"` runtime.
- Use `"output"` to wait for long‐running scripts; use `"reset"` to forcibly terminate a process.
- Use standard package managers (`pip`, `npm`, `apt-get`) for installations when using the terminal.
- **Avoid implicit print statements.** In Python use `print()`, in Node.js use `console.log()`.
- Ensure your code has no placeholder data—replace with actual values.
- Do not switch tools during code execution; await responses before continuing.
- Verify all dependencies before running the code.

**Usage Examples:**

*Executing Python code:*
~~~json
{
    "thoughts": ["Obtaining the current working directory."],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "python",
        "code": "import os\nprint(os.getcwd())"
    }
}
~~~

*Executing a terminal command:*
~~~json
{
    "thoughts": ["Installing necessary package."],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "terminal",
        "code": "apt-get install zip"
    }
}
~~~

*Waiting for output from a long-running script:*
~~~json
{
    "thoughts": ["Awaiting process completion."],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "output"
    }
}
~~~

*Resetting the terminal:*
~~~json
{
    "thoughts": ["Terminal unresponsive; initiating reset."],
    "tool_name": "code_execution_tool",
    "tool_args": {
        "runtime": "reset"
    }
}
~~~