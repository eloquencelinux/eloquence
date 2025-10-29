# Contributing to Eloquence GNU/Linux

Thank you for your interest in contributing to **Eloquence GNU/Linux**! We welcome bug reports, feature requests, documentation improvements, and code contributions.

---

## 🛠️ Development Setup

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/eloquence.git
   cd eloquence
   ```

2. **Install Dependencies in Editable Mode**:
   ```bash
   make install
   ```

3. **Run Code Validation**:
   Before submitting code, ensure all Python tests and shell linters pass:
   ```bash
   make test
   make lint
   ```

---

## 🚀 Building Live ISOs

Eloquence GNU/Linux supports dual-architecture builds (`amd64` and `arm64`):

```bash
# Build x86_64 / amd64 ISO
make build-iso-x64

# Build ARM64 / aarch64 ISO
make build-iso-arm64
```

---

## 📝 Pull Request Guidelines

- Ensure your code adheres to Python PEP 8 style standards.
- Keep commits atomic with descriptive commit messages (following Conventional Commits e.g. `feat:`, `fix:`, `docs:`).
- Verify that both `make test` and `make lint` complete without errors.

---
*Last updated: 29 October 2025*
