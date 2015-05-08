ansible-prepare:
	ansible-galaxy install --force -r ansible/requirements.yml

vagrant-up: ansible-prepare vagrant-destroy
	vagrant up

vagrant-destroy:
	vagrant destroy --force

clean: vagrant-destroy
