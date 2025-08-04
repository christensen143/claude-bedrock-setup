import subprocess
import json
from typing import List, Dict


class BedrockClient:
    def __init__(self, region: str = "us-west-2"):
        self.region = region

    def list_claude_models(self) -> List[Dict[str, str]]:
        """List available Claude models with inference profiles"""
        try:
            # Use AWS CLI directly to avoid credential issues
            cmd = [
                "aws",
                "bedrock",
                "list-inference-profiles",
                "--region",
                self.region,
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            response = json.loads(result.stdout)

            models = []
            for profile in response.get("inferenceProfileSummaries", []):
                profile_id = profile.get("inferenceProfileId", "")
                profile_name = profile.get("inferenceProfileName", "")

                # Filter for Claude models
                if "anthropic.claude" in profile_id:
                    # Extract model info from the profile ID
                    model_name = profile_name or profile_id.split("/")[-1]

                    models.append(
                        {
                            "id": profile_id,
                            "name": model_name,
                            "arn": profile.get("inferenceProfileArn", ""),
                            "status": profile.get("status", "ACTIVE"),
                        }
                    )

            # Sort models by name
            models.sort(key=lambda x: x["name"])

            return models

        except subprocess.CalledProcessError as e:
            if "AccessDeniedException" in e.stderr:
                raise Exception(
                    "Access denied. Please check your AWS "
                    "permissions for Amazon Bedrock."
                )
            elif "not authorized" in e.stderr:
                raise Exception(
                    "Not authenticated with AWS. Please run "
                    "'aws configure' or set up your AWS "
                    "credentials."
                )
            else:
                raise Exception(f"Error listing models: {e.stderr}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
