document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-form');
    const resultsContainer = document.getElementById('results-container');
    const monitoringStatus = document.getElementById('monitoring-status');
    
    let isMonitoring = false;
    let pollingInterval = null;
    
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const companyName = document.getElementById('company-name').value;
        const keywords = document.getElementById('keywords').value;
        
        if (!companyName || !keywords) {
            alert('Please enter both company name and keywords');
            return;
        }
        
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    company_name: companyName,
                    keywords: keywords
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                startMonitoring();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
    
    function startMonitoring() {
        isMonitoring = true;
        monitoringStatus.textContent = 'Monitoring active';
        monitoringStatus.style.display = 'block';
        
        // Poll for new results every 5 seconds
        pollingInterval = setInterval(fetchResults, 5000);
    }
    
    async function fetchResults() {
        try {
            const response = await fetch('/api/results');
            const data = await response.json();
            
            if (data.success && data.results.length > 0) {
                displayResults(data.results);
            }
        } catch (error) {
            console.error('Error fetching results:', error);
        }
    }
    
    function displayResults(results) {
        results.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result-item';
            resultElement.innerHTML = `
                <h3>${result.channel}</h3>
                <p>${result.date}</p>
                <p>${result.content}</p>
                <a href="${result.url}" target="_blank">View on Telegram</a>
            `;
            resultsContainer.prepend(resultElement);
        });
    }
});