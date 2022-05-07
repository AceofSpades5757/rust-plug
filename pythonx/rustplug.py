from __future__ import annotations

import logging
import platform
import subprocess
from pathlib import Path
from typing import Final
from typing import Iterable
from typing import Optional


log_dir: Path = Path(__file__).parent / 'logs'
log_dir.mkdir(exist_ok=True)
log_file: Path = log_dir / Path(__file__).with_suffix('.log').name

logging.getLogger().setLevel(logging.DEBUG)  # ROOT Logger
logger = logging.getLogger(__name__)

# Formatter
date_format = '%Y-%m-%dT%H:%M:%S%z'
message_format = '{asctime} - {name} - {levelname:<8} - {message}'
formatter = logging.Formatter(
    datefmt=date_format, style='{', fmt=message_format, validate=True
)

# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# logger.addHandler(stream_handler)

# File Handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


RUN_BINARY_VIM_FUNCTION: Final[str] = 'rustplug#run_binary'


class Plugin:
    """ Represents a Rust Plugin. """

    def __init__(self, name: str, env: Environment = None):

        logger.info(f'Init Plugin - name={name}')
        self.name: str = name
        self.env: Optional[Environment] = env

        if env is not None:
            self.bin_directory.mkdir(parents=True, exist_ok=True)

    @property
    def directory(self) -> Path:
        if self.env is None:
            raise ValueError('Environment required to run this method.')
        return self.env.vim_plug / self.name  # type: ignore

    def build(self) -> None:
        """ Build plugin to create binaries. """

        logger.info(f'Building: {self.name}')  # DEBUG REMOVE
        logger.info(f'Building: {self.directory}')
        process = subprocess.run(
            'cargo build --release'.split(),
            cwd=self.directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, _ = process.stdout.decode(), process.stderr.decode()
        if process.returncode != 0:
            raise RuntimeError(f"Unable to build Rust plugin: {self}")

    @property
    def built(self) -> bool:
        """ Was this already built?

        If self.install was run then it should have generated binaries.
        """
        binaries = self.directory.glob('target/release/*.exe')
        return bool(list(binaries))

    @property
    def installed(self) -> bool:
        """ Was this already installed?

        If self.install was run then it should have generated binaries.
        """
        return bool(list(self.binaries))

    def install(self) -> None:
        """Install binaries created."""

        if self.env is None:
            raise ValueError('Environment required to run this method.')

        import shutil

        binaries = self.directory.glob('target/release/*.exe')
        logger.info(f'Installing: {binaries}')
        for binary in binaries:
            logger.info(f'Installing Binary: {binary} to {self.bin_directory}')
            shutil.copy2(binary, self.bin_directory)  # type: ignore

    @property
    def bin_directory(self) -> Path:

        if self.env is None:
            raise ValueError('Environment required to run this method.')

        return self.env.rust_bin_dir / self.name  # type: ignore

    @property
    def binaries(self) -> Iterable[Path]:
        return self.bin_directory.glob('*.exe')

    def run(self) -> None:
        try:
            import vim  # type: ignore
        except ImportError:
            raise RuntimeError('This method is only available inside Vim.')

        for binary in self.binaries:
            readable: str = binary.as_posix()
            logger.info(f'Running binary (readable): {readable}')

            vim.command(f'call {RUN_BINARY_VIM_FUNCTION}("{readable}")')
            # run_binary: Callable = vim.bindeval("function('rustplug#run')")
            # run_binary('AceofSpades5757/rust-plug-poc')


class Environment:
    """ Rust-Plug Vim Plugin Environment """

    def __init__(self, plugin_name: str):

        logger.info(f'Init Environment - plugin_name={plugin_name}')
        self.plugin: Plugin = Plugin(name=plugin_name, env=self)

    @property
    def vimfiles(self) -> Path:
        if platform.system() == 'Linux':
            return Path.home() / '.vim'
        elif platform.system() == 'Windows':
            return Path.home() / 'vimfiles'
        else:
            raise NotImplementedError(
                "Platform {platform.system()} not supported."
            )

    @property
    def rust_bin_dir(self) -> Path:
        return self.vimfiles / 'rustplug'

    @property
    def vim_plug(self) -> Path:
        """ Vim-Plug directory """
        return self.vimfiles / 'plugged'


import unittest


class TestPlugin(unittest.TestCase):
    def test_simple(self) -> None:

        plugin = Plugin(name='my_plugin')

        self.assertEqual(plugin.name, 'my_plugin')
        self.assertIsNone(plugin.env)

        with self.assertRaises(Exception):
            self.assertEqual(plugin.directory, 'my_plugin')


class TestEnvironment(unittest.TestCase):
    def test_simple(self) -> None:

        plugin_name = 'my_plugin_with_env'
        env = Environment(plugin_name=plugin_name)

        if platform.system() == 'Linux':
            self.assertEqual(env.vimfiles, Path.home() / '.vim')
        elif platform.system() == 'Windows':
            self.assertEqual(env.vimfiles, Path.home() / 'vimfiles')

        self.assertEqual(
            env.plugin.directory,
            Path.home() / 'vimfiles/plugged' / plugin_name,
        )
        if platform.system() == 'Linux':
            self.assertEqual(env.vim_plug, Path.home() / '.vim/plugged')
        elif platform.system() == 'Windows':
            self.assertEqual(env.vim_plug, Path.home() / 'vimfiles/plugged')


if __name__ == '__main__':
    unittest.main()
