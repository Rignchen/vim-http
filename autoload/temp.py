import vim

def http_print(text: str):
    print(text)
    return
    vim.command(f"new")
    vim.command(f"normal! i{text}\n")

def http_help():
    http_print("""This is the help function for the http plugin.
    - Http: displays this help message.
    - HttpRun: run the current request.
    - HttpRunAll: run all requests in the current buffer.
    - HttpCurl: Transform the curl command into the corresponding http request.

Requests are defined inside .http files using the folowing syntax:
    METHOD url
    heaser_name: header_value

    body

Requests can be separated by 3 # characters on a new line.
# characters can be used at the beginning of a line to add comments.
#@ can be used to give instructions to the plugin.

List of available instructions:
    - @name: give a name to the request. This name will be used to name the log file
    - @no-log: by default the plugin store the response in a log file at the root of the project. This instruction disable this behavior
    - @no-output: by default the plugin display the response in a new buffer. This instruction disable this behavior
    - @html: remove every html balises from the response before displaying it in the buffer, the log file is not affecte
    - @file-format <format>: the log file will be named with the specified format

Example:
    ### Add toto to the users
    POST http://localhost:3000/users
    Authorization: Bearer 1234567890

    {
        "name": "toto",
        "age": 42
    }
""")

def http_getCurrentRequest() -> list[str]:
    lines = vim.current.buffer
    start_line, _ = vim.current.window.cursor
    start = start_line - 1
    stop = start_line
    while start > 0 and not lines[start].strip().startswith("###"):
        start -= 1
    while stop < len(lines) and not lines[stop].strip().startswith("###"):
        stop += 1
    return lines[start:stop]

def http_parseRequest(request: list[str]) -> tuple[list[str], str, str, dict[str, str], str]:
    """
    Parse a request and return the method, the url, the headers and the body

    Parsed format:
    method url
    header_name: header_value

    body
    """
    output = [[], "", "", {}, ""]
    if len(request) == 0:
        raise ValueError("Request cannot be empty")
    request[0] = request[0].replace(,' ').strip().split(' ')
    if len(request[0]) != 2:
        raise ValueError("Request need to follow this format:\n#comments\nMETHOD url\nheader_name: header_value\n\nboddy")
    output[0:2] = request.pop(0)
    if len(request) > 0:

def http_curl(command: list[str]):
    ...

...;...;...;...;...;...

vim.current.window.cursor = (7,5)

print(http_getCurrentRequest())
