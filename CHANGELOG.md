# Electron Search

## 1.4.0

## 1.3.0
- Iterate over app if provided directly
  - ex. `search_paths = ["/Applications/MyApp.app"]`
- Resolve Windows and Linux search regression from 1.2.0

## 1.2.0
- Add error handling for path permissions
- Publish `apps()` as property
- Allow platform override for OS detection
  - Suitable for situation where searching an external drive of a different OS
  - ex. macOS searching a Windows drive
- Rename `Search`'s `search_path` to `search_paths` for consistency

## 1.1.0
- Add Linux binary searching

## 1.0.0
- Initial release