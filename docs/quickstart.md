# Quick Start

This framework deploys a typical web stack on AWS using Python + CloudFormation.

## Prerequisites
- AWS account + permissions for VPC, ALB, ECS, RDS, IAM (and Route53/ACM for DNS/TLS).
- Python 3.10+
- AWS credentials configured (`aws configure` or env vars).

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Configure
Pick a scenario config to edit:
- **Public**: `config/web_stack.yaml`
- **Private + NAT + Route53/ACM**: `config/web_stack_private.yaml`

Set the database password via environment variable (recommended):
```bash
export DB_PASSWORD='your-strong-password'
```

## Deploy
```bash
python cli.py deploy --config config/web_stack.yaml
# or
python cli.py deploy --config config/web_stack_private.yaml
```

## Check status
```bash
python cli.py status --stack MyWebStack
```

## Destroy
```bash
python cli.py destroy --stack MyWebStack
```

> ⚠ Costs: ALB, RDS, and NAT Gateway incur ongoing charges. Destroy when done.
