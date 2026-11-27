#!/usr/bin/env python3
"""A stand-in agent for `[agent] preset = "custom"` in tests and smokes.

Reads the prompt on stdin and acts on its first word:
  answer  print an answer
  edit    append a line to the open note through Slate's MCP server, then answer
  sleep   record its pid in $FAKE_AGENT_DIR/pid and sleep
It reaches notes only as a real agent would: by starting the server named in
$SLATE_AGENT_MCP_CONFIG and speaking JSON-RPC to it over stdio.
"""
import json
import os
import re
import subprocess
import sys
import time


def call_tool(name, arguments):
    servers = json.load(open(os.environ['SLATE_AGENT_MCP_CONFIG']))['mcpServers']
    if 'slate' not in servers:
        return 'no slate server configured'
    server = servers['slate']
    proc = subprocess.Popen([server['command'], *server['args']], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, text=True)

    def request(ident, method, params):
        proc.stdin.write(json.dumps(dict(jsonrpc='2.0', id=ident, method=method, params=params)) + '\n')
        proc.stdin.flush()
        return json.loads(proc.stdout.readline())

    request(1, 'initialize', dict(protocolVersion='2025-06-18', capabilities={},
                                  clientInfo=dict(name='fake-agent', version='0')))
    result = request(2, 'tools/call', dict(name=name, arguments=arguments))
    proc.stdin.close()
    proc.wait(timeout=10)
    result = result.get('result', result)
    return 'refused: ' + result['content'][0]['text'] if result.get('isError') else 'ok'


prompt = sys.stdin.read()
if os.environ.get('FAKE_AGENT_DIR'):
    with open(os.path.join(os.environ['FAKE_AGENT_DIR'], 'prompt.txt'), 'w') as out:
        out.write(prompt)
word = prompt.split()[0]
note = re.search(r'\(id ([^)]+)\)', prompt).group(1)
if word == 'answer':
    print('ANSWER-42')
elif word == 'edit':
    print('edit', call_tool('append_to_note', dict(id=note, text='agent line')))
elif word == 'sleep':
    with open(os.path.join(os.environ['FAKE_AGENT_DIR'], 'pid'), 'w') as out:
        out.write(str(os.getpid()))
    time.sleep(120)
else:
    sys.exit(f'fake agent: unknown request {word!r}')
