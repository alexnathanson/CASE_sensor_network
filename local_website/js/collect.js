// Refresh every 5 minutes (300000 milliseconds)
setTimeout(() => {
  window.location.reload();
}, 300000); // 5 minutes

const params = new URLSearchParams(window.location.search);
const value = params.get('data'); // replace 'yourParam' with the actual key
console.log(value)

let endPt= "data?date=now"
if (value == "sensor"){
  endPt = "data?date=now"
} else if (value == "health"){
 endPt = "health"
}

let apiEndpoints = []

for (let e = 1; e < 9; e++){
  apiEndpoints.push('http://pi'+e+'.local:5000/api/'+endPt)
}
apiEndpoints.push('http://kasa.local:5000/api/'+endPt)

//const resultsContainer = document.getElementById('results');

const tableBody = document.querySelector("#resultsTable tbody");

function getHostOrder(url) {
  const match = url.match(/pi(\d+)\.local/);
  if (match) return parseInt(match[1]);
  if (url.includes("kasa")) return 999;
  return 1000; // fallback for unknown hosts
}

async function fetchAndDisplayData() {
  //resultsContainer.innerHTML = ''; // Clear loading text
  tableBody.innerHTML = ''; // Clear existing table rows
  const results = [];

  const fetchPromises = apiEndpoints.map(async (url) => {
    let retries = 3;
    let delay = 500;
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Status ${response.status}`);
        const data = await response.json();
        results.push({ url, data, error: null });
        // const row = document.createElement('tr');
        // row.innerHTML = `
        //   <td>${url}</td>
        //   <td><pre>${JSON.stringify(data, null, 2)}</pre></td>
        // `;
        // tableBody.appendChild(row);
        break;
      } catch (error) {
        if (attempt === retries) {
          // const errorRow = document.createElement('tr');
          // errorRow.innerHTML = `
          //   <td>${url}</td>
          //   <td style="color:red;">Error: ${error.message}</td>
          // `;
          // tableBody.appendChild(errorRow);
          results.push({ url, data: null, error: error.message });
        } else {
          await new Promise(r => setTimeout(r, delay * attempt));
        }
      }
    }
  });

  await Promise.all(fetchPromises);

  // Sort by host order
  results.sort((a, b) => getHostOrder(a.url) - getHostOrder(b.url));

  // Render table
  results.forEach(({ url, data, error }) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${url}</td>
      <td>${error
        ? `<span style="color:red;">Error: ${error}</span>`
        : `<pre>${JSON.stringify(data, null, 2)}</pre>`}</td>
    `;
    tableBody.appendChild(row);
  });
}

fetchAndDisplayData();