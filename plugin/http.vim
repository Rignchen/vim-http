" Title:        Http
" Description:  A plugin for http
" Last Change:  24 April 2024
" Maintainer:   Rignchen <https://github.com/Rignchen>
" License:      CC-BY-NC-SA

" Prevents the plugin from being loaded multiple times. If the loaded
if exists("g:loaded_http")
    finish
endif
let g:loaded_http" = 1

" Exposes the plugin's functions for use as commands in Vim.
command! -nargs=0 HttpHelp :call http#help()
command! -nargs=0 HttpRun: call http#run()
command! -nargs=0 HttpRunAll :call http#runall()
command! -nargs=0 HttpCurl :call http#curl()

