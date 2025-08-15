# Docker Usage

Run everything inside a container.

## Build
```bash
docker build -t aws-devops-framework .
```

## Deploy (public)
```bash
export AWS_PROFILE=default
export AWS_DEFAULT_REGION=us-east-1
export DB_PASSWORD='your-strong-password'

docker run --rm -it   -v "$PWD/config:/app/config"   -v "$HOME/.aws:/root/.aws:ro"   -e AWS_PROFILE   -e AWS_DEFAULT_REGION   -e DB_PASSWORD   aws-devops-framework deploy --config config/web_stack.yaml
```

## Status
```bash
docker run --rm -it   -v "$HOME/.aws:/root/.aws:ro"   -e AWS_PROFILE   -e AWS_DEFAULT_REGION   aws-devops-framework status --stack MyWebStack
```

## Destroy
```bash
docker run --rm -it   -v "$HOME/.aws:/root/.aws:ro"   -e AWS_PROFILE   -e AWS_DEFAULT_REGION   aws-devops-framework destroy --stack MyWebStack
```

## docker-compose
Edit `docker-compose.yml` (DB_PASSWORD, profile), then:
```bash
docker compose up --build
```
