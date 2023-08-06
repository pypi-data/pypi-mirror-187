## slack-bolt-router

[![Python Versions](https://badgen.net/pypi/python/slack-bolt-router)](https://pypi.org/project/slack-bolt-router/)
[![Slack-Bolt Version](https://badgen.net/badge/icon/%5E1.10.0?icon=slack&label=slack-bolt)]()
[![Release](https://badgen.net/github/release/dmytrohoi/slack-bolt-router)](https://github.com/dmytrohoi/slack-bolt-router/releases)
[![License](https://badgen.net/github/license/dmytrohoi/slack-bolt-router)](https://github.com/dmytrohoi/slack-bolt-router/blob/master/LICENSE)

### Description

The slack-bolt-router package it is a helper utility that can collect and add
routes for the Slack Application.

Current compatible slack-bolt version is __1.10.0__.

_NOTE: This package may be affected by major updates to the Slack-bolt library,
and may not contain additional routes from a future release._

### Usage

Install from pip:

``` sh
python3 -m pip install slack-bolt-router
```

Import router to file with your handler functions:

```python
from slack_bolt_router import Router
```

Start to use routers in your bot application:
```python
router = Router()

@router.register(type="view")
def example_submit(ack):
    ack()

router.apply_to(app)
```

__[Examples of usage](https://github.com/dmytrohoi/slack-bolt-router/blob/master/examples)__

### Contribution

1. Clone repo
2. Run `poetry install`
3. Make some changes and commit to new branch
4. Create pull request and add some information about changes in PR
5. Add project author to PR Reviewers

### Author

_You can sponsorship this project by links in github repo._

Author personal website: https://hoid.dev

(c) Dmytro Hoi <code@dmytrohoi.com>, 2021 | MIT License
