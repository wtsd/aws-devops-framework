# AWS DevOps Framework (Python + AWS SDK)

A ready-to-go scaffold for DevOps engineers to deploy a typical web stack on AWS using **Python (boto3)** + **CloudFormation**.

**Stacks included**
- **Public scenario**: ALB + ECS Fargate (public subnets) + RDS (private SG; not publicly accessible)
- **Private scenario**: ALB (public) + ECS Fargate (private subnets behind NAT) + RDS (private) + optional **Route53** alias + **ACM** DNS-validated certificate

**Run via**
- Python CLI (`cli.py`)
- **Docker** (Dockerfile, docker-compose)
- **GitHub Actions** (OIDC recommended)

> ⚠ **Costs**: ALB, RDS, NAT Gateway, etc. incur charges. Tear down stacks when done.

## Start here
- Read **docs/quickstart.md** for basic usage
- See **docs/docker.md** for container-based usage
- See **docs/private_scenario.md** for Route53 + ACM and private networking
- See **docs/ci_cd.md** for GitHub Actions
- Verify your deployment with **docs/aws_cli_verification.md**


---
### Documentation index
- [Quick Start](docs/quickstart.md)
- [Docker Usage](docs/docker.md)
- [Private Scenario (Route53/ACM)](docs/private_scenario.md)
- [CI/CD with GitHub Actions](docs/ci_cd.md)
- [AWS CLI Verification Guide](docs/aws_cli_verification.md)
