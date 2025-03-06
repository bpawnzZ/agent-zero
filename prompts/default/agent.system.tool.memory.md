## Memory Management Tools
Manage long–term memories (retrieve, save, delete, or forget). All stored information is user–owned.

### memory_load
Search for memories based on:
- **query:** The search string.
- **threshold:** Matching strictness (0 for any match, up to 1 for exact; default 0.6).
- **limit:** Maximum number of results (default is 5).
- **filter:** A Python expression filtering metadata keys.

**Usage:**
~~~json
{
    "thoughts": ["Searching for memories regarding file compression libraries."],
    "tool_name": "memory_load",
    "tool_args": {
        "query": "File compression library",
        "threshold": 0.6,
        "limit": 5,
        "filter": "area=='main' and timestamp < '2024-01-01 00:00:00'"
    }
}
~~~

### memory_save
Save a text snippet to memory and receive a unique memory ID.

**Usage:**
~~~json
{
    "thoughts": ["Saving solution details for future recall."],
    "tool_name": "memory_save",
    "tool_args": {
        "text": "# Compression solution details..."
    }
}
~~~

### memory_delete
Delete specific memories by providing their IDs (comma–separated).

**Usage:**
~~~json
{
    "thoughts": ["Removing outdated memory entries."],
    "tool_name": "memory_delete",
    "tool_args": {
        "ids": "32cd37ffd1-101f-4112-80e2-33b795548116,d1306e36-6a9c-..."
    }
}
~~~

### memory_forget
Remove memories that match a given query, threshold, and filter.  
_Default threshold is 0.75 to minimize accidental deletion._

**Usage:**
~~~json
{
    "thoughts": ["Forgetting all memories concerning cars."],
    "tool_name": "memory_forget",
    "tool_args": {
        "query": "cars",
        "threshold": 0.75,
        "filter": "timestamp.startswith('2022-01-01')"
    }
}
~~~