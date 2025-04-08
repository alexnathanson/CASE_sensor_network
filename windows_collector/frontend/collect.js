
let apiEndpoints = []

for (let e = 1; e < 9; e++){
  apiEndpoints.push('http://pi'+e+'.local:5000/api/data?date=now')
}

const resultsContainer = document.getElementById('results');

async function fetchAndDisplayData() {
  resultsContainer.innerHTML = ''; // Clear loading text

  const fetchPromises = apiEndpoints.map(async (url) => {
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error(`Status ${response.status}`);
      const data = await response.json();

      const el = document.createElement('div');
      el.className = 'result';
      el.innerHTML = `<strong>${url}</strong><pre>${JSON.stringify(data, null, 2)}</pre>`;
      resultsContainer.appendChild(el);
    } catch (error) {
      const errorEl = document.createElement('div');
      errorEl.className = 'result';
      errorEl.innerHTML = `<strong>${url}</strong><p style="color:red;">Error: ${error.message}</p>`;
      resultsContainer.appendChild(errorEl);
    }
  });

  await Promise.all(fetchPromises);
}

fetchAndDisplayData();