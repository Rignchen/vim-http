" Title:        Http
" Description:  A plugin for http
" Last Change:  24 April 2024
" Maintainer:   Rignchen <https://github.com/Rignchen>
" License:      CC-BY-NC-SA


python3 << EOF
import vim

def http_help():
    print("""This is the help function for the http plugin.
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
""")

def getCurrentRequest():
    lines = vim.current.buffer
    start_line, _ = vim.current.window.cursor
    start = start_line - 1
    stop = start_line
    while start > 0 and not lines[start].strip().startswith("###"):
        start -= 1
    while stop < len(lines) and not lines[stop].strip().startswith("###"):
        stop += 1
    return lines[start:stop]

EOF

function! http#help()
	python3 http_help()
endfunction


" TEST CASES

function! _comment()

###
# This is a comment
GET https://jsonplaceholder.typicode.com/posts/1

###
POST https://jsonplaceholder.typicode.com/posts
Content-Type: application/json

{
	"key": "value"
}
###

endfunction

python3 print(getCurrentRequest())

