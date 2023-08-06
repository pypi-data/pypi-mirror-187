# 🩺 `block-scopes`
_Block scoping in Python!_

[![PyPI - Version](https://img.shields.io/pypi/v/block-scopes.svg)](https://pypi.org/project/block-scopes)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/block-scopes.svg)](https://pypi.org/project/block-scopes)

-----

**Table of Contents**

- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Usage

```python
from scopes import scope

before = "I'll be kept!"

with scope("keep_me", "keep_me_too"):
    keep_me = "Keep me!"
    lose_me = "Not me!"

    keep_me_too = "Also... me!"

assert "before" in locals()
assert "keep_me" in locals()
assert "keep_me_too" in locals()

assert "lose_me" not in locals()
```

## Installation

```console
pip install block-scopes
```

## License

`block-scopes` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
