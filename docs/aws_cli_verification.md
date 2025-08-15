# AWS CLI Verification Guide

These commands help you validate and troubleshoot your deployment.

> Replace placeholders like `MyWebStack`, `cluster-name`, `service-name`, and regions as needed.

## 1) CloudFormation
Get stack status & outputs:
```bash
aws cloudformation describe-stacks --stack-name MyWebStack --query "Stacks[0].{Status:StackStatus,Outputs:Outputs}" --output table
```

## 2) ALB & Target Group
List load balancers:
```bash
aws elbv2 describe-load-balancers --query "LoadBalancers[].{Name:LoadBalancerName,DNS:DNSName,State:State.Code}" --output table
```
Find target group health (replace TG ARN):
```bash
TG_ARN=$(aws elbv2 describe-target-groups --query "TargetGroups[0].TargetGroupArn" --output text)
aws elbv2 describe-target-health --target-group-arn "$TG_ARN" --output table
```

## 3) ECS Cluster, Service, and Tasks
List clusters & services:
```bash
aws ecs list-clusters
aws ecs list-services --cluster <cluster-arn-or-name>
```
Describe service health:
```bash
aws ecs describe-services --cluster <cluster> --services <service-name> --query "services[0].{Status:status,Running:runningCount,Desired:desiredCount}" --output table
```
List tasks and describe one:
```bash
aws ecs list-tasks --cluster <cluster> --service-name <service-name>
aws ecs describe-tasks --cluster <cluster> --tasks <task-arn>
```

## 4) ECS Exec (into a running task)
Enable `executeCommand` at the account/cluster level if needed, then:
```bash
aws ecs execute-command   --cluster <cluster>   --task <task-arn>   --container app   --interactive   --command "/bin/sh"
```
From inside, you can curl the container, check env, etc.

## 5) CloudWatch Logs
Get recent container logs:
```bash
LOG_GROUP="/ecs/demo-web"  # replace with your ProjectName in the config
aws logs describe-log-streams --log-group-name "$LOG_GROUP" --order-by LastEventTime --descending --max-items 5
STREAM="<stream-name>"
aws logs get-log-events --log-group-name "$LOG_GROUP" --log-stream-name "$STREAM" --limit 50 --output text
```

## 6) RDS Endpoint & Connectivity
Get endpoint (also in CFN outputs):
```bash
aws rds describe-db-instances --query "DBInstances[].{DB:DBInstanceIdentifier,Endpoint:Endpoint.Address,Status:DBInstanceStatus}" --output table
```
For the **private scenario**, connect from inside an ECS task using `psql` (install if your image doesn't include it). Example:
```bash
# inside the ECS task shell:
apk add --no-cache postgresql-client || yum install -y postgresql || apt-get update && apt-get install -y postgresql-client
psql -h <db-endpoint> -U appuser -d appdb -c "SELECT now();"
```

## 7) Route53 & ACM (private scenario)
Check the DNS record:
```bash
aws route53 list-resource-record-sets --hosted-zone-id Z123456ABCDEFG --query "ResourceRecordSets[?Name=='app.example.com.']"
```
List certificates:
```bash
aws acm list-certificates --certificate-statuses ISSUED --query "CertificateSummaryList[].{Domain:DomainName,ARN:CertificateArn}" --output table
```

## 8) Cleanup
Destroy the stack to avoid charges:
```bash
aws cloudformation delete-stack --stack-name MyWebStack
aws cloudformation wait stack-delete-complete --stack-name MyWebStack
```
