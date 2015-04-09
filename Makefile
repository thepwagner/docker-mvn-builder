BUILDER_IMAGE=mvn-builder
IMAGE=mvn-child

POM_DEPS="org.apache.cassandra:cassandra-all:2.1.4"
POM_MAIN="org.apache.cassandra.service.CassandraDaemon"

build: .built

.built: .built.builder
	docker run --rm -e POM_DEPS=$(POM_DEPS) -e POM_MAIN=$(POM_MAIN) $(BUILDER_IMAGE) | docker build -t $(IMAGE) -
	@docker inspect -f '{{.Id}}' $(IMAGE) > .built

builder: .built.builder

.built.builder:
	docker build -t $(BUILDER_IMAGE) .
	@docker inspect -f '{{.Id}}' $(BUILDER_IMAGE) > .built.builder

runbash: .built
	docker run --rm -it $(IMAGE) /bin/bash

run: .built
	docker run --rm -it $(IMAGE)

runbuilder: .built.builder
	docker run --rm -e POM_DEPS=$(POM_DEPS) -e POM_MAIN=$(POM_MAIN) -it $(BUILDER_IMAGE) /bin/bash

clean:
	rm -f .built

cleanall:
	rm -f .built .built.builder
