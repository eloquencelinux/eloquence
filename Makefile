.PHONY: help install clean build-iso

help:
	@echo "Eloquence OS / Elo-Suite Build System"
	@echo "Available commands:"
	@echo "  make install     - Install Elquence Suite python packages in editable mode"
	@echo "  make build-iso   - Trigger the live-build ISO generation script"
	@echo "  make clean       - Remove temporary build artifacts and cache"

install:
	pip install --upgrade pip
	pip install -e .

build-iso:
	@echo "Starting ISO generation..."
	chmod +x scripts/build-iso.sh
	./scripts/build-iso.sh

clean:
	rm -rf build_output/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} +
