# Navigation AI Project

### Quick Start
__Note:__ this project runs on Ubuntu or WSL and requires Python3 + virtualenv. osmnx is much easier to install on Linux.

Create a virtual environment and activate it
```bash
virtualenv env
source ./env/bin/activate
```

Install dependencies
```bash
pip install requirements.txt
```

If you prefer, the dependencies can be installed individually. This project uses:
* geopy
* osmnx
* folium
* flask

Next create a file in the home directory called __api_key.txt__. This file stores the api key for google maps that is being read in by the application and will need to have the key added to its first line. As this repo is public and google services are not free, we have not included our api key however the api key will be included in the dropbox submission on canvas. The key will be deactivated on May 1 2021. Alternatively you can create your own api key with google and enable it for distance matrix.

Once the dependencies are all installed, the project can be run with the following command:
```bash
python3 app.py
```
__Note:__ the run command may differ based on your environment variables.
<br>
<br>

Once the flask server is running, navigate to localhost:5000 by clicking on the link in the shell or manually through the browser.

Once the project is running, enter a start and end address. The address must contain the city it is in and if not the province. For example:
```
start: 2544 Rosedrop Path, Oshawa
end: Ontario Tech University, Oshawa
```

Click the Find Route button and the program will take care of the rest. To add a new set of addresses, navigate back to the home page and enter new addresses.

Overall this application works fairly well. It has a sizeable bottleneck when obtaining the subsection of the map data from osmnx. I recommend not trying to navigate farther than 20-30km otherwise it may take a long time to load. When used to route from Waterloo to Oshawa (170km), it took about 20 minutes to generate the graph. The dijkstra's algorithm itself however is fairly fast.


