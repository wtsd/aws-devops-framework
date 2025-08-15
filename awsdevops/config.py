from __future__ import annotations
import os
import yaml

DEFAULTS = {
    "stack_name": "MyWebStack",
    "region": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    "project_name": "web-sample",
    "scenario": "public",  # 'public' or 'private'
    "vpc_cidr": "10.80.0.0/16",
    "public_subnet_cidrs": ["10.80.10.0/24", "10.80.20.0/24"],
    "private_subnet_cidrs": ["10.80.110.0/24", "10.80.120.0/24"],
    "container_image": "public.ecr.aws/nginx/nginx:latest",
    "container_port": 80,
    "desired_count": 1,
    "db_engine_version": "15.6",
    "db_instance_class": "db.t4g.micro",
    "db_allocated_storage": 20,
    "db_name": "appdb",
    "db_username": "appuser",
    "db_password": None,  # set in config or via DB_PASSWORD env
    # TLS/DNS
    "ssl_certificate_arn": "",        # public scenario
    "domain_name": "",                # private scenario
    "hosted_zone_id": "",             # private scenario
    "provide_certificate_arn": "",    # private scenario
    "tags": {"Project": "DevOpsFramework", "Owner": "you"},
}

def load_config(path: str) -> dict:
    with open(path, "r") as f:
        cfg = yaml.safe_load(f) or {}
    merged = {**DEFAULTS, **cfg}
    if not merged.get("db_password"):
        merged["db_password"] = os.getenv("DB_PASSWORD")
    if not merged["db_password"]:
        raise ValueError("db_password must be provided (config or DB_PASSWORD env).")
    return merged
