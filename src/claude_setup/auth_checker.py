from __future__ import annotations

import subprocess


def check_aws_auth() -> bool:
    """Check if AWS credentials are properly configured"""
    try:
        # Use AWS CLI to verify credentials
        subprocess.run(
            ["aws", "sts", "get-caller-identity"],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        # AWS CLI not installed
        return False
    except Exception:
        return False
