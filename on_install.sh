#!/bin/bash

HOMEDIR='/home/'$1
CURDIR=`pwd`

su - $1

rm $HOMEDIR/.zshrc
rm $HOMEDIR/.zsh_aliases
rm $HOMEDIR/.tmux.conf
rm -rf $HOMEDIR/.config/i3
rm -r $HOMEDIR/.screenlayout
rm -r $HOMEDIR/.config/nvim
rm -r $HOMEDIR/.config/rofi
mkdir -p $HOMEDIR/.config/i3
mkdir $HOMEDIR/.config/nvim
mkdir $HOMEDIR/.config/rofi

sudo apt install -y git build-essential xclip python3-pip curl zsh tmux i3 nitrogen apt-transport-https whois rofi
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt update
sudo apt install -y docker-ce
sudo groupadd docker
sudo usermod -aG docker $1
su - $1
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
git clone https://github.com/bhilburn/powerlevel9k.git $HOMEDIR/.oh-my-zsh/custom/themes/powerlevel9k
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt install -y neovim yarn nodejs
sudo apt install -y arandr i3blocks pm-utils xbacklight blueman mongodb xautolock fonts-firacode
sudo apt install -f -y

mkdir -p $HOMEDIR/.fonts
cp $CURDIR/.fonts/* $HOMEDIR/.fonts/

ln -s $CURDIR/.config/nvim/init.vim $HOMEDIR/.config/nvim/init.vim
ln -s $CURDIR/.config/nvim/colors $HOMEDIR/.config/nvim/colors
ln -s $CURDIR/.zshrc $HOMEDIR/.zshrc
ln -s $CURDIR/.zsh_aliases $HOMEDIR/.zsh_aliases
ln -s $CURDIR/.tmux.conf $HOMEDIR/.tmux.conf
ln -s $CURDIR/.screenlayout $HOMEDIR/.screenlayout
ln -s $CURDIR/.config/i3/config $HOMEDIR/.config/i3/config
ln -s $CURDIR/.config/i3/startup $HOMEDIR/.config/i3/startup
cp $CURDIR/.config/rofi/config $HOMEDIR/.config/rofi/config

cd ~/Downloads
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo dpkg -i skypeforlinux-64.deb
sudo apt install -f
mkdir ~/applications
cd ~/applications
git clone https://github.com/flutter/flutter.git -b beta
. ~/.zshrc
flutter doctor
mkdir ~/FlutterProjects
cd ~/FlutterProjects
git clone https://github.com/eternali/watoplan_flut -b dev
git clone https://github.com/eternali/custom_radio
git clone https://github.com/eternali/mldemos
git clone https://github.com/eternali/flutter_calendar
git clone https://github.com/eternali/date_utils
git clone https://github.com/eternali/tictacthrow
mkdir ~/VueProjects
cd ~/VueProjects
git clone https://github.com/eternali/conradheidebrecht.com
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 931FF8E79F0876134EDDBDCCA87FF9DF48BF1C90
echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list
sudo apt install -y spotify-client
git config --global user.email "conrad.heidebrecht@gmail.com"
git config --global user.name "Conrad"
cd ~/Downloads
git clone https://github.com/guimeira/i3lock-fancy-multimonitor.git
cp -r i3lock-fancy-multimonitor ~/.config/i3
chmod +x ~/.config/i3/i3lock-fancy-multimonitor/lock



