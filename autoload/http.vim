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
""")

EOF

function! http#help()
	python3 http_help()
endfunction

