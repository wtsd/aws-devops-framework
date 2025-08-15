from __future__ import annotations
import os, json, pathlib
import click
from awsdevops.config import load_config
from awsdevops.cfn import ensure_stack, stack_status, destroy_stack

TEMPLATE_PUBLIC = pathlib.Path(__file__).parent / "templates" / "web_stack.yaml"
TEMPLATE_PRIVATE = pathlib.Path(__file__).parent / "templates" / "web_stack_private.yaml"

def render_params(cfg: dict) -> dict:
    base = {
        "ProjectName": cfg["project_name"],
        "VpcCidr": cfg["vpc_cidr"],
        "PublicSubnet1Cidr": cfg["public_subnet_cidrs"][0],
        "PublicSubnet2Cidr": cfg["public_subnet_cidrs"][1],
        "ContainerImage": cfg["container_image"],
        "ContainerPort": str(cfg["container_port"]),
        "DesiredCount": str(cfg["desired_count"]),
        "DBName": cfg["db_name"],
        "DBUsername": cfg["db_username"],
        "DBPassword": cfg["db_password"],
        "DBAllocatedStorage": str(cfg["db_allocated_storage"]),
        "DBInstanceClass": cfg["db_instance_class"],
        "DBEngineVersion": cfg["db_engine_version"],
    }
    if cfg.get("scenario", "public") == "public":
        base["SSLCertificateArn"] = cfg.get("ssl_certificate_arn", "") or ""
        return base
    else:
        base.update({
            "PrivateSubnet1Cidr": cfg["private_subnet_cidrs"][0],
            "PrivateSubnet2Cidr": cfg["private_subnet_cidrs"][1],
            "DomainName": cfg.get("domain_name", ""),
            "HostedZoneId": cfg.get("hosted_zone_id", ""),
            "ProvideCertificateArn": cfg.get("provide_certificate_arn", ""),
        })
        return base

@click.group()
def cli():
    pass

@cli.command()
@click.option("--config", "-c", "config_path", required=True, help="Path to YAML config.")
def deploy(config_path):
    """Create or update the selected stack."""
    cfg = load_config(config_path)
    template_path = TEMPLATE_PRIVATE if cfg.get("scenario", "public") == "private" else TEMPLATE_PUBLIC
    with open(template_path, "r") as f:
        template_body = f.read()
    params = render_params(cfg)
    ensure_stack(cfg["region"], cfg["stack_name"], template_body, params, cfg.get("tags", {}))
    st = stack_status(cfg["region"], cfg["stack_name"])
    click.echo(json.dumps(st, indent=2))

@cli.command()
@click.option("--stack", "stack_name", required=True, help="Stack name")
@click.option("--region", default=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
def status(stack_name, region):
    """Show current stack status and outputs."""
    st = stack_status(region, stack_name)
    click.echo(json.dumps(st, indent=2))

@cli.command()
@click.option("--stack", "stack_name", required=True, help="Stack name")
@click.option("--region", default=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
def destroy(stack_name, region):
    """Delete the stack (dangerous)."""
    destroy_stack(region, stack_name)
    click.echo(f"Stack {stack_name} deleted.")

if __name__ == "__main__":
    cli()
