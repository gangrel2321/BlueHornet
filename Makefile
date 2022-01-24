all : docker_build
CURRENT_DIR := $(shell pwd)

docker_build :
	docker build -t "blue_hornet:$(USER)"

docker_run :
	docker run \
		-dt \
		-v "$(CURRENT_DIR):/BlueHornet" \
		--workdir /BlueHornet \
		--name "blue_hornet_$(USER)" \
		"blue_hornet:$(USER)" \
		bash

docker_exec : 
	docker exec -it "blue_hornet:$(USER)" bash

docker_clean : 
	docker rm --force "blue_hornet:$(USER)"
