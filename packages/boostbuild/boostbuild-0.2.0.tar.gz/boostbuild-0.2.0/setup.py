# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boostbuild', 'boostbuild.cmd']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0', 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['boost = boostbuild.main:main']}

setup_kwargs = {
    'name': 'boostbuild',
    'version': '0.2.0',
    'description': 'Boost is a simple build system that aims to create an interface for shell command substitution across different operative systems.',
    'long_description': '# Boost\nBoost is a simple build system that aims to create an interface for shell command substitution across different operative systems while keeping a simple interface. Boost tries to centralize build steps on different development environments.\n\nBoost adds a simple way to add custom commands with different behaviours for different platforms.\n\nWarning: Boost follows semantic versioning and we are currently on 0.Y.Z version which means that the API will probably be modified on early stages and that boost does not have all the validations that we want to implement before the 1.0.0 release.\n\n## Commands\nA command is a group of functions which determines the behaviour of an action on different environments. A command needs to implement these functions:\n- `generic_exec(args: List[str]) -> dict`: function if the code is the same across multiple platforms or\n- `win_exec(args: List[str]) -> dict`: for Windows commands.\n- `posix_exec(args: List[str]) -> dict`: for Posix commands.\n\nCurrently, commands files under cmd package which implement above deffined functions can be automatically used by its file name. For example, `boost.cmd.delete` can be used inside any `boost.yaml` `boost` targets by using the keyword `delete`.\n\n## Using Boost\nTo use Boost, first, create a `boost.yaml` file in your project directory. This is an example of a simple boost file.\n\n```yaml\nvars:\n  - file: example.txt\n  - current_dir: pwd\n    attributes: exec\n  - im_a_password: SUPER SECRET PASSWORD\n    attributes: secret\nboost:\n  dev: |\n    delete {file}\n    echo {current_dir}\n```\n- `vars`: List of variable objects that a boost target needs to be executed. A variable needs a key that will act as the variable name, and a value for the variable value. Variables can also have an optional key called `attributes` to modify its behavour.\n- `boost`: key-value pairs named boost targets. Target key will be used to call that specific target. Key value contains a list of commands separated by `\\n` (yaml multi line strings) that will be triggered when calling a specific target.\nIf a value needs to use a variable, use `{VARIABLE KEY}` where `VARIABLE NAME` is the variable key decalred on the `vars` section. To call a boost target, run `boost <TARGET>`. If no boost target was specified, boost will use the first defined target. If a target only needs to run a single command, it can be written like a one line string on yaml:\n\n  ```yaml\n  boost:\n    dev: echo I am a single command!!!\n  ```\n\n## Variables\n\nVariables are a list of objects. Each object should have a key that will represent the variable name, and a value for its variable value. For example:\n\n```yaml\nvars:\n  - variable_name: variable_value\n```\n\nOnly variables required by the target specified will be loaded. So, in the following example, only the variable `foo` and `bar` will be loaded by the execution of `boost dev`:\n\n```yaml\nvars:\n  foo: \'{bar}\'\n  bar: im a value\n  example: im not going to be loaded if the target build is not called :(\nboost:\n  dev: echo {foo}\n  build: |\n    echo {example}\n    echo {bar}\n```\n\nNote that `bar` is loaded because it is required by `foo` which is the one beeing required by the target `dev`.\n\nAs you saw in the above example, variables can reference other variables with the same sytax `{VARIABLE}` but it is not allowed to reference themselves.\n\nVariables are loaded when boost is initialized and currently their values cannot be modified. A new variable attribute to change this behaviour will be implemented to allow the re-execution of variables.\n\n### Attributes\nVariables can also have an optional key called `attributes`. Attributes modifies variable behaviour. The value of this key is a comma-separated list of attributes.\n\nList of available attributes:\n  - `secret`: Avoid a value of a variable to be printed when boost echoes each boost target command. The value will be replaced by `*****`. Note that for the moment this is not applied to the output of commands. Example:\n    ```yaml\n    vars:\n      - password: super secret password\n        attributes: secret\n    ```\n  - `exec`: Handle variable value as a command that needs to be executed to get the actual variable value. Example:\n    ```yaml\n    vars:\n      - current_dir: pwd   # translated to the output of "pwd" when used\n        attributes: exec\n    ```\n\n## Developing boost\nRequirements:\n  - poetry\n\nRun `poetry install`. Whit the previous command, you can run `poetry run boost` to test boost or just `boost` if you run `poetry shell`. Boost command does automatically trigger `boostbuild.main:main` function.\nMore information about Poetry can be found at [their official documentation](https://python-poetry.org/docs/).\n',
    'author': 'David Lopez',
    'author_email': 'davidlopez.hellin@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
