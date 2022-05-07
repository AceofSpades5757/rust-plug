" Plugin:      rust-plug
" Author:      Kyle L. Davis <AceofSpades5757.github@gmail.com>
" Version:     0.1.0
" Modified:    2022 Apr 30
" Description:
"
"     Vim plugin framework for Rust.
"

" Plugin Guard
if exists("g:loaded_rust_plug")
    finish
endif
let g:loaded_rust_plug = 1

" Config
" Deprecated by ch_open's waittime option
"let g:rustplug_max_startup_time = 5
let g:rustplug_max_work_time = 5

" Public API
command! -nargs=? RustPlugRunAll call rustplug#runall(<f-args>)
command! -nargs=+ RustPlugRun call rustplug#run(<f-args>)
command! -nargs=+ RustPlugInstall call rustplug#install(<f-args>)
command! -nargs=+ RustPlugRunBinary call rustplug#run_binary(<f-args>)

" Run all Rust Plugins
call rustplug#runall()
