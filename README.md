# Electron Search

Framework for finding Electron-based applications on your host.

Currently supports:
- Windows
- macOS
- Linux

Additionally supports searching for [`nwjs`-based applications](https://nwjs.io), a pseudo-predecessor to Electron.

## Installation

```sh
python -m pip install electron-search
```


## Usage

```py
>>> from electron_search import Search
>>> search = Search()
>>> search.apps
['C:\\Users\\RIPEDA\\AppData\\Local\\1Password\\app\\8\\1Password.exe', 'C:\\Users\\RIPEDA\\AppData\\Local\\Discord\\app-1.0.9030\\Discord.exe']
```

### `Search()` Parameters

```py
search_paths (str | list[str]): The path(s) to search for Electron-based applications.
platform                 (str): The platform to search for Electron-based applications on. Defaults to sys.platform.
variant                  (str): The Electron-based application variant to search for. Defaults to "electron", supports "nwjs".
```
