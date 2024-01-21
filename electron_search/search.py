"""
search.py: Search for Electron-based applications
"""

import os
import sys
from pathlib import Path


class Search:
    """
    Search for Electron-based applications
    """

    def __init__(self, search_path: list = None):
        """
        Initialize the ElectronSearch class.

        Parameters:
            search_path (str | list[str]): The path(s) to search for Electron-based applications.
        """
        self._platform = sys.platform

        self.search_path = search_path
        if isinstance(self.search_path, str):
            self.search_path = [self.search_path]

        if self.search_path is None:
            self.search_path = self._default_search_path()


    def _default_search_path(self) -> list:
        """
        Get the default search path for the current platform.
        """
        if self._platform  == "darwin":
            return ["/Applications"]
        if self._platform  == "win32":
            return ["C:\\Program Files", "C:\\Program Files (x86)", f"C:\\Users\\{os.getlogin()}\\AppData\\Local"]
        if self._platform  == "linux":
            return ["/usr/share", "/usr/bin", "/opt"]
        raise NotImplementedError(f"Platform {self._platform } is not supported.")


    def _search_function(self) -> str:
        """
        Get the search function for the current platform.
        """
        if self._platform  == "darwin":
            return self._macos_search
        if self._platform  == "win32":
            return self._windows_search
        if self._platform  == "linux":
            return self._linux_search
        raise NotImplementedError(f"Platform {self._platform } is not supported.")


    def _macos_search(self, path: str) -> list:
        """
        Search for Electron-based applications on macOS.
        """
        apps = []
        for app in Path(path).glob("**/*.app"):
            if not app.is_dir():
                continue
            if not Path(app, "Contents", "Frameworks", "Electron Framework.framework").resolve().exists():
                continue
            apps.append(str(app))

        return apps


    def _windows_search(self, path: str) -> list:
        """
        Search for Electron-based applications on Windows.
        """
        apps = []
        for bin in Path(path).glob("**/v8_context_snapshot.bin"):
            if not bin.is_file():
                continue

            # Now need to resolve the electron executable
            for executable in Path(bin).parent.glob("*.exe"):
                if not executable.is_file():
                    continue
                if b"Electron/" not in executable.read_bytes():
                    continue
                if b"v8_context_snapshot.bin" not in executable.read_bytes():
                    continue

                apps.append(str(executable))

        return apps


    def _linux_search(self, path: str) -> list:
        """
        Search for Electron-based applications on Linux.
        """
        apps = []
        for bin in Path(path).glob("**/v8_context_snapshot.bin"):
            if not bin.is_file():
                continue

            # Now need to resolve the electron executable
            for executable in Path(bin).parent.glob("*"):
                if not executable.is_file():
                    continue
                if b"Electron/" not in executable.read_bytes():
                    continue
                if b"v8_context_snapshot.bin" not in executable.read_bytes():
                    continue

                apps.append(str(executable))

        return apps


    def apps(self) -> list:
        """
        Search for Electron-based applications.

        Returns:
            A list of paths to Electron-based applications.
        """
        apps = []
        for path in self.search_path:
            apps.extend(self._search_function()(path))

        return apps
