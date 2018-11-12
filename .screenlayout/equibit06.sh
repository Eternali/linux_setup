#!/bin/sh
xrandr --output VIRTUAL1 --off
xrandr --output eDP1 --primary --mode 1920x1080 --pos 1440x1432 --rotate normal
xrandr --output DP1 --off
xrandr --output HDMI2 --off
xrandr --output HDMI1 --off
xrandr --output DP1-3 --off
xrandr --output DP1-2 --mode 2560x1440 --pos 2416x0 --rotate normal
xrandr --output DP1-1 --mode 2560x1440 --pos 0x0 --rotate right --output DP2 --off
