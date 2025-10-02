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
let hist = 1; // days of history to display
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

async function fetchAndParseCSV(url,s) {
  const time = [];
  const temp = [];
  for (let d in dateArray){ 
    let fUrl = url+dateArray[d]
    const response = await fetch(fUrl);
    let text = await response.text();  
    const rows = text.trim().split('\n').map(row => row.split(','));

    const headers = rows[0];
    const timeIndex = headers.findIndex(h => h.toLowerCase().includes('datetime'));

    let tempIndex;
    if (s == 'f'){
       tempIndex = headers.findIndex(h => h.includes('tempF'));
    } else if (s == 'c'){
      tempIndex = headers.findIndex(h => h.includes('tempC'));
    } else if (s == 'ccal'){
      tempIndex = headers.findIndex(h => h.includes('tempC_offset'));
    } else if (s == 'h'){
      tempIndex = headers.findIndex(h => h.includes('humidity'));
    }

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

  return { time, temp };
}

async function plotTempData(s) {
  const traces = [];
  //let allData = []
  for (let i = 0; i < apiEndpoints.length; i++) {
    try {
      const data = await fetchAndParseCSV(apiEndpoints[i],s);
      //allData.push(data)
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

  //get averages
  let avgData = []
  let avgTime = []

  console.log(traces)
  for (let a=0;a<traces[0].x.length;a++){// for each reading
    av = 0
    for (let d=0;d<traces.length;d++){// for each device
      av = av + traces[d]['y'][a]
    }
    avgData.push(av/traces.length)
    avgTime.push(traces[0]['x'][a])
  }
  traces.push({
        x: avgTime,
        y: avgData,
        mode: 'lines',
        name: `Rough Average`,
        line: {color: 'black'}});

  if (s == 'f'){
    t = 'Temperature (°F)'
    p = 'plotF'
  } else if (s == 'c'){
    t = 'Temperature (°C)'
    p = 'plotC'
  } else if (s == 'ccal'){
    t = 'Temperature (°C calibrated)'
    p = 'plotCCal'
  } else if (s == 'h'){
    t = 'Humidity'
    p = 'plotH'
  }

  Plotly.newPlot(p, traces, {
    title: t + ' Over Time',
    xaxis: { title: 'Time' },
    yaxis: { title: t }
  });
}

plotTempData('f');
plotTempData('c');
plotTempData('ccal');
plotTempData('h');
