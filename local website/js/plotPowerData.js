let apiEndpointK = 'http://kasa.local:5000/api/data?date='

async function fetchAndParseCSV_power(url) {
  const time = [];
  const power1 = [];
  const power2 = [];
  const power3 = [];
  const power4 = [];
  for (let d in dateArray){ 
    let fUrl = url+dateArray[d]
    const response = await fetch(fUrl);
    let text = await response.text();  
    const rows = text.trim().split('\n').map(row => row.split(','));

    const headers = rows[0];
    console.log(headers)
    const timeIndex = headers.findIndex(h => h.toLowerCase().includes('datetime'));
    const power1Index = headers.findIndex(h => h.includes('kasa1_W'));
    const power2Index = headers.findIndex(h => h.includes('kasa2_W'));
    const power3Index = headers.findIndex(h => h.includes('kasa3_W'));
    const power4Index = headers.findIndex(h => h.includes('kasa4_W'));

    for (let i = 1; i < rows.length; i++) {
      const row = rows[i];
      const date = new Date(row[timeIndex]);
      const p1 = parseFloat(row[power1Index]);
      const p2 = parseFloat(row[power2Index]);
      const p3 = parseFloat(row[power3Index]);
      const p4 = parseFloat(row[power4Index]);
      
      if (!isNaN(date)) {
        time.push(date);
        if (!isNaN(p1)) {
          power1.push(p1);
        } else {
          power1.push(0);
        }

        if (!isNaN(p2)) {
          power2.push(p2);
        } else {
          power2.push(0);
        }

        if (!isNaN(p3)) {
          power3.push(p3);
        } else {
          power3.push(0);
        }

        if (!isNaN(p4)) {
          power4.push(p4);
        } else {
          power4.push(0);
        }
      }
      
    }
  }

  return { time, power1,power2,power3,power4 };
}

async function plotPowerData() {
  const traces = [];

  try {
    const data = await fetchAndParseCSV_power(apiEndpointK);
    for (let k=0; k < 4; k++){
      traces.push({
        x: data.time,
        y: data[`power${k+1}`],
        mode: 'lines',
        name: `Plug ${k + 1}`
      });
    }
  } catch (error) {
    console.error(`Error fetching/parsing source:`, error);
  }

  Plotly.newPlot('plotP', traces, {
    title: 'Power (Watts) Over Time',
    xaxis: { title: 'Time' },
    yaxis: { title: 'Power (Watts)' }
  });
}

plotPowerData();
