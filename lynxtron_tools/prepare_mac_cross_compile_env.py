#!/usr/bin/env python3
"""Prepare macOS host tools and target dependencies using the shared setup."""
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def target_environment(arch):
    if arch not in ('arm64', 'x64'):
        raise ValueError(f'Unsupported macOS target: {arch}')
    env = dict(os.environ)
    env.update(npm_config_arch=arch, npm_config_platform='darwin',
               LYNXTRON_SKIP_DOWNLOAD='1')
    # Patch application needs a Git identity on fresh CI hosts. Keep it scoped
    # to these subprocesses rather than changing the developer's Git config.
    for key, value in {'GIT_AUTHOR_NAME': 'Lynxtron Scripts',
                       'GIT_AUTHOR_EMAIL': 'scripts@lynxtron.com',
                       'GIT_COMMITTER_NAME': 'Lynxtron Scripts',
                       'GIT_COMMITTER_EMAIL': 'scripts@lynxtron.com'}.items():
        env.setdefault(key, value)
    # Habitat selects Node for the host. Only DEPS.extension consumes the
    # requested architecture when selecting the CEF SDK.
    tool_paths = [ROOT / 'buildtools/node/bin',
                  ROOT / 'buildtools/cmake/CMake.app/Contents/bin']
    env['PATH'] = os.pathsep.join(map(str, tool_paths)) + os.pathsep + env['PATH']
    return env


def prepare(arch):
    if platform.system() != 'Darwin':
        raise RuntimeError('macOS and Xcode Command Line Tools are required')
    env = target_environment(arch)
    subprocess.run(['xcrun', '--find', 'clang++'], env=env, check=True)
    subprocess.run([sys.executable, str(ROOT / 'lynxtron_tools/prepare_build_env.py')],
                   cwd=ROOT, env=env, check=True)
    subprocess.run([str(ROOT / 'lynxtron_tools/hab'), 'sync', '.',
                    '--no-history', '--target', 'extension', '--target-only'],
                   cwd=ROOT / 'src', env=env, check=True)
    subprocess.run([sys.executable, 'setup_deps.py'],
                   cwd=ROOT / 'lynx/third_party/weak-node-api', env=env, check=True)
    subprocess.run(['node', '--version'], env=env, check=True)
    subprocess.run(['cmake', '--version'], env=env, check=True)
    return env
