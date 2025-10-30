document.addEventListener('DOMContentLoaded', function() {
    const simulationForm = document.getElementById('simulationForm');
    const simulateBtn = document.getElementById('simulateBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsContainer = document.getElementById('resultsContainer');
    const errorContainer = document.getElementById('errorContainer');
    const intensitySlider = document.getElementById('intensity');
    const intensityValue = document.getElementById('intensityValue');

    // Update intensity value display
    intensitySlider.addEventListener('input', function() {
        intensityValue.textContent = this.value;
    });

    // Form submission
    simulationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        runSimulation();
    });

    async function runSimulation() {
        // Show loading
        simulateBtn.disabled = true;
        loadingSpinner.style.display = 'block';
        resultsContainer.style.display = 'none';
        errorContainer.style.display = 'none';

        // Get form data
        const formData = {
            city: document.getElementById('city').value,
            manipulation_type: document.getElementById('manipulationType').value,
            intensity: parseFloat(document.getElementById('intensity').value),
            duration: parseInt(document.getElementById('duration').value)
        };

        try {
            const response = await fetch('/api/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'Simulation failed');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        } finally {
            // Hide loading
            simulateBtn.disabled = false;
            loadingSpinner.style.display = 'none';
        }
    }

    function displayResults(data) {
        // Show current weather
        displayCurrentWeather(data.current_weather);

        // Show charts
        document.getElementById('chartsContainer').innerHTML = data.charts_html;

        // Show heatmap
        document.getElementById('heatmapContainer').innerHTML = data.heatmap_html;

        // Show AI summary
        document.getElementById('aiSummary').innerHTML = formatText(data.ai_summary);

        // Show report
        document.getElementById('reportContainer').innerHTML = data.report_html;

        // Show results
        resultsContainer.style.display = 'block';

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }

    function displayCurrentWeather(weather) {
        const content = `
            <div class="row text-center">
                <div class="col-6">
                    <i class="fas fa-thermometer-half fa-2x text-danger"></i>
                    <p class="mb-1"><strong>${weather.temperature}°C</strong></p>
                    <small class="text-muted">Temperature</small>
                </div>
                <div class="col-6">
                    <i class="fas fa-tint fa-2x text-info"></i>
                    <p class="mb-1"><strong>${weather.humidity}%</strong></p>
                    <small class="text-muted">Humidity</small>
                </div>
            </div>
            <div class="row text-center mt-2">
                <div class="col-6">
                    <i class="fas fa-cloud-rain fa-2x text-primary"></i>
                    <p class="mb-1"><strong>${weather.rainfall}mm</strong></p>
                    <small class="text-muted">Rainfall</small>
                </div>
                <div class="col-6">
                    <i class="fas fa-cloud fa-2x text-secondary"></i>
                    <p class="mb-1"><strong>${weather.clouds}%</strong></p>
                    <small class="text-muted">Clouds</small>
                </div>
            </div>
            <p class="text-center mt-2"><em>${weather.description}</em></p>
        `;

        document.getElementById('currentWeatherContent').innerHTML = content;
        document.getElementById('currentWeatherCard').style.display = 'block';
    }

    function formatText(text) {
        // Convert line breaks to paragraphs
        return text.split('\n').map(paragraph => {
            if (paragraph.trim()) {
                return `<p>${paragraph.trim()}</p>`;
            }
            return '';
        }).join('');
    }

    function showError(message) {
        errorContainer.textContent = message;
        errorContainer.style.display = 'block';
    }

    // Load weather options on page load
    loadWeatherOptions();

    async function loadWeatherOptions() {
        try {
            const response = await fetch('/api/weather-options');
            const options = await response.json();

            // Update manipulation type select with descriptions
            const select = document.getElementById('manipulationType');
            select.innerHTML = '';

            for (const [key, value] of Object.entries(options)) {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = `${key.charAt(0).toUpperCase() + key.slice(1)} - ${value.description}`;
                select.appendChild(option);
            }
        } catch (error) {
            console.error('Failed to load weather options:', error);
        }
    }

    // Add some interactive features
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
