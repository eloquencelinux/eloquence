.PHONY: help install clean clean-build build-iso build-iso-x64 build-iso-arm64 deb test lint

ARCH ?= amd64

help:
	@echo "====================================================="
	@echo " Eloquence OS / Eloquence Suite Build System"
	@echo "====================================================="
	@echo "Available make commands:"
	@echo "  make install         - Install Eloquence Suite (virtualenv or PEP 668 system mode)"
	@echo "  make build-iso       - Build Live ISO for target ARCH (default: amd64)"
	@echo "  make build-iso-x64   - Build Live ISO for x86_64 / amd64"
	@echo "  make build-iso-arm64 - Build Live ISO for ARM64 / aarch64"
	@echo "  make deb             - Build native Debian package (.deb) using dpkg-buildpackage"
	@echo "  make test            - Run Python syntax checks for Eloquence Suite"
	@echo "  make lint            - Run shell script syntax linters"
	@echo "  make clean           - Clean build artifacts, venv, pycache, and chroot locks"
	@echo "  make clean-build     - Purge live-build chroot and cache locks (lb clean --purge)"
	@echo "====================================================="

install:
	@echo "===> Installing Eloquence Suite..."
	@if [ -d ".venv" ] || python3 -m venv .venv 2>/dev/null; then \
		echo "[INFO] Using virtual environment (.venv)"; \
		.venv/bin/pip install --upgrade pip && \
		.venv/bin/pip install -e . ; \
	else \
		echo "[INFO] Virtual environment creation unavailable, falling back to --break-system-packages"; \
		pip install --upgrade pip --break-system-packages 2>/dev/null || true ; \
		pip install -e . --break-system-packages ; \
	fi

build-iso:
	@echo "Starting ISO generation for architecture: $(ARCH)..."
	chmod +x scripts/build.sh
	./scripts/build.sh $(ARCH)

build-iso-x64:
	$(MAKE) build-iso ARCH=amd64

build-iso-arm64:
	$(MAKE) build-iso ARCH=arm64

deb:
	@echo "Building native Debian package (.deb)..."
	dpkg-buildpackage -us -uc -b

test:
	@echo "Running Python syntax validation..."
	python3 -m py_compile elovirt/main.py elovirt/qemu_wrapper.py
	python3 -m py_compile elofind/main.py
	python3 -m py_compile elooffice/main.py
	python3 -m py_compile eloapps/main.py
	@echo "[SUCCESS] All Python modules compiled cleanly."

lint:
	@echo "Running shell script syntax check..."
	bash -n bin/elo.sh
	bash -n scripts/build.sh
	bash -n scripts/verify-iso.sh
	sh -n auto/config.sh
	sh -n auto/build.sh
	@echo "[SUCCESS] All shell scripts passed syntax check."

clean-build:
	@echo "Purging live-build environment and locks..."
	@if command -v lb >/dev/null 2>&1; then \
		lb clean --purge 2>/dev/null || true; \
	fi
	rm -rf .build/ chroot/ binary/ binary.iso binary.hybrid.iso live-image-*.iso build.log

clean: clean-build
	rm -rf build_output/
	rm -rf *.egg-info/
	rm -rf dist/ build/ .venv/
	find . -type d -name "__pycache__" -exec rm -rf {} +
