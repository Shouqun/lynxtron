import os
import runpy
import unittest
from unittest import mock

from lynxtron_tools import prepare_mac_cross_compile_env as setup


class MacCrossCompileTest(unittest.TestCase):
    def test_target_does_not_change_host_tools(self):
        with mock.patch.dict(os.environ, {'PATH': '/usr/bin'}, clear=True):
            arm = setup.target_environment('arm64')
            intel = setup.target_environment('x64')
        self.assertEqual(arm['PATH'], intel['PATH'])
        self.assertEqual(intel['npm_config_arch'], 'x64')
        self.assertEqual(intel['npm_config_platform'], 'darwin')
        self.assertEqual(intel['LYNXTRON_SKIP_DOWNLOAD'], '1')

    def test_preparation_uses_shared_setup_then_habitat(self):
        with mock.patch.object(setup.platform, 'system', return_value='Darwin'), \
                mock.patch.object(setup.subprocess, 'run') as run:
            env = setup.prepare('x64')
        calls = run.call_args_list
        self.assertIn('prepare_build_env.py', calls[1].args[0][1])
        self.assertEqual(calls[2].args[0][1:],
                         ['sync', '.', '--no-history', '--target', 'extension', '--target-only'])
        self.assertEqual(calls[3].args[0][1], 'setup_deps.py')
        self.assertEqual(calls[3].kwargs['cwd'], setup.ROOT / 'lynx/third_party/weak-node-api')
        for call in calls:
            self.assertEqual(call.kwargs['env'], env)
            self.assertTrue(call.kwargs['check'])

    def test_dependency_selection_separates_host_and_target(self):
        for target, suffix in [('x64', 'macosx64'), ('arm64', 'macosarm64')]:
            with mock.patch.dict(os.environ, {'npm_config_arch': target}), \
                    mock.patch('platform.system', return_value='Darwin'), \
                    mock.patch('platform.machine', return_value='arm64'):
                deps = runpy.run_path(str(setup.ROOT / 'src/dependencies/DEPS.extension'))['deps']
                tools = runpy.run_path(str(setup.ROOT / 'src/dependencies/DEPS.tools_shared'),
                                      init_globals={'root_dir': str(setup.ROOT / 'src')})['deps']
            self.assertIn(suffix, deps['../third_party/cef_binary']['url'])
            self.assertIn('macos-universal', deps['../buildtools/cmake']['url'])
            self.assertIn('darwin-arm64', tools['../buildtools/node']['url'])

    def test_unsupported_target_fails_before_setup(self):
        with self.assertRaises(ValueError):
            setup.target_environment('x86')


if __name__ == '__main__':
    unittest.main()
