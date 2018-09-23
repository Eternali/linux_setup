#!/bin/zsh

apt install git build-essential docker xclip python3-pip curl zsh tmux i3 nitrogen
cp -r * ~/
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
git clone https://github.com/bhilburn/powerlevel9k.git {local_home}/.oh-my-zsh/custom/themes/powerlevel9k
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
apt install neovim yarn nodejs
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \\
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
apt install arandr i3blocks pm-utils xbacklight blueman mongodb xautolock
apt install -f
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
echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list
apt install spotify-client
git config --global user.email "conrad.heidebrecht@gmail.com"
git config --global user.name "Conrad"
cd ~/Downloads
git clone https://github.com/guimeira/i3lock-fancy-multimonitor.git
cp -r i3lock-fancy-multimonitor ~/.config/i3
chmod +x ~/.config/i3/i3lock-fancy-multimonitor/lock



