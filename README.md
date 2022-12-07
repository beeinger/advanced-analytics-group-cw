### 1. Make sure you have python 3.9 installed

### 2. Install poetry https://python-poetry.org/

### 3. Run these commands:

```bash
poetry install
poetry run python main.py -b
```

### 4. Flags

`-v` or `--version` is for version

`-b` or `--benchmark` is for benchmarking`

**Examples:**

The default version is 2, so it doesn't need the `-v` flag, but if you want to you can run it like that as well

```
poetry run python main.py -v 2 -b
```

If you want to run version 3, you can do so by running

```
poetry run python main.py -v 3 -b
```

If you don't want benchmarking, you can remove the `-b` flag.

```
poetry run python main.py
```
