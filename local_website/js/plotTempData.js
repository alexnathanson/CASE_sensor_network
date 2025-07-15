// Refresh every 60 minutes (3600000 milliseconds)
rt = 1000 * 60 * 60 
setTimeout(() => {
  window.location.reload();
}, rt); // 5 minutes

//make sure all days and months are double digits
function doubleDate(s){
  if (s.length != 2){
    s = '0' + s
  }
  return s
}

// Download CSV file with /api/data?date=YYYY-MM-DD
let hist = 3; // days of history to display
let dateArray = []
let dayDelta =  1000 * 60 *60 * 24
for (let dd = hist-1; dd >= 0; dd--){
  let ms = Date.now(); // milliseconds since January 1, 1970
  let d = new Date(ms - (dd * dayDelta));
  let month = doubleDate(String(d.getMonth() + 1));
  let day = doubleDate(String(d.getDate()));
  dateArray.push(String(d.getFullYear()) +'-'+ month +'-' + day);
}
//console.log(dateArray)

let endPt= "data?date="

let apiEndpoints = []

for (let e = 1; e < 9; e++){
  apiEndpoints.push('http://pi'+e+'.local:5000/api/'+endPt)
}

//apiEndpoints.push('http://kasa.local:5000/api/'+endPt)

async function fetchAndParseCSV(url) {
  const time = [];
  const temp = [];
  for (let d in dateArray){ 
    let fUrl = url+dateArray[d]
    const response = await fetch(fUrl);
    let text = await response.text();  
    const rows = text.trim().split('\n').map(row => row.split(','));

    const headers = rows[0];
    const timeIndex = headers.findIndex(h => h.toLowerCase().includes('datetime'));
    const tempIndex = headers.findIndex(h => h.includes('tempF'));

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      const date = new Date(row[timeIndex]);
      const t = parseFloat(row[tempIndex]);
      if (!isNaN(date) && !isNaN(t)) {
        time.push(date);
        temp.push(t);
      }
    }
  }

  console.log(temp)
  return { time, temp };
}

async function plotTempData() {
  const traces = [];

  for (let i = 0; i < apiEndpoints.length; i++) {
    try {
      const data = await fetchAndParseCSV(apiEndpoints[i]);
      traces.push({
        x: data.time,
        y: data.temp,
        mode: 'lines',
        name: `Sensor ${i + 1}`
      });
    } catch (error) {
      console.error(`Error fetching/parsing source ${i + 1}:`, error);
    }
  }

  Plotly.newPlot('plotT', traces, {
    title: 'Temperature (°F) Over Time',
    xaxis: { title: 'Time' },
    yaxis: { title: 'Temperature (°F)' }
  });
}

plotTempData();
