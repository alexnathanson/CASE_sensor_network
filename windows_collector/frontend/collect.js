const port = 5000;

let apiEndpoints = []

const today = new Date();
const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, '0'); // Months are 0-based
const dd = String(today.getDate()).padStart(2, '0');

const date = `${yyyy}-${mm}-${dd}`;
print(date)

for (let h = 1; h < 9; h++){
  apiEndpoints.push('http://pi' + h +".local:"+port+'/api/data?date'+date)
}

// async function fetchData(url) {
//   try {
//     const response = await fetch(url);
//     if (!response.ok) throw new Error(`Error: ${response.status}`);
//     return await response.json();
//   } catch (error) {
//     console.error(`Failed to fetch ${url}:`, error);
//     return null;
//   }
// }

async function fetchCSV(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Failed to fetch ${url}`);
    const csvText = await response.text();
    const parsed = Papa.parse(csvText, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true
    });
    return parsed.data;
  } catch (err) {
    console.error(err);
    return null;
  }
}

async function getAllData() {
  const results = await Promise.all(apiEndpoints.map(fetchCSV));
  return results.filter(data => data); // remove any null responses
}

function createChart(datasets) {
  const ctx = document.getElementById('timeseriesChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: datasets[0].map(point => point.time),  // Assuming aligned times
      datasets: datasets.map((data, idx) => ({
        label: `Series ${idx + 1}`,
        data: data.map(point => point.value),
        borderWidth: 2,
        fill: false
      }))
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: { display: true, text: 'Time' }
        },
        y: {
          title: { display: true, text: 'Value' }
        }
      }
    }
  });
}

(async function () {
  const rawData = await getAllData();

  // Example structure adjustment
  // Each item should be an array of objects: [{ time: '2024-01-01', value: 123 }, ...]
  const formattedData = rawData.map(apiData => 
    apiData.map(entry => ({
      time: entry.timestamp || entry.date || entry.time,
      value: entry.value || entry.amount || entry.count
    }))
  );

  createChart(formattedData);
})();
