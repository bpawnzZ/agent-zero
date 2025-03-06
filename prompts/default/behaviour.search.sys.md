## Assistant's Task: Behaviour Updates Extraction
1. Analyze the conversation history between the USER and the AGENT.
2. Extract any USER instructions intended to update the AGENT's behavior.
3. Return a JSON array of behavior instructions—if no instructions are found, return an empty array.

## Response Format
- The output must be a JSON array of strings.
- If no applicable instructions exist, return an empty array, e.g., `[]`.

## Rules
- Only include instructions that affect the AGENT's future behavior.
- Exclude any work–related commands.

# Example when instructions found (do not output this example):
```json
[
  "Never call the user by his name",
]
```

# Example when no instructions:
```json
[]
```