# CGM Smart Lights

CGM Smart Lights is a Python application for synchronizing Hue lights with Dexcom CGM

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

### Pre-Commit

To enforce common rules, pre-commit hooks are used

<https://pre-commit.com/>

```bash
pre-commit install
pre-commit run --all-files # To run without a commit
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
