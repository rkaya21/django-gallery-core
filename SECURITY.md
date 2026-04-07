# Security Policy

## Supported Versions

This package is currently in an early `0.x` phase. Security fixes, when needed, should target the latest version first.

## Reporting a Vulnerability

Please do not open a public issue for suspected security vulnerabilities.

Instead, report privately with:
- a description of the issue
- affected version or commit
- reproduction steps
- impact assessment if known

If this repository is published publicly, use the repository security advisory flow or contact the maintainer privately.

## Response Expectations

The goal is to:
- acknowledge receipt promptly
- validate the report
- prepare a fix if confirmed
- publish the minimum necessary disclosure after a fix is available

## Package-Specific Concerns

When reviewing or reporting security issues in `django-gallery-core`, pay special attention to:
- file upload handling
- path generation and storage assumptions
- serializer validation for gallery mutation flows
- unintended exposure of internal media URLs
- admin-side misuse of bulk image operations

## Dependency Hygiene

Consumers are responsible for keeping Django, DRF, and their storage backend dependencies updated. This package intentionally keeps its dependency surface small to reduce risk.
