#!/bin/zsh

HOMEDIR='/home/'$1
CURDIR=`pwd`
rm $HOMEDIR/.zshrc
rm $HOMEDIR/.zsh_aliases
rm $HOMEDIR/.tmux.conf
rm -rf $HOMEDIR/.config/i3
rm -r $HOMEDIR/.screenlayout
rm -r $HOMEDIR/.config/nvim
mkdir -p $HOMEDIR/.config/nvim
ln -s $CURDIR/.config/nvim/init.vim $HOMEDIR/.config/nvim/init.vim
ln -s $CURDIR/.config/nvim/colors $HOMEDIR/.config/nvim/colors
ln -s $CURDIR/.zshrc $HOMEDIR/.zshrc
ln -s $CURDIR/.zsh_aliases $HOMEDIR/.zsh_aliases
ln -s $CURDIR/.tmux.conf $HOMEDIR/.tmux.conf
ln -s $CURDIR/.config/i3 $HOMEDIR/.config/i3
ln -s $CURDIR/.screenlayout $HOMEDIR/.screenlayout

apt install -y git build-essential xclip python3-pip curl zsh tmux i3 nitrogen apt-transport-https
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt update
apt install -y docker-ce
groupadd docker
usermod -aG docker $1
su - $1
cp -r * ~/
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
git clone https://github.com/bhilburn/powerlevel9k.git $HOMEDIR/.oh-my-zsh/custom/themes/powerlevel9k
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
curl -sL https://deb.nodesource.com/setup_10.x | -E bash -
apt install -y neovim yarn nodejs
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \\
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
apt install -y arandr i3blocks pm-utils xbacklight blueman mongodb xautolock fonts-firacode
apt install -f -y
cd ~/Downloads
dpkg -i google-chrome-stable_current_amd64.deb
dpkg -i skypeforlinux-64.deb
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
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 931FF8E79F0876134EDDBDCCA87FF9DF48BF1C90
echo deb http://repository.spotify.com stable non-free | tee /etc/apt/sources.list.d/spotify.list
apt install -y spotify-client
git config --global user.email "conrad.heidebrecht@gmail.com"
git config --global user.name "Conrad"
cd ~/Downloads
git clone https://github.com/guimeira/i3lock-fancy-multimonitor.git
cp -r i3lock-fancy-multimonitor ~/.config/i3
chmod +x ~/.config/i3/i3lock-fancy-multimonitor/lock



