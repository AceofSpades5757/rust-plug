" Plugin Guard
if exists("g:loaded_rust_plug")
    finish
endif
let g:loaded_rust_plug = 1

" Config
let g:rustplug_max_work_time = 5

" Public API
command! -nargs=+ RustPlugRun call rustplug#run(<f-args>)
command! -nargs=? RustPlugRunAll call rustplug#runall(<f-args>)
command! -nargs=+ RustPlugInstall call rustplug#install(<f-args>)
command! -nargs=+ RustPlugRunBinary call rustplug#run_binary(<f-args>)

" Run all Rust Plugins
call rustplug#runall()
