###########################################################################################################################
# Make framework that provides generic docker based function
# and project values.
#
# @author Félix Voituret <fvoituret@deezer.com>
# @version 1.0.0
###########################################################################################################################

SHELL 			= /bin/bash -x
PROJECT			= muzeeglot
COMPOSE			= docker-compose -p $(PROJECT)
COMPOSE_FILE 	= docker-compose.yaml
COMPOSE_OPTS	=
DOCKER			= docker
DOMAIN			=
CERTCOMMAND		= certonly --webroot --webroot-path=/data/letsencrypt -d $(DOMAIN) -d www.$(DOMAIN)
CERTVOLUMES		= -v $(PROJECT)-certificates:/etc/letsencrypt
CERTVOLUMES		+= -v $(PROJECT)-certificates-data:/data/letsencrypt
BUILDERVOLUMES  = $(CERTVOLUMES) -v frontend/nginx/certificate-builder.conf:/etc/nginx/nginx.conf:ro

.PHONY: api frontend

usage:
	$(eval SHELL=/bin/bash)
	@echo "Supported goals:"
	@echo "	* make [no-cache] api|frontend"
	@echo "	* make [ssl] run|start|stop"
	@echo "	* make clean|letsencrypt|logs"

no-cache:
	$(eval COMPOSE_OPTS=$(COMPOSE_OPTS) --no-cache)

ssl:
	$(eval COMPOSE_FILE=docker-compose-ssl.yaml)

letsencrypt:
	-@$(DOCKER) volume rm $(PROJECT)-certificates
	-@$(DOCKER) volume rm $(PROJECT)-certificates-data
	@$(DOCKER) volume create $(PROJECT)-certificates
	@$(DOCKER) volume create $(PROJECT)-certificates-data
	@$(DOCKER) run -d $(BUILDERVOLUMES) -p 80:80 -p 443:443 --name $(PROJECT)-certificate-builder nginx
	@$(DOCKER) run -it --rm $(CERTVOLUMES) deliverous/certbot $(CERTCOMMAND)
	@$(DOCKER) kill $(PROJECT)-certificate-builder
	@$(DOCKER) rm $(PROJECT)-certificate-builder

api:
	@$(COMPOSE) build $(COMPOSE_OPTS) api

frontend:
	@$(COMPOSE) build $(COMPOSE_OPTS) frontend

run: api frontend
	@$(COMPOSE) up

start: api frontend
	@$(COMPOSE) -f $(COMPOSE_FILE) up -d

stop:
	@$(COMPOSE) -f $(COMPOSE_FILE) down

logs:
	@$(COMPOSE) -f $(COMPOSE_FILE) logs --follow

clean: stop
	@docker volume rm $$(docker volume ls | grep muzeeglot | tr -s ' ' | cut -d' ' -f2)
