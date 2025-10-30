.PHONY: help install clean clean-build build-iso build-iso-x64 build-iso-arm64 build-iso-all deb test lint docker-build docker-iso-x64 docker-iso-arm64 docker-iso-all

ARCH ?= amd64

help:
	@echo "====================================================="
	@echo " Eloquence GNU/Linux Build System (Dual-Architecture)"
	@echo "====================================================="
	@echo "Available make commands:"
	@echo "  make build-iso         - Build Live ISO for target ARCH (default: amd64)"
	@echo "  make build-iso-x64     - Build Live ISO for x86_64 / amd64"
	@echo "  make build-iso-arm64   - Build Live ISO for ARM64 / aarch64"
	@echo "  make build-iso-all     - Build both x86_64 and ARM64 Live ISOs sequentially"
	@echo "  make docker-build      - Build Docker container image for build environment"
	@echo "  make docker-iso-x64    - Build x86_64 ISO inside Docker container"
	@echo "  make docker-iso-arm64  - Build ARM64 ISO inside Docker container"
	@echo "  make docker-iso-all    - Build both x86_64 and ARM64 ISOs inside Docker"
	@echo "  make deb               - Build native Debian package (.deb) using dpkg-buildpackage"
	@echo "  make test              - Run syntax and configuration audit"
	@echo "  make lint              - Run shell script syntax linters"
	@echo "  make clean             - Clean build artifacts, venv, pycache, and chroot locks"
	@echo "  make clean-build       - Purge live-build chroot and cache locks (lb clean --purge)"
	@echo "====================================================="

build-iso:
	@echo "Starting ISO generation for architecture: $(ARCH)..."
	chmod +x scripts/build.sh
	./scripts/build.sh $(ARCH)

build-iso-x64:
	$(MAKE) build-iso ARCH=amd64

build-iso-arm64:
	$(MAKE) build-iso ARCH=arm64

build-iso-all:
	@echo "====================================================="
	@echo "===> [1/2] Building x86_64 (amd64) Live ISO..."
	@echo "====================================================="
	$(MAKE) clean-build
	$(MAKE) build-iso-x64
	@echo "====================================================="
	@echo "===> [2/2] Building ARM64 (aarch64) Live ISO..."
	@echo "====================================================="
	$(MAKE) clean-build
	$(MAKE) build-iso-arm64
	@echo "====================================================="
	@echo "[SUCCESS] Both x86_64 and ARM64 ISOs generated in build_output/!"
	@echo "====================================================="

docker-build:
	@echo "===> Building Docker container image (eloquence-builder:latest)..."
	docker build -t eloquence-builder:latest .

docker-iso-x64: docker-build
	@echo "===> Building x86_64 ISO inside Docker container..."
	docker run --privileged --rm -v $(shell pwd):/build eloquence-builder:latest "make build-iso-x64"

docker-iso-arm64: docker-build
	@echo "===> Building ARM64 ISO inside Docker container..."
	docker run --privileged --rm -v $(shell pwd):/build eloquence-builder:latest "make build-iso-arm64"

docker-iso-all: docker-build
	@echo "===> Building both x86_64 and ARM64 ISOs inside Docker container..."
	docker run --privileged --rm -v $(shell pwd):/build eloquence-builder:latest "make build-iso-all"

deb:
	@echo "Building native Debian package (.deb)..."
	dpkg-buildpackage -us -uc -b

test: lint
	@echo "[SUCCESS] All configuration and shell validation checks passed."

lint:
	@echo "Running shell script syntax check..."
	bash -n scripts/build.sh
	bash -n scripts/verify-iso.sh
	sh -n auto/config.sh
	sh -n auto/build.sh
	sh -n config/hooks/normal/099-eloquence-branding.chroot
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
