# Description

A framework for creating Vim plugins in Rust.

# Installation

Add the plugin using `vim-plug`.

_Refer to [rust-plug-poc](https://github.com/AceofSpades5757/rust-plug-poc) for an example._

``` vim
Plug 'AceofSpades5757/rust-plug' |  " Requirement
    \ Plug 'AceofSpades5757/rust-plug-poc',
        \ {
            \ 'do': ':call rustplug#run(''AceofSpades5757/rust-plug-poc'')',
        \ }
```

***WARNING: Need to run `PlugInstall` twice to allow the Python runtime path to update.***

Then install using `PlugInstall`. The posthook, `do`, will install the Rust plugin, and run it.

# Usage

## Help

`:help rust-plug.txt`

## Options

* `g:rustplug_max_startup_time`: Seconds to wait for plugin to startup (start the binary).
* `g:rustplug_max_work_time`: Seconds to allow the plugin to run (run the binary).

## Functions

* `rustplug#run`: Run Rust plugin. Will build if not already built. Will install if not already installed.
* `rustplug#install`: Build and install Rust plugin.
* `rustplug#run_binary`: Run a specific binary, given path.

## Commands (matched to functions)

* `RustPlugRun`: Run Rust plugin. Will build if not already built. Will install if not already installed.
* `RustPlugInstall`: Build and install Rust plugin.
* `RustPlugRunBinary`: Run a specific binary, given path.
