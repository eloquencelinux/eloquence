FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install all live-build requirements, kernel tools, QEMU static, and build toolchain
RUN apt-get update && apt-get install -y --no-install-recommends \
    live-build \
    debootstrap \
    squashfs-tools \
    xorriso \
    cpio \
    syslinux-utils \
    isolinux \
    grub-pc-bin \
    grub-efi-amd64-bin \
    grub-efi-arm64-bin \
    qemu-user-static \
    binfmt-support \
    python3 \
    python3-pip \
    python3-setuptools \
    git \
    make \
    bash \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY . /build

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["make build-iso-x64"]
