#!/bin/sh
xrandr --output VIRTUAL1 --off
xrandr --output eDP1 --primary --mode 1920x1080 --pos 0x272 --rotate normal
xrandr --output DP1 --off
xrandr --output HDMI2 --mode 1920x1080 --pos 1920x0 --rotate normal
xrandr --output HDMI1 --off --output DP2 --off
