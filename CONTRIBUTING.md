# Contributing

Thanks for contributing to `django-gallery-core`.

## Scope

This package should stay small and focused. Contributions are most useful when they improve one of these areas:

- ordered gallery model ergonomics
- serializer/admin reuse
- migration safety
- documentation and examples
- tests for real Django integration patterns

Please avoid turning the package into a full CMS or media platform.

## Development Principles

- prefer explicit Django patterns over heavy abstraction
- keep the public API small
- avoid app-specific assumptions in shared code
- document migration impact for model changes
- include tests for user-visible behavior

## Getting Started

1. Fork the repository.
2. Create a feature branch.
3. Make the smallest coherent change.
4. Update docs if the public API or setup flow changes.
5. Add or update tests when behavior changes.

## Before Opening a PR

Please check the following when relevant:

```bash
python3 -m compileall .
python3 -m build
```

If you are working inside a Django host project, also run focused tests for the integration surface that uses this package.

## Pull Request Guidelines

- keep PRs narrow and single-purpose
- explain why the change belongs in the package core
- call out any breaking change explicitly
- update `CHANGELOG.md` for release-relevant changes
- include README changes if installation, usage, or API shape changed

## Good First Contributions

- improve README examples
- tighten tests around upload syncing
- improve typing and docstrings
- reduce accidental coupling in helpers
- improve package metadata and release workflow
