# Molecule Lima Driver

Драйвер Lima для Molecule, позволяющий тестировать Ansible роли на macOS Apple Silicon и Linux.

## Установка

```bash
pip install molecule-lima
```

Или для разработки:

```bash
git clone https://github.com/yourusername/molecule-lima.git
cd molecule-lima
pip install -e .
```

## Требования

- macOS (Apple Silicon) или Linux
- Lima >= 0.17.0
- Ansible >= 2.12
- Molecule >= 6.0.0

## Установка Lima

### macOS
```bash
brew install lima
```

### Linux
```bash
# Скачать последнюю версию с GitHub
wget https://github.com/lima-vm/lima/releases/latest/download/lima-$(uname -m).tar.gz
tar -xzf lima-$(uname -m).tar.gz
sudo install -m 755 bin/limactl /usr/local/bin/
```

## Использование

### Создание нового сценария

```bash
molecule init scenario --driver-name lima
```

### Конфигурация платформ

Пример `molecule.yml`:

```yaml
driver:
  name: lima
  ssh_timeout: 180

platforms:
  # Ubuntu ARM64
  - name: ubuntu-22-04
    image: "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img"
    arch: aarch64
    vm_type: vz  # vz для Apple Silicon, qemu для Intel/Linux
    cpus: 4
    memory: 4GiB
    disk: 30GiB
    python_interpreter: /usr/bin/python3
    provision_script: |
      apt-get install -y docker.io
    mounts:
      - location: "/Users/username/project"
        writable: true

  # Debian ARM64
  - name: debian-12
    image: "https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-arm64.qcow2"
    arch: aarch64
    cpus: 2
    memory: 2GiB
    disk: 20GiB

  # Rocky Linux ARM64
  - name: rocky-9
    image: "https://download.rockylinux.org/pub/rocky/9/images/aarch64/Rocky-9-GenericCloud-Base.latest.aarch64.qcow2"
    arch: aarch64
    cpus: 2
    memory: 2GiB
    disk: 20GiB
```

### Параметры платформы

| Параметр | Описание | По умолчанию |
|----------|----------|--------------|
| `name` | Имя инстанса | обязательно |
| `image` | URL образа ОС | обязательно |
| `arch` | Архитектура (aarch64, x86_64) | aarch64 |
| `vm_type` | Тип VM (vz, qemu) | vz |
| `cpus` | Количество CPU | 2 |
| `memory` | Объем RAM | 2GiB |
| `disk` | Размер диска | 20GiB |
| `python_interpreter` | Путь к Python | /usr/bin/python3 |
| `provision_script` | Bash-скрипт для провизионинга | - |
| `mounts` | Дополнительные mount points | - |

### Доступные образы

#### Ubuntu
- 22.04 ARM64: `https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img`
- 20.04 ARM64: `https://cloud-images.ubuntu.com/releases/20.04/release/ubuntu-20.04-server-cloudimg-arm64.img`

#### Debian
- 12 (Bookworm) ARM64: `https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-generic-arm64.qcow2`
- 11 (Bullseye) ARM64: `https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-generic-arm64.qcow2`

#### Rocky Linux
- 9 ARM64: `https://download.rockylinux.org/pub/rocky/9/images/aarch64/Rocky-9-GenericCloud-Base.latest.aarch64.qcow2`

### Команды Molecule

```bash
# Создать инстансы
molecule create

# Запустить конвергенцию
molecule converge

# Проверить идемпотентность
molecule idempotence

# Запустить верификацию
molecule verify

# Уничтожить инстансы
molecule destroy

# Полный тест
molecule test
```

## Примеры

### Пример 1: Тестирование роли с Docker

```yaml
# molecule/default/molecule.yml
driver:
  name: lima

platforms:
  - name: docker-host
    image: "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-arm64.img"
    cpus: 4
    memory: 4GiB
    provision_script: |
      apt-get update
      apt-get install -y docker.io
      systemctl enable --now docker
      usermod -aG docker $USER

provisioner:
  name: ansible
  playbooks:
    converge: converge.yml