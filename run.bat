@echo off
title Youtube Downloader - make by NDC

:::
:::     _   __   ____     ______
:::    / | / /  / __ \   / ____/
:::   /  |/ /  / / / /  / /     
:::  / /|  /  / /_/ /  / /___   
::: /_/ |_/  /_____/   \____/
:::

for /f "delims=: tokens=*" %%A in ('findstr /b ::: "%~f0"') do @echo(%%A

echo Start GUI for download video and audio from youtube

pip install tk
pip install pytube

python newVersion.py
