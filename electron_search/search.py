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

    def __init__(self, search_paths: list = None, platform: str = sys.platform, variant = "electron"):
        """
        Initialize the ElectronSearch class.

        Parameters:
            search_path (str | list[str]): The path(s) to search for Electron-based applications.
            platform (str): The platform to search for Electron-based applications on. Defaults to sys.platform.
            variant (str): The Electron-based application variant to search for. Defaults to "electron", supports "nwjs".
        """
        self._variant  = variant
        self._platform = platform

        self._frameworks = self._search_frameworks(variant=self._variant)
        self._strings    = self._search_strings(variant=self._variant)

        self.search_paths = search_paths
        if isinstance(self.search_paths, str):
            self.search_paths = [self.search_paths]

        if self.search_paths is None:
            self.search_paths = self._default_search_path()


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


    def _search_strings(self, variant: str = "electron") -> list:
        """
        Get the search strings executable type
        """
        if variant == "electron":
            return [b"Electron/", b"v8_context_snapshot.bin"]
        if variant == "nwjs":
            if self._platform == "win32":
                return [b"nw.exe", b"nw_elf.dll"]
            if self._platform == "linux":
                return [b".js.map", b"libnw.so"]
            if self._platform == "darwin":
                return [] # String search not used for detection on macOS
        raise NotImplementedError(f"Variant {variant} is not supported.")


    def _search_frameworks(self, variant: str = "electron") -> str:
        """
        Get the search framework for macOS
        """
        if variant == "electron":
            return ["Electron Framework.framework"]
        if variant == "nwjs":
            # https://github.com/nwjs/nw.js/commit/8d45cf4ec8ba56caf70ce7222f491ae431936c4f
            return ["nwjs Framework.framework", "node-webkit Framework.framework"]
        raise NotImplementedError(f"Variant {variant} is not supported.")


    def _macos_search(self, path: str) -> list:
        """
        Search for Electron-based applications on macOS.
        """
        apps = []

        if path.endswith(".app"):
            for framework in self._frameworks:
                try:
                    if Path(path, "Contents", "Frameworks", framework).exists():
                        apps.append(path)
                        break
                except PermissionError:
                    continue

        for app in Path(path).glob("**/*.app"):
            try:
                if not app.is_dir():
                    continue
            except OSError:
                continue
            for framework in self._frameworks:
                # Reference: https://github.com/ripeda/Lectricus/issues/1
                try:
                    if Path(app, "Contents", "Frameworks", framework).exists():
                        apps.append(str(app))
                        break
                except PermissionError:
                    continue

        return apps


    def _windows_search(self, path: str) -> list:
        """
        Search for Electron-based applications on Windows.
        """
        return self._generic_search(path, secondary_glob="*.exe")


    def _linux_search(self, path: str) -> list:
        """
        Search for Electron-based applications on Linux.
        """
        return self._generic_search(path, secondary_glob="*")


    def _generic_search(self, path: str, main_glob: str = "**/v8_context_snapshot.bin", secondary_glob: str = ".exe") -> list:
        """
        Search for Electron-based applications based on File structure.
        """
        apps = []

        try:
            if Path(path).is_file():
                bytes = Path(path).read_bytes()
                if not all(string in bytes for string in self._strings):
                    return apps

                apps.append(str(path))
                return apps
        except OSError:
            pass

        for bin in Path(path).glob(main_glob):
            try:
                if not bin.is_file():
                    continue
            except OSError:
                continue

            # Now need to resolve the electron executable
            for executable in Path(bin).parent.glob(secondary_glob):
                try:
                    if not executable.is_file():
                        continue
                except OSError:
                    continue

                bytes = executable.read_bytes()
                if not all(string in bytes for string in self._strings):
                    continue

                apps.append(str(executable))

        return apps


    @property
    def apps(self) -> list:
        """
        Search for Electron-based applications.

        Returns:
            A list of paths to Electron-based applications.
        """
        apps = []
        for path in self.search_paths:
            apps.extend(self._search_function()(path))

        return apps
