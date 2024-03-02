# APT Free Space Checker
An python script, implemented as an apt pre-check trigger, for automating disk space checks before APT package installations

## Overview
This repository contains a Python script for automating disk space checks before APT package installations. 
The APT Free Space Checker ensures that sufficient disk space is available on the system before initiating APT package installations. It consists of:
An Ansible playbook is also provided to ease installation.

- An Ansible playbook (`apt-free-space-trigger.yaml`) that configures APT to perform disk space checks before installing packages.
- A Python script (`apt-check-space-trigger.py`) that checks the available disk space on specified partitions and prints warning or error messages if the free space falls below specified thresholds. The script returns an error result of 1 if space is under the defined warning or error limits.

## Why It's Necessary

Running out of disk space during a package installation can lead to a messy system state, incomplete installations, or even system failures. By checking disk space availability before initiating package installations, the APT Free Space Checker helps prevent these issues and ensures smooth system operation.

## Ansible Playbook (`apt-free-space-trigger.yaml`)

The Ansible playbook `apt-free-space-trigger.yaml` performs the following tasks:

1. Creates the necessary directory structure for APT configuration
2. Adds configuration to APT to perform disk space checks before package installations (`/etc/apt/apt.conf.d/00-check-free-space`)
3. Specifies warning and error thresholds for disk space checks.

## Python Script (`apt-check-space-trigger.py`)

The Python script `apt-check-space-trigger.py` is responsible for performing disk space checks on specified partitions. It takes the following arguments:

- `-e` or `--error-at-mb`: Specifies the amount of free space in megabytes to generate an error message.
- `-w` or `--warning`: Specifies the minimum amount of free space in megabytes before generating a warning message.

Example usage:

```
check_space.py -e 2000 -w 2500
```

## Requirements

- Ansible
- Python 3

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
