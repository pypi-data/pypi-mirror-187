import os
import sys
from pathlib import Path
import unittest

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # visionai/visionai directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from util.general import WorkingDirectory, invoke_cmd

class TestInvoke(unittest.TestCase):
    @WorkingDirectory(ROOT)
    def test_invoke_scenario(self):
        output = invoke_cmd(f'python main.py scenario')
        assert 'Error' in output
        assert 'Missing command' in output

    @WorkingDirectory(ROOT)
    def test_invoke_scenario_help(self):
        output = invoke_cmd('python main.py scenario --help')
        assert 'Usage' in output
        assert 'Commands' in output
        assert 'add' in output
        assert 'list' in output
        assert 'remove' in output

    @WorkingDirectory(ROOT)
    def test_invoke_scenario_add_help(self):
        output = invoke_cmd('python main.py scenario add --help')
        assert 'Usage' in output
        assert 'scenario' in output
        assert 'add' in output
        assert '--camera' in output
        assert '--scenario' in output
        assert '--help' in output

    @WorkingDirectory(ROOT)
    def test_invoke_scenario_remove_help(self):
        output = invoke_cmd('python main.py scenario remove --help')
        assert 'Usage' in output
        assert 'scenario' in output
        assert 'remove' in output
        assert '--scenario' in output
        assert '--camera' in output
        assert '--help' in output

    @WorkingDirectory(ROOT)
    def test_invoke_scenario_list_help(self):
        output = invoke_cmd('python main.py scenario list --help')
        assert 'Usage' in output
        assert 'scenario' in output
        assert '--camera' in output
        assert '--help' in output

    @WorkingDirectory(ROOT)
    def test_invoke_scenario_add_remove(self):
        # cleanup (prior test failures)
        output = invoke_cmd('python main.py scenario remove --name TEST-999')

        # add camera
        output = invoke_cmd('python main.py camera add --name TEST-999 --uri youtube.com --description "Test camera"')
        assert 'Success' in output

        # add scenario
        output = invoke_cmd(f'python main.py scenario add --camera TEST-999 --scenario smoke-and-fire-detection')
        assert 'Scenario' in output
        assert 'smoke-and-fire-detection' in output
        assert 'added for camera' in output

        # list scenario
        output = invoke_cmd('python main.py scenario list --camera TEST-999')
        assert "Listing configured scenarios for" in output
        assert 'TEST-999' in output
        assert "'name': 'smoke-and-fire-detection'" in output

        # remove scenario
        output = invoke_cmd('python main.py scenario remove --camera TEST-999 --scenario smoke-and-fire-detection')
        assert 'Success' in output

        # list scenario
        output = invoke_cmd('python main.py scenario list  --camera TEST-999')
        assert "Listing configured scenarios for" in output
        assert 'TEST-999' in output
        assert "'name': 'smoke-and-fire-detection'" not in output

        # remove camera
        output = invoke_cmd('python main.py scenario remove --name TEST-999')




if __name__ == '__main__':
    unittest.main()
