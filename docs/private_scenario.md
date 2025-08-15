# Private Subnets + NAT + Route53/ACM

## What it does
- ECS tasks in **private subnets** (no public IPs)
- **NAT Gateway** allows tasks to pull images & reach the internet
- **RDS** in private subnets, only accessible from ECS SG
- Optional **Route53** ALIAS + **ACM** DNS-validated certificate for HTTPS

## Configure
Edit `config/web_stack_private.yaml`:
```yaml
scenario: private
# Option 1: Use existing ACM certificate
provide_certificate_arn: arn:aws:acm:REGION:ACCOUNT:certificate/...
# Option 2: Create ACM certificate + ALIAS record
domain_name: app.example.com
hosted_zone_id: Z123456ABCDEFG
```
> The hosted zone must be authoritative for `domain_name` (or its parent).

## Deploy
```bash
export DB_PASSWORD='your-strong-password'
python cli.py deploy --config config/web_stack_private.yaml
```

## Notes
- NAT Gateway costs ~$30+/month + data processing. Destroy when idle.
- For DB admin, connect from an ECS task using `aws ecs execute-command` (see verification guide).
