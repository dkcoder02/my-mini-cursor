from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def write_file(input_data):
    """Writes the content to a specified file."""
    try:
        file_path = input_data['file_path']
        content = input_data['content']
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

new_code = '''
import React, { useState } from 'react';

const App = () => {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  const addTodo = () => {
    if (!input.trim()) return;
    setTodos([...todos, { id: Date.now(), text: input, completed: false }]);
    setInput('');
  };

  const toggleComplete = (id) => {
    setTodos(
      todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  return (
    <div className='min-h-screen bg-gray-100 flex items-center justify-center p-4'>
      <div className='bg-white shadow-md rounded-xl w-full max-w-md p-6'>
        <h1 className='text-2xl font-bold text-center mb-4'>📝 ToDo App</h1>
        <div className='flex gap-2 mb-4'>
          <input
            type='text'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className='w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'
            placeholder='Add a new task...'
          />
          <button
            onClick={addTodo}
            className='bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded'
          >
            Add
          </button>
        </div>
        <ul className='space-y-2'>
          {todos.map((todo) => (
            <li
              className={`flex items-center justify-between p-3 rounded ${todo.completed ? 'bg-green-100' : 'bg-gray-200'}`}
            >
              <span
                className={`flex-1 cursor-pointer ${todo.completed ? 'line-through text-gray-500' : ''}`}
                onClick={() => toggleComplete(todo.id)}
              >
                {todo.text}
              </span>
              <button
                onClick={() => deleteTodo(todo.id)}
                className='ml-3 text-red-500 hover:text-red-700'
              >
                ❌
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;




'''

edit_todo_new_code = '''
import React, { useState } from 'react';

const App = () => {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');
  const [editId, setEditId] = useState(null);
  const [editInput, setEditInput] = useState('');

  const addTodo = () => {
    if (!input.trim()) return;
    setTodos([...todos, { id: Date.now(), text: input, completed: false }]);
    setInput('');
  };

  const toggleComplete = (id) => {
    setTodos(
      todos.map((todo) =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
      )
    );
  };

  const deleteTodo = (id) => {
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  const startEdit = (id, currentText) => {
    setEditId(id);
    setEditInput(currentText);
  };

  const saveEdit = (id) => {
    setTodos(
      todos.map((todo) =>
        todo.id === id ? { ...todo, text: editInput } : todo
      )
    );
    setEditId(null);
    setEditInput('');
  };

  const cancelEdit = () => {
    setEditId(null);
    setEditInput('');
  };

  return (
    <div className='min-h-screen bg-gray-100 flex items-center justify-center p-4'>
      <div className='bg-white shadow-md rounded-xl w-full max-w-md p-6'>
        <h1 className='text-2xl font-bold text-center mb-4'>📝 ToDo App</h1>
        <div className='flex gap-2 mb-4'>
          <input
            type='text'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className='w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'
            placeholder='Add a new task...'
          />
          <button
            onClick={addTodo}
            className='bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded'
          >
            Add
          </button>
        </div>
        <ul className='space-y-2'>
          {todos.map((todo) => (
            <li
              key={todo.id}
              className={`flex items-center justify-between p-3 rounded ${todo.completed ? 'bg-green-100' : 'bg-gray-200'}`}
            >
              {editId === todo.id ? (
                <div className='flex-1 flex gap-2 items-center'>
                  <input
                    value={editInput}
                    onChange={(e) => setEditInput(e.target.value)}
                    className='w-full border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-300'
                  />
                  <button
                    onClick={() => saveEdit(todo.id)}
                    className='text-green-600 hover:text-green-800 font-semibold'
                  >
                    💾
                  </button>
                  <button
                    onClick={cancelEdit}
                    className='text-gray-600 hover:text-gray-800 font-semibold'
                  >
                    ❌
                  </button>
                </div>
              ) : (
                <>
                  <span
                    className={`flex-1 cursor-pointer ${todo.completed ? 'line-through text-gray-500' : ''}`}
                    onClick={() => toggleComplete(todo.id)}
                  >
                    {todo.text}
                  </span>
                  <div className='flex gap-2 ml-3'>
                    <button
                      onClick={() => startEdit(todo.id, todo.text)}
                      className='text-blue-500 hover:text-blue-700'
                    >
                      ✏️
                    </button>
                    <button
                      onClick={() => deleteTodo(todo.id)}
                      className='text-red-500 hover:text-red-700'
                    >
                      ❌
                    </button>
                  </div>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default App;

'''

tailwindcss_vite_config_code= '''
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
    plugins: [
        react(),
        tailwindcss(),
    ],
})
'''

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
    • If you've suggested a reasonable code_edit that wasn't followed by the apply model:
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
    - frontend side always uses vite and do not use create-react-app

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

    User Query: create a todo app with separate frontend folder.
    Output: {{ "step": "plan", "content": "The user wants to create a todo app using vite with separate frontend folders after installtion of tailwind css and write a code of todo functionality" }}
    Output: {{ "step": "input", "content": "What would you like to name your project folder?" }}
    Output: {{ "step": "user", "content": "todo-app" }}
    Output:{{ "step": "input", "content": "Which CSS framework would you prefer for the frontend? (Tailwind/ None"}}
    Output:{{ "step": "user", "content": "tailwind" }}
    Output: {{ "step": "plan", "content": "Start by creating the root folder with name todo-app and subfolders for frontend." }}
    Output: {{ "step": "action", "function": "run_command", "input": "mkdir todo-app && cd todo-app && mkdir frontend" }}
    Output: {{ "step": "observe", "output": "Created folders: todo-app, todo-app/frontend }}
    Output: {{ "step": "plan", "content": "Next, initialize a Vite project inside the frontend folder using React template." }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd todo-app/frontend && npm create vite@latest . -- --template react" }}
    Output: {{ "step": "plan", "content": "Start installation of tailwind css in todo-app/frontend" }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd todo-app/frontend && npm install tailwindcss @tailwindcss/vite" }}
    Output: {{ "step": "plan", "content": "Add the @tailwindcss/vite plugin to your Vite configuration." }}
    Output: {{ "step": "action", "function": "write_file", "input": "file_path":"todo-app/frontend/vite.config.js","content":{tailwindcss_vite_config_code} }}
    Output: {{ "step": "plan", "content": "Add imports Tailwind CSS in index.css file." }}
    Output: {{ "step": "action", "function": "write_file", "input": "file_path":"todo-app/frontend/src/index.css","content":@import "tailwindcss"; }}
    Output: {{ "step": "observe", "output": "Vite project created successfully with React template." }}
    Output: {{ "step": "plan", "content": "Install required dependencies in the Vite frontend app." }}
    Output: {{ "step": "action", "function": "run_command", "input": "cd todo-app/frontend && npm install" }}
    Output: {{ "step": "observe", "output": "All npm packages installed." }}
    Output: {{ "step": "plan", "content": "Write clean and well-formatted code for a Todo app with create, read, and delete functionalities." }}
    Output: {{ "step": "action", "function": "write_file", "input": "file_path":"todo-app/frontend/src/App.jsx","content":{new_code} }}
    Output: {{ "step": "plan", "content": "Write clean and well-formatted code for a Todo app. now add new functionality is edit todos " }}
    Output: {{ "step": "action", "function": "write_file", "input": "file_path":"todo-app/frontend/src/App.jsx","content":{edit_todo_new_code} }}

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