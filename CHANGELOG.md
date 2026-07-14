# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-15

### Added

- `response['headers']['cb_status']` as the preferred Crawlbase status field.
- The library resolves status by preferring `cb_status` from the API response (header or JSON body), then falling back to `pc_status` when `cb_status` is absent.

### Deprecated

- `response['headers']['pc_status']` is deprecated but still supported temporarily for backward compatibility. It is populated with the same resolved value as `cb_status`.

### Migration

```python
# Deprecated (still works temporarily)
print(response['headers']['pc_status'])

# Preferred
print(response['headers']['cb_status'])
```

[1.1.0]: https://github.com/crawlbase-source/crawlbase-python/compare/v1.0.0...v1.1.0
