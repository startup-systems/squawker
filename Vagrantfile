# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  # Using this box rather than the official one because of:
  # https://bugs.launchpad.net/cloud-images/+bug/1621393
  config.vm.box = "boxcutter/ubuntu1604"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Flask
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  # Django
  config.vm.network "forwarded_port", guest: 8000, host: 8000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", name: "root privisioning", inline: <<-SHELL
    # https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions
    curl -sL https://deb.nodesource.com/setup_6.x | bash -

    apt-get update
    apt-get install -y build-essential git nodejs python3-pip

    pip3 install --upgrade pip virtualenvwrapper
  SHELL

  config.vm.provision "shell", name: "user provisioning", privileged: false, inline: <<-SHELL
    git config --global push.default simple
    echo "export EDITOR=vim" >> ~/.bash_profile

    # set up auto_virtualenv
    # https://gist.github.com/afeld/4aefc7c9493f1519e141f52b40dc6479
    wget -nv https://gist.githubusercontent.com/afeld/4aefc7c9493f1519e141f52b40dc6479/raw/3731cc202f5e52ea67bcc9c8f7282357849546d8/auto_virtualenv.sh
    chmod a+x auto_virtualenv.sh
    echo "source ~/auto_virtualenv.sh" >> ~/.bash_profile

    # work around NPM permissions issue
    # https://docs.npmjs.com/getting-started/fixing-npm-permissions#option-2-change-npms-default-directory-to-another-directory
    mkdir -p ~/.npm-global
    npm config set prefix '~/.npm-global'
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.profile
  SHELL
end
