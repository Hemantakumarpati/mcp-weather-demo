# MCP Sample: Weather Server

This is a simple example of a Model Context Protocol (MCP) server and client in Python.

## Prerequisites

- Python 3.10+
- `mcp` package

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

The server is designed to run over stdio, which is how MCP clients (like Claude Desktop or the provided `src/mcp_client.py`) communicate with it.

You usually don't run it directly in the terminal to interact with it, but you can check if it starts:
```bash
python src/weather_server.py
```
(It will wait for JSON-RPC messages on stdin)

## Running the Client Demo

The client launcher script starts the server as a subprocess and communicates with it:

```bash
# Interactive mode
python src/mcp_client.py

# Or pass a city argument
python src/mcp_client.py "Paris"
```

Output should look like:
```
Connected to server.
Available tools: ['get_weather']

Calling get_weather for 'Paris'...
Result: Weather in Paris, France: 15°C, Wind: 10 km/h
```
