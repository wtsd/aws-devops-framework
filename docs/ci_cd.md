# CI/CD with GitHub Actions (OIDC)

A workflow is included at `.github/workflows/deploy.yml`.

## Setup
1. Create an IAM role for GitHub OIDC that can deploy CloudFormation, ECS, RDS, etc.
2. In your repo, add secrets:
   - `AWS_ROLE_TO_ASSUME`: that role's ARN
   - `AWS_REGION`: e.g., `us-east-1`
   - `DB_PASSWORD`: your DB password
   - `ECR_REPO` (optional): e.g., `123456789012.dkr.ecr.us-east-1.amazonaws.com/myapp`

## Use
- Push to `main` triggers the workflow.
- Set env `SCENARIO=public` (default) or `SCENARIO=private` to select stack.
- Outputs are printed at the end via `cli.py status`.

## Notes
- OIDC avoids long-lived keys; prefer it over static credentials.
- If building a custom app, push its image to ECR and set `container_image` in the config.
