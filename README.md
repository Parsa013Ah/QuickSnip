# quicksnip

> A fast, terminal-based code snippet manager for developers

[![PyPI](https://img.shields.io/pypi/v/quicksnip.svg)](https://pypi.org/project/quicksnip/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![demo](demo.gif)

## Why quicksnip?

Tired of searching through old projects for that one function you wrote? **quicksnip** lets you save, search, and copy code snippets right from your terminal.

## Features

- **Fast** - Search and copy snippets in milliseconds
- **Fuzzy search** - Find snippets by name, description, or code
- **Tags & languages** - Organize your snippets
- **Clipboard integration** - Copy with one command
- **Import/Export** - Backup and share your snippets
- **Syntax highlighting** - Beautiful code display

## Installation

```bash
pip install quicksnip
```

## Usage

Both `snip` and `quicksnip` commands work:

### Add a snippet
```bash
snip add my-function -d "Quick sort implementation" -l python -t "algorithms,sorting" -c "def quicksort(arr): ..."
```

### Search snippets
```bash
snip search "sort"
snip search -l python
snip search -t algorithms
```

### Copy to clipboard
```bash
snip copy my-function
```

### List all snippets
```bash
snip list
snip list -l python
```

### Show a snippet
```bash
snip show my-function
```

### Export/Import
```bash
snip export backup.json
snip import backup.json
```

## License

MIT
