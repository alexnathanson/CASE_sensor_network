# Local Website

This directory is for the local website. It will only work on the same local network as the sensors. To run the external website - which pulls less frequent, lower resolution from airtable - see 'external website directory'.

This is a front-end JS only site, the pulls data from the APIs running on the Raspberry Pis.

To run:
* Navigate to the "local website" directory and run `python -m http.server 8000`
* In a browser, go to http://localhost:8000/

## Plots

4 plots
* temp (ind & abg)
* humidity (ind & avg)
* cooling energy
* heater energy


12-hour live visualization