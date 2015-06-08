Vagrant.configure(2) do |config|
    config.vm.box = "ubuntu/trusty64"

    config.vm.box_check_update = true

    config.vm.network "forwarded_port", guest: 80, host: 8000
    config.vm.network "forwarded_port", guest: 5432, host: 5432
    config.vm.network "forwarded_port", guest: 5672, host: 5672
    config.vm.network "forwarded_port", guest: 15672, host: 15672

    # config.vm.network "private_network", ip: "192.168.33.10"
    # config.vm.network "public_network"

    # config.vm.synced_folder "../data", "/vagrant_data"

    config.vm.provider "virtualbox" do |vb|
        # Customize the amount of memory on the VM:
        vb.memory = "2048"
    end

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provision/setup.yml"
        ansible.sudo = true
        ansible.extra_vars = {
            'core_hostname' => 'passgen',
            'postgis_is_dev' => true,
        }
    end
end
