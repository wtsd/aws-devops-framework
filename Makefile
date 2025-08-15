.PHONY: build shell deploy status destroy

IMAGE ?= aws-devops-framework:latest

build:
	docker build -t $(IMAGE) .

shell:
	docker run --rm -it \	  -v $$PWD/config:/app/config \	  -v $$HOME/.aws:/root/.aws:ro \	  -e AWS_PROFILE=$${AWS_PROFILE:-default} \	  -e AWS_DEFAULT_REGION=$${AWS_DEFAULT_REGION:-us-east-1} \	  -e DB_PASSWORD=$${DB_PASSWORD:-changeme} \	  $(IMAGE) --help

deploy:
	docker run --rm -it \	  -v $$PWD/config:/app/config \	  -v $$HOME/.aws:/root/.aws:ro \	  -e AWS_PROFILE=$${AWS_PROFILE:-default} \	  -e AWS_DEFAULT_REGION=$${AWS_DEFAULT_REGION:-us-east-1} \	  -e DB_PASSWORD=$${DB_PASSWORD} \	  $(IMAGE) deploy --config $${CFG:-config/web_stack.yaml}

status:
	docker run --rm -it \	  -v $$HOME/.aws:/root/.aws:ro \	  -e AWS_PROFILE=$${AWS_PROFILE:-default} \	  -e AWS_DEFAULT_REGION=$${AWS_DEFAULT_REGION:-us-east-1} \	  $(IMAGE) status --stack $${STACK:-MyWebStack}

destroy:
	docker run --rm -it \	  -v $$HOME/.aws:/root/.aws:ro \	  -e AWS_PROFILE=$${AWS_PROFILE:-default} \	  -e AWS_DEFAULT_REGION=$${AWS_DEFAULT_REGION:-us-east-1} \	  $(IMAGE) destroy --stack $${STACK:-MyWebStack}
