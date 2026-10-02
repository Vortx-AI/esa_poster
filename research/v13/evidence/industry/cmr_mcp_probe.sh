#!/bin/sh
# Probe NASA's official Earthdata/CMR MCP server: list tools, call get_granules, save raw.
set -e
EP=https://cmr.earthdata.nasa.gov/mcp/v1
H='-H Content-Type:application/json -H Accept:application/json,text/event-stream'
SID=$(curl -sS -m 30 -D - -o /dev/null -X POST $EP $H -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}' | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2}' | tr -d '\r')
echo "session=$SID"
curl -sS -m 30 -X POST $EP $H -H "mcp-session-id: $SID" -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' -o /dev/null
curl -sS -m 30 -X POST $EP $H -H "mcp-session-id: $SID" -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' > cmr_tools_list.sse
curl -sS -m 60 -X POST $EP $H -H "mcp-session-id: $SID" -d "$1" > cmr_call.sse
