# Local Website

This directory is for the local website. It will only work on the same local network as the sensors. To run the external website - which pulls less frequent, lower resolution from airtable - see 'external website directory'.

This is a front-end JS only site, the pulls data from the APIs running on the Raspberry Pis.

To run:
* Navigate to the "local_website" directory and run `python -m http.server 8888`
* In a browser, go to http://localhost:8888

## Plots

4 plots
* tempF (ind & abg)
* tempC (ind & abg)
* humidityF (ind & avg)
* Power