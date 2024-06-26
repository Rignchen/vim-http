import vim
import re
import requests
import datetime
import os
import html

class http_request:
    def __init__(self, method: str = "", url: str = "", headers: dict[str, str] = {}, body: str = "", instructions: list[str] = []):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.instructions = list(set(instructions))
    def __str__(self):
        name = [i for i in self.instructions if i.startswith("name")][-1]
        istructions = "".join(f'\n#@ {i}' for i in self.instructions)
        headers = "".join(f'\n{k}: {v}' for k,v in self.headers.items())
        return f"{name}{istructions}\n{self.method} {self.url}{headers}\n\n{self.body}"
    def run(self):
        # parse the instructions
        parced_instructions = {}
        for i in self.instructions:
            if not i.startswith(("@name", "@no-log", "@no-output", "@html", "@file-format", "@output-format", "@file-extension", "@timeout")):
                raise ValueError(f"Unknown instruction: {i}")
            parced_instructions[i.split(' ')[0]] = i.split(' ')[1] if ' ' in i else True

        try:
            response = requests.request(self.method, self.url, headers=self.headers, data=self.body, timeout=int(parced_instructions.get("@timeout", 10)))
        except requests.exceptions.ConnectTimeout:
            return http_response(f"{http_color.red}Connection Timeout{http_color.reset}", 408, {}, parced_instructions)
        except requests.exceptions.ConnectionError:
            return http_response(f"{http_color.red}Connection Error{http_color.reset}", 404, {}, parced_instructions)

        return http_response(response.text, response.status_code, response.headers, parced_instructions)

class http_color:
    reset = "\033[0m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    white = "\033[37m"
    black = "\033[30m"
    gray = "\033[90m"
    bold = "\033[1m"

class http_response:
    def __init__(self, text: str, code: int, headers: dict[str, str], instructions: dict[str, str|bool]):
        self.text = text
        self.code = code
        self.headers = "".join(f'\n{k}: {v}' for k,v in headers.items())
        self.instructions = instructions
    def write_in_file(self):
        # ensure you're supposed to write in a file
        if self.instructions.get("@no-log", False):
            return

        # get the name of the file
        name = f".vim_http/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{self.instructions.get('@name', '')}_{self.code}"

        # get the file format
        format = '.' + self.instructions.get("@file-extension", "log")

        # ensure the file doesn't already exist
        os.makedirs(os.path.dirname(f"{name}.{format}"), exist_ok=True)
        if os.path.exists(f"{name}.{format}"):
            count = 0
            while os.path.exists(f"{name}({count}).{format}"):
                count += 1
            name = f"{name}({count})"

        # write the response in the file
        with open(f"{name}.{format}", "w") as file:
            file.write(self.instructions.get("@file-format", "%c\n%h\n\n%t").replace("%n", self.instructions.get('@name', '')).replace("%c", str(self.code)).replace("%h", self.headers).replace("%t", self.text))
    def display(self):
        # ensure you're supposed to display the response
        if self.instructions.get("@no-output", False):
            return

        # remove html balises if needed
        if self.instructions.get("@html", False):
            # remove comments
            self.text = re.sub('<!--.+?-->', '', self.text, flags=re.DOTALL)
            # remove scripts
            self.text = re.sub('<script.+?</script>', '', self.text, flags=re.DOTALL)
            # remove styles
            self.text = re.sub('<style.+?</style>', '', self.text, flags=re.DOTALL)
            # remove html balises
            self.text = re.sub('<(?!br>)[^<]+?>', '', self.text, flags=re.DOTALL)
            # remove multiple spaces
            self.text = re.sub('\n\s+', '\n', self.text, flags=re.DOTALL)
            self.text = re.sub('\s{2,}', ' ', self.text, flags=re.DOTALL)
            # add line breaks back
            self.text = self.text.replace('<br>', '\n')
            # change the html special characters
            self.text = html.unescape(self.text)

        name = f"{http_color.purple}{self.instructions['@name']}{http_color.reset}" if '@name' in self.instructions else ""

        if self.code == 200:          code = ""
        elif 201 <= self.code <= 299: code = f"{http_color.green }{http_color.bold}{self.code}{http_color.reset}"
        elif 300 <= self.code <= 399: code = f"{http_color.yellow}{http_color.bold}{self.code}{http_color.reset}"
        elif 400 <= self.code <= 499: code = f"{http_color.purple}{http_color.bold}{self.code}{http_color.reset}"
        elif 500 <= self.code <= 599: code = f"{http_color.red   }{http_color.bold}{self.code}{http_color.reset}"
        else:                         code = f"{http_color.blue  }{http_color.bold}{self.code}{http_color.reset}"

        headers = f"{http_color.gray}{self.headers}{http_color.reset}\n" if self.headers != "" else ""

        http_print(self.instructions.get("@output-format", "%n\n%c\n%h\n\n%t").replace("%n", name).replace("%c", code).replace("%h", headers).replace("%t", self.text))

def http_print(text: str):
    print(text)
    return
    vim.command("new")
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
    - @file-format <format>: the log file will be written respecting the specified format (%t -> response's text, %c -> exit code, %h -> headers and %n -> name. Default is %c\n%h\n\n%t)
    - @output-format <format>: the response output will be written respecting the specified format (%t -> response's text, %c -> exit code, %h -> headers and %n -> name. Default is %n\n%c\n%h\n\n%t)
    - @file-extension <extension>: the log file will use the specified extension
    - @timeout <seconds>: set the timeout for the request, by default it's 10 seconds

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

def http_parseRequest(request: list[str]):
    """
    Parse a request and return the method, the url, the headers and the body

    Parsed format:
    method url
    header_name: header_value

    body
    """
    if len(request) == 0:
        raise ValueError("Request cannot be empty")
    output = http_request()

    # remove leading and trailing whitespaces
    for n in range(len(request)):
        if re.match('^\s*#', request[n]): # comments
            request[n] = re.sub(' {2,}',' ', request[n].replace('\t',' '), flags=re.DOTALL).strip()
        elif re.match('^\s.+\s:', request[n]): # headers
            continue
        elif re.match('^\s*$', request[n]): # begining of the body
            break # we have to keep the whole body intact so we can't remove leading and trailing whitespaces

    # get instructions, remove other comments
    for i in range(n - 1, -1, -1):
        if request[i].startswith("#"):
            if re.match('^#{3,} {0,}[a-zA-Z0-9_\-]{1,}$',request[i]):
                request[i] = re.sub('^#{3,} {0,}','#@name ',request[i], flags=re.DOTALL)
            request[i] = re.sub('^#\s+','#',request[i], flags=re.DOTALL)
            if re.match('^#@.+',request[i]):
                output.instructions.insert(0,request.pop(i)[1:])
            else:
                request.pop(i)

    # get method and url
    request[0] = request[0].split(' ')
    if len(request[0]) != 2:
        raise ValueError("Request need to follow this format:\n#comments\nMETHOD url\nheader_name: header_value\n\nboddy")
    output.method = request[0][0]
    output.url = request.pop(0)[1]

    if len(request) > 0:
        # get headers
        while len(request) > 0 and request[0] != "":
            header = request.pop(0).split(':',1)
            if len(header) != 2:
                raise ValueError("Header need to follow this format:\nheader_name: header_value")
            output.headers[header[0].strip()] = header[1].strip()

        # get body
        if len(request) > 1:
            output.body = "\n".join(request[1:])

    return output

def http_curl(command: list[str]):
    ...

...;...;...;...;...;...

vim.current.window.cursor = (28,5)

http_parseRequest(http_getCurrentRequest()).run().display()

