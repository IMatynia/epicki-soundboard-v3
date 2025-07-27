# God i hate windows
set shell := ["powershell.exe", "-c"] 

all: compile-ui

compile-ui:
    uv run -m tools.compile_ui 