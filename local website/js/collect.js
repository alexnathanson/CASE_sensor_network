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

const resultsContainer = document.getElementById('results');

async function fetchAndDisplayData() {
  resultsContainer.innerHTML = ''; // Clear loading text

  const fetchPromises = apiEndpoints.map(async (url) => {
    let retries = 3;
    let delay = 500;
    for (let attempt = 1; attempt <= retries; attempt++) {
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Status ${response.status}`);
        const data = await response.json();

        const el = document.createElement('div');
        el.className = 'result';
        el.innerHTML = `<strong>${url}</strong><pre>${JSON.stringify(data, null, 2)}</pre>`;
        resultsContainer.appendChild(el);
        break;
      } catch (error) {
          if (attempt === retries) {
            const errorEl = document.createElement('div');
            errorEl.className = 'result';
            errorEl.innerHTML = `<strong>${url}</strong><p style="color:red;">Error: ${error.message}</p>`;
            resultsContainer.appendChild(errorEl);
            throw error;
          } else{
            //console.log(attempt + ": " + url)
            await new Promise(r => setTimeout(r, delay*attempt));
          }
      }
    }
  });

  await Promise.all(fetchPromises);
}

fetchAndDisplayData();