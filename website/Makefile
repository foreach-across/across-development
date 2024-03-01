.PHONY: help develop production publish

help:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | grep -E -v -e '^[^[:alnum:]]' -e '^$@$$'
	@echo "$(LC_ALL)"
	@echo For development, use: make start

start:
	hugo server --buildDrafts --buildFuture --disableFastRender

develop:
	rm -rf public/*
	hugo --buildDrafts --buildFuture

production:
	rm -rf public/*
	hugo

deploy:
	@echo To deploy, run the script: ./deploy.sh "<GIT_COMMENT>"
