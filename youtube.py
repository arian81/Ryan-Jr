import requests
import re


def check_new_video():
    channel = "https://www.youtube.com/channel/UC7gXXzu2D5rSu3NH4DJw9cw"
    html = requests.get(channel + "/videos").text
    info = re.search('(?<={"label":").*?(?="})', html).group()
    url = (
        "https://www.youtube.com/watch?v="
        + re.search('(?<="videoId":").*?(?=")', html).group()
    )

    if "1XC3" in info:
        latest_video = url

    with open("latest_video.txt", "r") as f:
        previous_video = f.read().strip("\n")
    with open("latest_video.txt", "w") as f:
        f.write(latest_video)

    return previous_video != latest_video
