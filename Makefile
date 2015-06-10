PASSGEN_SERVER_NAME = localhost

ansible-prepare:
	ansible-galaxy install --force -r requirements.yml -p provision/roles

vagrant-up: ansible-prepare vagrant-destroy
	vagrant up

vagrant-destroy:
	vagrant destroy --force

clean: vagrant-destroy clean-setup

clean-setup:
	rm -rf dist

.PHONY: dist
dist:
	cd passgen/static.in; gulp build
	./setup.py sdist

	mkdir -p provision/files
	rm -rf provision/files/latest.tar.gz
	cp dist/`ls -1 dist | sort -r | head -1` provision/files/latest.tar.gz

.PHONY: deploy
deploy: dist
	ansible-playbook \
		-i "wygoda.net," \
		--extra-vars "core_hostname=faron passgen_server_name=$(PASSGEN_SERVER_NAME)" \
		--become --ask-become-pass \
		provision/setup.yml
