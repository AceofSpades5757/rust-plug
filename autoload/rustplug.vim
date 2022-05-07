" Plugin:      rust-plug
" Author:      Kyle L. Davis <AceofSpades5757.github@gmail.com>
" Version:     0.1.0
" Modified:    2022 Apr 30
" Description:
"
"     Vim plugin framework for Rust.
"

function! rustplug#run(plugin) abort

    " To keep it simple, keeping plugin as a repo string
    py3 repo: str = vim.eval('a:plugin')

python3 << EOF
import rustplug
from rustplug import Environment
from rustplug import Plugin
from rustplug import logger  # DEBUG - REMOVE THIS


plugin_name: str = repo.rsplit('/', 1)[-1]
logger.info(f'rustplug#run - name={plugin_name}')  # REMOVE THIS

env: Environment = Environment(plugin_name=plugin_name)
plugin: Plugin = env.plugin

# Setup
# Creates bin dir, builds, and installs if that hasn't been done already.
env.rust_bin_dir.mkdir(parents=True, exist_ok=True)
if not plugin.built:
    plugin.build()
if not plugin.installed:
    plugin.install()

# Runs any binaries generated
plugin.run()
EOF
endfunction

function! rustplug#run_binary(binary) abort

    " PLUGIN STYLE
    "
    " 1. Start Server
    " 2. Connect to Server
    " 3. Do Work
    " 4. Stop (Optional)
    "

    " Verify Arguments
    call rustplug#verify_binary(a:binary)

    " 1. Start Server
    if !exists('job_id')
        let job_id = 0
        let job_options = {}
    endif

    " Try ports 8700 - 8799
    let port = 8700
    for i in range(100)

        let env = environ()
        let env["VII_PLUGIN_PORT"] = port
        let job_options["env"] = env
        let job = job_start([a:binary], job_options)

        " Wait Time
        if job_status(job) == 'fail'
            sleep 50m
        endif

        if job_status(job) == 'fail'
            let port += 1
        else
            break
        endif
    endfor

    " 2. Connect to Server
    " Needs time to wait for server startup

    let ch_address = 'localhost:' . port
    let ch_options = {}
    let channel = ch_open(ch_address, ch_options)

    let count_ = 0
    while ch_status(channel) == "fail"

        " Waiting to Connect
        if count_ >= g:rustplug_max_startup_time
            break
        endif
        let count_ += 1
        sleep 1

        " Try Again
        let channel = ch_open(ch_address, ch_options)

    endwhile

    " 3. Work
    "
    " Should have a set timer to run.

    let count_ = 0
    while ch_status(channel) == "open"
        " Rust Plugin is doing work
        if count_ >= g:rustplug_max_work_time
            break
        endif
        let count_ += 1
        sleep 1
    endwhile

endfunction


function! rustplug#verify_binary(binary)
    if !filereadable(a:binary)
        throw "binary is not readable: " . a:binary
    endif
endfunction

function! rustplug#install(repo, ...) abort
    " Init a Rust Plugin, as you would with VimPlug

" Arguments
py3 repo = vim.eval('a:repo')

python3 << EOF
import rustplug
from rustplug import Environment
from rustplug import Plugin


plugin_name: str = repo.rsplit('/', 1)[-1]

env: Environment = Environment(plugin_name=plugin_name)
plugin: Plugin = env.plugin

env.rust_bin_dir.mkdir(parents=True, exist_ok=True)
if not plugin.built:
    plugin.build()
if not plugin.installed:
    plugin.install()
EOF
endfunction
