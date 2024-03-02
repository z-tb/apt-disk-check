#!/usr/bin/env python3

"""
This script checks the available disk space on specified partitions and prints warning or error messages
if the free space falls below specified thresholds. It is intended to be called by an apt pre-hook 
"""

import os
import argparse
import sys

# ANSI escape sequences for colorizing output
ERROR_COLOR = "\033[91m"  # Red
WARNING_COLOR = "\033[93m"  # Yellow
RESET_COLOR = "\033[0m"  # Reset color

ERROR = "ERROR"
WARNING = "WARNING"

def message(state, msg):
    """
    Print a colored message based on the state.

    Args:
        state (str): The state of the message (ERROR or WARNING).
        msg (str): The message to print.

    Returns:
        None
    """
    program_name = os.path.basename(sys.argv[0])
    if state == ERROR:
        print(ERROR_COLOR + f"{program_name} Error: {msg}" + RESET_COLOR)
    elif state == WARNING:
        print(WARNING_COLOR + f"{program_name} Warning: {msg}" + RESET_COLOR)

def check_free_space(partition, warning_mb, error_at_mb):
    """
    Check the available disk space on a partition and print a warning or error message if the free space is below
    the specified thresholds.

    Args:
        partition (str): The partition to check.
        warning_mb (int): The minimum amount of free space in megabytes before a warning is generated.
        error_at_mb (int): The amount of free space in megabytes to generate an error message.

    Returns:
        str: The state of the message (ERROR or WARNING).
    """
    try:
        stat = os.statvfs(partition)
        free_space = (stat.f_bavail * stat.f_frsize) / (1024 * 1024)  # Convert bytes to megabytes

        if free_space < error_at_mb:
            message(ERROR, f"Critical disk space on {partition}: {free_space:.2f} MB left")
            return ERROR
        elif free_space < warning_mb:
            message(WARNING, f"Low disk space on {partition}: {free_space:.2f} MB left")
            return WARNING
        else:
            return None
    except FileNotFoundError:
        message(ERROR, f"Partition {partition} not found")
        return ERROR
    except Exception as e:
        message(ERROR, str(e))
        return ERROR

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check available disk space on specified partitions")
    parser.add_argument("-w", "--warning", type=int, help="Minimum amount of free space in megabytes before warning")
    parser.add_argument("-e", "--error-at-mb", type=int, help="Amount of free space in megabytes to generate an error message")
    args = parser.parse_args()

    partitions = ["/boot", "/", "/home", "/tmp", "/usr", "/var"]
    exit_code = 0

    if args.warning is None or args.error_at_mb is None:
        message(ERROR, "Specify warning threshold with -w or --warning and error threshold with -e or --error-at-mb")
        exit(1)

    for partition in partitions:
        if os.path.ismount(partition):  # Check if partition is a mounted partition
            result = check_free_space(partition, args.warning, args.error_at_mb)
            if result == ERROR:
                exit_code = 1

    exit(exit_code)

