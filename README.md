# playlist-color-sort
A simple script to sort your Spotify playlists by their track image color 

# Step [-1] Install Python (if not already present)
Download python from www.python.org and install it. If you're a windows user, please make sure to add python to the PATH

# Step [0] Create your spotify app
For the script to work (at all), you need to create your app at https://developer.spotify.com/dashboard/ . Then, note the client ID and client secret

# Step [1] Download the script
Download the script and run `pip install -r requirements.txt` to install any missing libraries. Then, you can start the program properly.
Start it via the command line by either `python sort.py` on windows or by `python3 sort.py` on any other Unix-like system.

Copy the link to the playlist. The ID, which you need for the program, is located between the first "/" and the last "?"
(for example, the ID of the playlist "https://open.spotify.com/playlist/56sOJzB9ybdp7yr1XnZL1K?si=98630216bcd546c8" is "56sOJzB9ybdp7yr1XnZL1K")

Follow the output on the screen and enjoy

# Limitations
The algorithm works by sorting the hue first and then the saturation, so it might not seem 100% "sorted" at times (it is called "step"-algorithm, courtesy of Alan Zucconis great article: https://www.alanzucconi.com/2015/09/30/colour-sorting/). 

Second of all, due to the compression by the Spotify Servers (the images get stored as jpg), the image might not exactly have the color you can see. 

Non-monochromatic images tend to yield very interesting color results (as a black and white image yields >grey<). This is a limitation due to the fact that the **average** color gets taken. I might change this in the future to the most present color to mild this effect.

# Roadmap
- better image color algorithm
- better handling of rate limit restrictions
- option to sort all playlists of a user at once
