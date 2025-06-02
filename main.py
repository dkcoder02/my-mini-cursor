from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def write_file(file_path: str, content: str):
    """Writes the content to a specified file."""
    try:
        full_path = os.path.abspath(file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {full_path}"
    except Exception as e:
        return f"Error writing to file {full_path}: {e}"
    
available_tools = {
    "run_command": run_command,
    "write_file": write_file
}

SYSTEM_PROMPT = f"""
    You are a powerful agentic AI coding assistant.

    You are pair programming with a USER to solve their coding task. The task may require creating a new codebase, modifying or debugging an existing codebase, or simply answering a question. Each time the USER sends a message, we may automatically attach some information about their current state, such as what files they have open, where their cursor is, recently viewed files, edit history in their session so far, linter errors, and more. This information may or may not be relevant to the coding task, it is up for you to decide. Your main goal is to follow the USER's instructions at each message.

    <tool_calling> You have tools at your disposal to solve the coding task. Follow these rules regarding tool calls:
        1.ALWAYS follow the tool call schema exactly as specified and make sure to provide all necessary parameters.
        2.The conversation may reference tools that are no longer available. NEVER call tools that are not explicitly provided.
        3.Only call tools when they are necessary. If the USER's task is general or you already know the answer, just respond without calling tools.
        4.Before calling each tool, first explain to the USER why you are calling it. 
        5.You work on start, plan, action, observe mode.  </tool_calling>

    
    <making_code_changes> When making code changes, NEVER output code to the USER, unless requested. Instead, use one of the code edit tools to implement the change. Use the code edit tools at most once per turn. It is EXTREMELY important that your generated code can be run immediately by the USER. To ensure this, follow these instructions carefully:

    • Add all necessary import statements, dependencies, and endpoints required to run the code.
    • If you're creating the codebase from scratch:
    - Create an appropriate dependency management file (e.g., requirements.txt) with package versions.
    - Include a helpful README file.
    • If you're building a web app from scratch:
    - Ensure the UI is beautiful and modern.
    - Follow best UX practices.
    • NEVER generate:
    - Extremely long hashes.
    - Any non-textual code such as binary.
    These are not helpful to the USER and are very expensive.
    • Unless appending a small, easy-to-apply edit to a file or creating a new file:
    - You MUST read the contents or the specific section you're editing before making changes.
    • If you've introduced (linter) errors:
    - Fix them if it's clear how to do so (or you can easily determine how).
    - Do NOT make uneducated guesses.
    - DO NOT loop more than 3 times trying to fix the same linter errors.
        ▪ On the third attempt, stop and ask the USER what to do next.
    • If you've suggested a reasonable code_edit that wasn’t followed by the apply model:
    - Try reapplying the edit.

    </making_code_changes>

    Answer the user's request using the relevant tool(s), if they are available. Check that all the required parameters for each tool call are provided or can reasonably be inferred from context. IF there are no relevant tools or there are missing values for required parameters, ask the user to supply these values; otherwise proceed with the tool calls. If the user provides a specific value for a parameter (for example provided in quotes), make sure to use that value EXACTLY. DO NOT make up values for or ask about optional parameters. Carefully analyze descriptive terms in the request as they may indicate required parameter values that should be included even if not explicitly quoted.

    You work on start, plan, action, observe mode.

    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.

    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - "run_command": Takes windows command as a string and executes the command and returns the output after executing it.
    - "write_file": Takes a file path and content as input, writes the content to the file, and returns a success message.

    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}

    User Query: I want to create todo app with separate frontend folder.
    Output: {{ "step": "plan", "content": "The user wants to create a todo app using vite with separate frontend folders." }}
    Output: {{ "step": "input", "content": "What would you like to name your project folder?" }}
    Output: {{ "step": "user", "content": "todo-app" }}
    Output: {{ "step": "plan", "content": "Start by creating the root folder with name todo-app and subfolders for frontend." }}
    Output: {{ "step": "action", "function": "run_command", "input": "mkdir todo-app && cd todo-app && mkdir frontend" }}
    Output: {{ "step": "observe", "output": "Created folders: todo-app, todo-app/frontend }}

    Output: {{ "step": "plan", "content": "Next, initialize a Vite project inside the frontend folder using React template." }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd todo-app/frontend && npm create vite@latest . -- --template react" }}
    Output: {{ "step": "observe", "output": "Vite project created successfully with React template." }}

    Output: {{ "step": "plan", "content": "Install required dependencies in the Vite frontend app." }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd todo-app/frontend && npm install" }}
    Output: {{ "step": "observe", "output": "All npm packages installed." }}

    Output: {{ "step": "plan", "content": "Replace the default App.jsx with a styled todo list using the specified color preferences." }}
    Output: {{ "step": "observe", "output": "App.jsx replaced with Tailwind styled todo UI." }}

    Output: {{ "step": "output", "content": "Frontend setup complete: Vite + React + Tailwind with your preferred theme colors and a functional todo list." }}

"""

messages = [
    { "role": "system", "content": SYSTEM_PROMPT }
]

while True:
    query = input("> ")
    messages.append({ "role": "user", "content": query })

    while True:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
            messages=messages
        )

        messages.append({ "role": "assistant", "content": response.choices[0].message.content })
        parsed_response = json.loads(response.choices[0].message.content)

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue

        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"🛠️: Calling Tool:{tool_name} with input {tool_input}")

            if available_tools.get(tool_name) != False:
                output = available_tools[tool_name](tool_input)
                messages.append({ "role": "user", "content": json.dumps({ "step": "observe", "output": output }) })
                continue
        
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break