ansible-prepare:
	ansible-galaxy install --force -r ansible/requirements.yml

vagrant-up: ansible-prepare vagrant-destroy
	vagrant up

vagrant-destroy:
	vagrant destroy --force

clean: vagrant-destroy clean-setup

clean-setup:
	rm -rf dist

dist:
	./setup.py sdist
	rm -f dist/latest.tar.gz
	ln -s `ls -1 dist | sort -r | head -1` dist/latest.tar.gz

.PHONY: dist
