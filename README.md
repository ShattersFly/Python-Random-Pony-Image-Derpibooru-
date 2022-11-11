# Random-Pony-Image(Derpibooru)
Is a python script using sereral modules to fetch and send pony pictures from Derpibooru using windows notifications
It is designed to work on windows 10/11(and 7, though i didnt test it since i have nothing to test it on, but i tried)
For this to work windows notifications must be enabled in settings as well as in privacy settings

For those who dont want to work with python, there will be .exe version(compiled with Pyinstaller) in Releases page

# Customizing
In generated config that the path of which will be shown to you on first run you can customize several things:

interval_minutes - interval in minutes before new image will be sent(def. 20)
tags - which tags image must have or not have, works the same as search on derpibooru, so make sure to correctly set them
image_by_date - uses score of the image to show you new, old, whatever images. there are 4 modes: new, old, random, custom (def. new)
custom_score_range - if image_by_date is set to custom you define range of score you want your images to have, must contain at least two numbers, for example: custom_score_range=30,500
