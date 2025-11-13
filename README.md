# Molecule Lima Driver

[![PyPI version](https://img.shields.io/pypi/v/molecule-lima.svg)](https://pypi.org/project/molecule-lima/)
[![Python versions](https://img.shields.io/pypi/pyversions/molecule-lima.svg)](https://pypi.org/project/molecule-lima/)
[![License](https://img.shields.io/github/license/filatof/molecule-lima.svg)](https://github.com/filatof/molecule-lima/blob/main/LICENSE)

A [Molecule](https://ansible.readthedocs.io/projects/molecule/) driver for [Lima VM](https://lima-vm.io/), enabling testing of Ansible roles on macOS (Apple Silicon) and Linux with native virtualization support.

## Features

- 🚀 **Native Apple Silicon Support** - Uses VZ framework for optimal performance on ARM Macs
- 🐧 **Cross-Platform** - Works on macOS (Apple Silicon/Intel) and Linux
- ⚡ **Fast** - Lightweight virtualization with minimal overhead
- 🔧 **Flexible** - Extensive configuration options for CPU, memory, disk, and networking
- 📦 **Cloud Images** - Support for Ubuntu, Debian, Rocky Linux, and other distributions
- 🎯 **Molecule Native** - Seamless integration with Molecule testing workflow

## Requirements

- **Operating System**: macOS (Apple Silicon/Intel) or Linux
- **Lima**: >= 0.17.0
- **Python**: >= 3.9
- **Ansible**: >= 2.12
- **Molecule**: >= 6.0.0

## Installation

### Install Lima

**macOS (Homebrew):**
```bash
brew install lima
```

**Linux:**
```bash
# Download the latest release
wget https://github.com/lima-vm/lima/releases/latest/download/lima-$(uname -m).tar.gz
tar -xzf lima-$(uname -m).tar.gz
sudo install -m 755 bin/limactl /usr/local/bin/
```

### Install Molecule Lima Driver
```bash
pip install molecule-lima
```

**Development Installation:**
```bash
git clone https://github.com/filatof/molecule-lima.git
cd molecule-lima
pip install -e .[dev]
```

## Quick Start

### Initialize a New Scenario
```bash
molecule init scenario <scenario-name>
```

### Basic Configuration

Create or update `molecule/default/molecule.yml`:
```yaml
driver:
  name: molecule-lima
  ssh_timeout: 180

platforms:
  - name: ubuntu-22-04
    image: "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img"
    arch: aarch64
    vm_type: vz  # vz for Apple Silicon, qemu for Intel/Linux
    cpus: 2
    memory: 2GiB
    disk: 20GiB

provisioner:
  name: ansible
  config_options:
    defaults:
      callbacks_enabled: profile_tasks,timer
      stdout_callback: yaml
      host_key_checking: false

verifier:
  name: ansible
```

### Run Tests
```bash
# Create instances
molecule create

# Run converge
molecule converge

# Run verification
molecule verify

# Run idempotence
molecule idempotence

# Full test cycle
molecule test
```

## Configuration Options

### Platform Parameters

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `name` | Instance name | - | Yes |
| `image` | OS image URL | - | Yes |
| `arch` | Architecture (`aarch64`, `x86_64`) | `aarch64` | No |
| `vm_type` | VM type (`vz`, `qemu`) | `vz` | No |
| `cpus` | Number of CPUs | `2` | No |
| `memory` | RAM amount | `2GiB` | No |
| `disk` | Disk size | `20GiB` | No |
| `python_interpreter` | Python path | `/usr/bin/python3` | No |
| `provision_script` | Provisioning bash script | - | No |
| `mounts` | Additional mount points | - | No |

### VM Type Selection

- **`vz`** (Virtualization.framework) - Recommended for Apple Silicon Macs (faster, native)
- **`qemu`** - For Intel Macs and Linux systems

### Advanced Configuration Example
```yaml
driver:
  name: molecule-lima
  ssh_timeout: 240

platforms:
  # Docker host for container testing
  - name: docker-host
    image: "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img"
    arch: aarch64
    vm_type: vz
    cpus: 4
    memory: 4GiB
    disk: 30GiB
    python_interpreter: /usr/bin/python3
    provision_script: |
      apt-get update
      apt-get install -y docker.io python3-pip
      systemctl enable --now docker
      usermod -aG docker $USER
    mounts:
      - location: "/Users/username/project"
        writable: true

  # Multi-platform testing
  - name: debian-12
    image: "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-arm64.qcow2"
    arch: aarch64
    cpus: 2
    memory: 2GiB

  - name: rocky-9
    image: "https://download.rockylinux.org/pub/rocky/9/images/aarch64/Rocky-9-GenericCloud-Base.latest.aarch64.qcow2"
    arch: aarch64
    cpus: 2
    memory: 2GiB
```

## Supported OS Images

### Ubuntu ARM64

- **22.04 (Jammy)**: `https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img`
- **20.04 (Focal)**: `https://cloud-images.ubuntu.com/releases/20.04/release/ubuntu-20.04-server-cloudimg-arm64.img`

### Debian ARM64

- **12 (Bookworm)**: `https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-arm64.qcow2`
- **11 (Bullseye)**: `https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-generic-arm64.qcow2`

### Rocky Linux ARM64

- **9**: `https://download.rockylinux.org/pub/rocky/9/images/aarch64/Rocky-9-GenericCloud-Base.latest.aarch64.qcow2`

> **Note**: For Intel/x86_64 systems, use corresponding x86_64 images by replacing `arm64`/`aarch64` with `amd64`/`x86_64` in URLs.

## Use Cases

### Testing Docker-Based Roles
```yaml
platforms:
  - name: docker-test
    image: "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img"
    cpus: 4
    memory: 4GiB
    provision_script: |
      curl -fsSL https://get.docker.com | sh
      systemctl start docker
```

### Multi-Distribution Testing
```yaml
platforms:
  - name: ubuntu-latest
    image: "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img"
  
  - name: debian-stable
    image: "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-arm64.qcow2"
  
  - name: rocky-latest
    image: "https://download.rockylinux.org/pub/rocky/9/images/aarch64/Rocky-9-GenericCloud-Base.latest.aarch64.qcow2"
```

## Troubleshooting

### SSH Connection Timeout

Increase `ssh_timeout` in driver configuration:
```yaml
driver:
  name: molecule-lima
  ssh_timeout: 300  # 5 minutes
```

### Lima Instance Not Starting

Check Lima status:
```bash
limactl list
limactl validate /path/to/lima-config.yaml
```

### Image Download Issues

Verify image URL is accessible:
```bash
curl -I <image-url>
```

### Performance on Apple Silicon

Ensure you're using `vm_type: vz` for best performance:
```yaml
platforms:
  - name: instance
    vm_type: vz  # Native Apple Silicon virtualization
```

## License

MIT License - see [LICENSE](LICENSE) file for details.