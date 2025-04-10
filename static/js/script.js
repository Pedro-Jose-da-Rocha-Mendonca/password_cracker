document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('passwordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const password = document.getElementById('password_input').value;
        const attackMethod = document.getElementById('attack_method').value;
        
        fetch('/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'password_input': password,
                'attack_method': attackMethod
            })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('resultsContainer').style.display = 'block';
            
            // Hide all simulation detail sections first
            document.querySelectorAll('.sim-details').forEach(el => el.style.display = 'none');
            
            // Display password strength information
            displayPasswordStrength(data);
            
            // Display simulation results based on method
            document.getElementById('simulationMethod').textContent = 
                `Method: ${data.simulation_result.method.replace('_', ' ')}`;
                
            if (data.simulation_result.method === 'brute_force') {
                displayBruteForceResults(data.simulation_result);
            } else if (data.simulation_result.method === 'dictionary_attack') {
                displayDictionaryResults(data.simulation_result);
            } else if (data.simulation_result.method === 'pattern_analysis') {
                displayPatternResults(data.simulation_result);
            }
            
            // Display mental models
            const mentalModelsHtml = data.mental_model_insights
                .map(insight => `<div class="mental-model">${insight}</div>`)
                .join('');
            document.getElementById('mentalModels').innerHTML = mentalModelsHtml;
            
            // Scroll to results
            document.getElementById('resultsContainer').scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred during the simulation.');
        });
    });
    
    // Function to display password strength information
    function displayPasswordStrength(data) {
        document.getElementById('passwordStrength').textContent = 
            `Your password is rated as: ${data.password_strength}`;
        
        const strengthMeter = document.getElementById('strengthMeter');
        strengthMeter.className = 'strength-value';
        strengthMeter.classList.add(data.password_strength.replace(' ', '-'));
        
        document.getElementById('passwordStats').innerHTML = 
            `Length: ${data.password_length} characters<br>` +
            `Contains uppercase letters: ${data.contains_uppercase ? 'Yes' : 'No'}<br>` +
            `Contains lowercase letters: ${data.contains_lowercase ? 'Yes' : 'No'}<br>` +
            `Contains numbers: ${data.contains_numbers ? 'Yes' : 'No'}<br>` +
            `Contains symbols: ${data.contains_symbols ? 'Yes' : 'No'}<br>` +
            `Entropy: ${data.entropy} bits`;
        
        document.getElementById('crackTime').textContent = 
            `Estimated time to crack: ${data.estimated_crack_time}`;
    }
    
    // Function to display brute force attack results
    function displayBruteForceResults(result) {
        const bruteForceSection = document.getElementById('bruteForceSim');
        bruteForceSection.style.display = 'block';
        
        // Display character sets
        let charSetsHtml = '<h5>Character Sets Used</h5><ul>';
        result.character_sets_used.forEach(set => {
            charSetsHtml += `<li>${set.type}: ${set.count} characters</li>`;
        });
        charSetsHtml += `</ul>`;
        charSetsHtml += `<p>Total character space: ${result.character_space_size}</p>`;
        charSetsHtml += `<p>Total possible combinations: ${result.possible_combinations.toExponential(2)}</p>`;
        charSetsHtml += `<p>Password entropy: ${result.entropy_bits} bits</p>`;
        bruteForceSection.querySelector('.char-sets').innerHTML = charSetsHtml;
        
        // Display sample attempts
        let attemptsHtml = '<div class="attempts-table">';
        attemptsHtml += '<div class="attempt-row header"><div>Attempt</div><div>Type</div><div>Result</div></div>';
        
        result.sample_attempts.forEach((attempt, index) => {
            const isSuccess = index === result.sample_attempts.length - 1;
            attemptsHtml += `
                <div class="attempt-row ${isSuccess ? 'success' : ''}">
                    <div>${attempt}</div>
                    <div>${result.attempt_types[index]}</div>
                    <div>${isSuccess ? 'Success' : 'Failed'}</div>
                </div>
            `;
        });
        attemptsHtml += '</div>';
        bruteForceSection.querySelector('.attempts-list').innerHTML = attemptsHtml;
        
        // Display time estimates
        let estimatesHtml = '<div class="estimates-table">';
        estimatesHtml += '<div class="estimate-row header"><div>Search Space %</div><div>Time</div></div>';
        
        Object.entries(result.time_estimates).forEach(([percentage, time]) => {
            estimatesHtml += `
                <div class="estimate-row">
                    <div>${percentage}</div>
                    <div>${time}</div>
                </div>
            `;
        });
        estimatesHtml += '</div>';
        bruteForceSection.querySelector('.estimates-grid').innerHTML = estimatesHtml;
        
        // Display hardware comparison
        let hardwareHtml = '<div class="hardware-table">';
        hardwareHtml += '<div class="hardware-row header"><div>Hardware</div><div>Time</div></div>';
        
        Object.entries(result.gpu_comparison).forEach(([hardware, time]) => {
            const hardwareName = hardware.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            hardwareHtml += `
                <div class="hardware-row">
                    <div>${hardwareName}</div>
                    <div>${time}</div>
                </div>
            `;
        });
        hardwareHtml += '</div>';
        bruteForceSection.querySelector('.hardware-grid').innerHTML = hardwareHtml;
        
        // Basic description for simulation details
        document.getElementById('simulationDetails').innerHTML = `
            <p>Brute force attacks try every possible combination of characters until the password is found.</p>
            <p>With a character space of ${result.character_space_size} and password length of ${result.password_length},
            there are ${result.possible_combinations.toExponential(2)} possible combinations to check.</p>
        `;
    }
    
    // Function to display dictionary attack results
    function displayDictionaryResults(result) {
        const dictionarySection = document.getElementById('dictionarySim');
        dictionarySection.style.display = 'block';
        
        // Basic information
        let dictInfoHtml = `
            <p>Found in common password list: <strong>${result.found_in_common_list ? 'Yes' : 'No'}</strong></p>
            <p>Susceptible to wordlist attack: <strong>${result.susceptible_to_wordlist ? 'Yes' : 'No'}</strong></p>
            <p>Estimated dictionary needed: <strong>${result.estimated_dictionaries_needed}</strong></p>
        `;
        dictionarySection.querySelector('.dict-info').innerHTML = dictInfoHtml;
        
        // Similar passwords
        let similarHtml = '';
        if (result.similar_passwords && result.similar_passwords.length > 0) {
            similarHtml = result.similar_passwords.map(p => 
                `<li>${p.password} (${p.similarity} similar)</li>`
            ).join('');
        } else {
            similarHtml = '<li>No similar passwords found in common lists</li>';
        }
        dictionarySection.querySelector('.similar-list').innerHTML = similarHtml;
        
        // Attack progression
        let progressHtml = '<div class="progress-table">';
        progressHtml += '<div class="progress-row header"><div>Attempt</div><div>Type</div><div>Result</div></div>';
        
        if (result.attack_progression) {
            result.attack_progression.forEach(step => {
                const isSuccess = step.result === 'success';
                progressHtml += `
                    <div class="progress-row ${isSuccess ? 'success' : ''}">
                        <div>${step.attempt}</div>
                        <div>${step.type}</div>
                        <div>${step.result}</div>
                    </div>
                `;
            });
        }
        progressHtml += '</div>';
        dictionarySection.querySelector('.progress-steps').innerHTML = progressHtml;
        
        // Dictionary sizes
        let dictSizesHtml = '<div class="dict-table">';
        dictSizesHtml += '<div class="dict-row header"><div>Dictionary Type</div><div>Size</div></div>';
        
        Object.entries(result.dictionary_sizes).forEach(([dict, size]) => {
            dictSizesHtml += `
                <div class="dict-row">
                    <div>${dict.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</div>
                    <div>${size.toLocaleString()}</div>
                </div>
            `;
        });
        dictSizesHtml += '</div>';
        dictionarySection.querySelector('.dict-sizes').innerHTML = dictSizesHtml;
        
        // Pattern variations
        let variationsHtml = '<h5>Pattern Variations Checked</h5><ul>';
        result.variations_checked.forEach(variation => {
            variationsHtml += `<li>${variation}</li>`;
        });
        variationsHtml += '</ul>';
        
        // Basic description for simulation details
        document.getElementById('simulationDetails').innerHTML = `
            <p>Dictionary attacks use lists of common passwords and words, along with variations.</p>
            ${variationsHtml}
        `;
    }
    
    // Function to display pattern analysis results
    function displayPatternResults(result) {
        const patternSection = document.getElementById('patternSim');
        patternSection.style.display = 'block';
        
        // Pattern overview
        const riskLevel = result.risk_assessment;
        const riskClass = riskLevel === 'High' ? 'high-risk' : 
                         (riskLevel === 'Medium' ? 'medium-risk' : 'low-risk');
        
        let overviewHtml = `
            <p>Overall risk assessment: <span class="risk-badge ${riskClass.toLowerCase()}">${riskLevel}</span></p>
            <p>Patterns detected: ${result.patterns_detected.length}</p>
        `;
        patternSection.querySelector('.pattern-overview').innerHTML = overviewHtml;
        
        // Pattern details grid
        let patternsGridHtml = '';
        
        if (result.pattern_details) {
            Object.entries(result.pattern_details).forEach(([type, details]) => {
                let detailContent = '';
                
                if (details.found) {
                    detailContent = `<p>Pattern: ${details.pattern}</p>`;
                } else if (details.count) {
                    detailContent = `<p>Count: ${details.count}</p>`;
                } else if (details.sequence) {
                    detailContent = `<p>Sequence: ${details.sequence}</p>`;
                } else if (details.patterns) {
                    detailContent = `<p>${details.patterns.join(', ')}</p>`;
                } else if (details.message) {
                    detailContent = `<p>${details.message}</p>`;
                }
                
                const riskClass = details.risk && details.risk.toLowerCase().includes('high') ? 'high-risk' : 
                                (details.risk && details.risk.toLowerCase().includes('medium') ? 'medium-risk' : 'low-risk');
                
                patternsGridHtml += `
                    <div class="pattern-card ${riskClass}">
                        <h6>${type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</h6>
                        ${detailContent}
                        ${details.risk ? `<div class="risk-level">${details.risk}</div>` : ''}
                    </div>
                `;
            });
        }
        
        patternSection.querySelector('.patterns-grid').innerHTML = patternsGridHtml;
        
        // Character distribution
        let distributionHtml = '<div class="dist-chart">';
        
        if (result.character_distribution) {
            const total = Object.values(result.character_distribution).reduce((sum, val) => sum + val, 0);
            
            Object.entries(result.character_distribution).forEach(([type, count]) => {
                const percentage = (count / total * 100).toFixed(1);
                distributionHtml += `
                    <div class="dist-bar-container">
                        <div class="dist-label">${type}</div>
                        <div class="dist-bar-wrapper">
                            <div class="dist-bar" style="width: ${percentage}%"></div>
                        </div>
                        <div class="dist-value">${count} (${percentage}%)</div>
                    </div>
                `;
            });
        }
        
        distributionHtml += '</div>';
        patternSection.querySelector('.distribution-chart').innerHTML = distributionHtml;
        
        // Risk assessment
        const entropyPerChar = result.password_layout ? result.password_layout.entropy_per_character.toFixed(2) : 0;
        
        let riskHtml = `
            <div class="risk-meter ${riskClass}">
                <div class="risk-level">${riskLevel}</div>
                <div class="risk-description">
                    <p>Based on detected patterns and character distribution.</p>
                    <p>Entropy per character: ${entropyPerChar} bits</p>
                </div>
            </div>
        `;
        patternSection.querySelector('.risk-indicator').innerHTML = riskHtml;
        
        // Basic description for simulation details
        document.getElementById('simulationDetails').innerHTML = `
            <p>Pattern analysis looks for common structures and predictable sequences in passwords.</p>
            <p>Patterns detected: ${result.patterns_detected.map(p => `<span class="pattern-tag">${p}</span>`).join(' ')}</p>
        `;
    }
    
    // Educational section interactivity
    const toggleButton = document.getElementById('toggleSimple');
    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            const simpleTest = document.getElementById('simpleTest');
            simpleTest.classList.toggle('hidden-section');
            
            if (!simpleTest.classList.contains('hidden-section')) {
                toggleButton.textContent = 'Hide Test';
            } else {
                toggleButton.textContent = 'Try a Simple Test';
            }
        });
    }
    
    // Add event listeners to checkboxes
    const checkboxes = document.querySelectorAll('.interactive-checklist input[type="checkbox"]');
    const resultText = document.getElementById('checklist-result');
    
    if (checkboxes.length > 0 && resultText) {
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                let anyChecked = false;
                checkboxes.forEach(cb => {
                    if (cb.checked) {
                        anyChecked = true;
                    }
                });
                
                if (anyChecked) {
                    resultText.classList.remove('hidden-section');
                } else {
                    resultText.classList.add('hidden-section');
                }
            });
        });
    }
});
