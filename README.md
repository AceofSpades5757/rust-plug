# Description

A framework for creating Vim plugins in Rust.

# Installation

Add the plugin using `vim-plug`.

``` vim
Plug 'AceofSpades5757/rust-plug' |  " Requirement
    \ Plug 'AceofSpades5757/vim-rust-plugin-poc',
        \ {
            \ 'do': ':call rustplug#run(''AceofSpades5757/vim-rust-plugin-poc'')',
        \ }
```

***WARNING: Need to run `PlugInstall` twice to allow the Python runtime path to update.***

Then install using `PlugInstall`. The posthook, `do`, will install the Rust plugin, and run it.

# Usage

Functions

* `rustplug#run`: Run Rust plugin. Will build if not already built. Will install if not already installed.
* `rustplug#install`: Build and install Rust plugin.
* `rustplug#run_binary`: Run a specific binary, given path.

Commands (matched to functions)

* `RustPlugRun`: Run Rust plugin. Will build if not already built. Will install if not already installed.
* `RustPlugInstall`: Build and install Rust plugin.
* `RustPlugRunBinary`: Run a specific binary, given path.
