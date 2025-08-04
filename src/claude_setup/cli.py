from __future__ import annotations

import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import sys

from .auth_checker import check_aws_auth
from .aws_client import BedrockClient
from .config_manager import ConfigManager
from .gitignore_manager import ensure_gitignore

# Create console - disable color when NO_COLOR is set or in tests
# Rich needs explicit no_color=True to disable ANSI codes
no_color = os.environ.get("NO_COLOR") or os.environ.get("PYTEST_CURRENT_TEST")
console = Console(no_color=bool(no_color))


@click.group()
@click.version_option(version="0.1.0", prog_name="claude-bedrock-setup")
def cli() -> None:
    """Claude Bedrock Setup CLI - Configure Claude to use AWS Bedrock"""
    pass


@cli.command()
@click.option("--region", default="us-west-2", help="AWS region (default: us-west-2)")
@click.option("--non-interactive", is_flag=True, help="Run in non-interactive mode")
def setup(region: str, non_interactive: bool) -> None:
    """Set up Claude to use AWS Bedrock"""
    console.print(
        Panel.fit(
            Text("Claude Bedrock Setup", style="bold blue"),
            subtitle="Configure Claude to use AWS Bedrock",
        )
    )

    # Check AWS authentication
    console.print("\n[yellow]Checking AWS authentication...[/yellow]")
    if not check_aws_auth():
        console.print("[red]✗ Not authenticated with AWS[/red]")
        console.print("\nPlease authenticate with AWS using one of these " "methods:")
        console.print("  • aws configure")
        console.print(
            "  • Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY "
            "environment variables"
        )
        console.print("  • Use AWS SSO: aws sso login")
        console.print("\nThen run this command again.")
        sys.exit(1)

    console.print("[green]✓ AWS authentication verified[/green]")

    # Initialize Bedrock client
    bedrock_client = BedrockClient(region)

    # Get available models
    console.print(
        f"\n[yellow]Fetching available Claude models from " f"{region}...[/yellow]"
    )
    models = bedrock_client.list_claude_models()

    if not models:
        console.print("[red]No Claude models found in the specified " "region.[/red]")
        console.print("Please check your AWS permissions and region.")
        sys.exit(1)

    # Select model
    if non_interactive and models:
        selected_model = models[0]
        console.print(
            f"[yellow]Using first available model: "
            f"{selected_model['name']}[/yellow]"
        )
    else:
        console.print("\n[bold]Available Claude models:[/bold]")
        for idx, model in enumerate(models, 1):
            console.print(f"  {idx}. {model['name']} ({model['id']})")

        while True:
            try:
                choice = click.prompt("\nSelect a model", type=int)
                if 1 <= choice <= len(models):
                    selected_model = models[choice - 1]
                    break
                else:
                    console.print("[red]Invalid choice. Please try " "again.[/red]")
            except (ValueError, KeyboardInterrupt):
                console.print("\n[yellow]Setup cancelled.[/yellow]")
                sys.exit(0)

    # Configure settings
    config_manager = ConfigManager()
    settings = {
        "CLAUDE_CODE_USE_BEDROCK": "1",
        "AWS_REGION": region,
        "ANTHROPIC_MODEL": selected_model["arn"],
        "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "4096",
        "MAX_THINKING_TOKENS": "1024",
    }

    config_manager.save_settings(settings)

    # Update .gitignore
    ensure_gitignore()

    console.print("\n[green]✓ Configuration saved successfully![/green]")
    console.print(f"\nModel: [cyan]{selected_model['name']}[/cyan]")
    console.print(f"Region: [cyan]{region}[/cyan]")
    console.print(f"Settings file: [cyan]{config_manager.settings_path}" "[/cyan]")
    console.print("\nClaude is now configured to use AWS Bedrock!")


@cli.command()
def status() -> None:
    """Show current Claude Bedrock configuration"""
    config_manager = ConfigManager()
    settings = config_manager.load_settings()

    if not settings:
        console.print("[yellow]No configuration found.[/yellow]")
        console.print(
            "Run 'claude-bedrock-setup setup' to configure Claude for " "AWS Bedrock."
        )
        return

    console.print(Panel.fit(Text("Claude Bedrock Configuration", style="bold blue")))

    console.print("\n[bold]Current settings:[/bold]")
    for key, value in settings.items():
        if key == "ANTHROPIC_MODEL":
            # Extract model ID from ARN
            model_id = value.split("/")[-1] if "/" in value else value
            console.print(f"  {key}: [cyan]{model_id}[/cyan]")
        else:
            console.print(f"  {key}: [cyan]{value}[/cyan]")

    console.print(f"\n[dim]Settings file: " f"{config_manager.settings_path}[/dim]")


@cli.command()
@click.confirmation_option(
    prompt="Are you sure you want to reset the " "configuration?"
)
def reset() -> None:
    """Reset Claude Bedrock configuration"""
    config_manager = ConfigManager()
    config_manager.reset_settings()
    console.print("[green]✓ Configuration reset successfully.[/green]")


if __name__ == "__main__":
    cli()
