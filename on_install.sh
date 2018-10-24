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
rm -r $HOMEDIR/.config/i3blocks
mkdir -p $HOMEDIR/.config/i3
mkdir $HOMEDIR/.config/nvim
mkdir $HOMEDIR/.config/rofi

# general essentials and dependancies
sudo apt install -y
    git \
    build-essential \
    xclip \
    python3-pip \
    curl \
    zsh \
    tmux \
    i3 \
    rofi
    nitrogen \
    apt-transport-https \
    whois \
    screenfetch \
    default-jdk \
    gradle \
    libpth-dev \
    libx11-dev \
    libx11-xcb-dev \
    libcairo2-dev \
    libxcb-xkb-dev \
    libxcb-xinerama0-dev \
    libxcb-randr0-dev \
    libxinerama-dev \
    libxft-dev

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
sudo apt install -y arandr i3blocks pm-utils xbacklight blueman mongodb xautolock fonts-firacode scratchpad
sudo apt install -f -y
sudo npm i -g typescript typings standard @vue/cli eslint

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
ln -s $CURDIR/.config/i3blocks $HOMEDIR/.config/i3blocks
cp $CURDIR/.config/rofi/config $HOMEDIR/.config/rofi/config

cd ~/Downloads
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo dpkg -i skypeforlinux-64.deb
sudo apt install -f

# applications
mkdir ~/applications
cd ~/applications
git clone https://github.com/flutter/flutter.git -b beta
. ~/.zshrc
flutter doctor
git clone https://github.com/sbstnc/dmenu-ee
sudo make clean install
#git clone https://github.com/emgram769/lighthouse
#cd lighthouse
#make
#sudo make install
#lighthouse-install
#chmod +x ~/.config/lighthouse/cmd*
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
curl -s https://updates.signal.org/desktop/apt/keys.asc | sudo apt-key add -
echo "deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main" | sudo tee -a /etc/apt/sources.list.d/signal-xenial.list
sudo apt update && sudo apt install signal-desktop
sudo apt install snapd snapd-xdg-open
sudo snap install kotlin --classic

# pip
sudo pip3 install neovim

sudo mv /usr/bin/dmenu /usr/bin/dmenu_bak
sudo ln -s /usr/local/bin/dmenu /usr/bin/dmenu
