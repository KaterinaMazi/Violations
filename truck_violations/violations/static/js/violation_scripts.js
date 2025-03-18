document.addEventListener('DOMContentLoaded', function() {
    const previousInspectionInput = document.getElementById(formIds.previousInspection);
    const currentInspectionInput = document.getElementById(formIds.currentInspection);
    const daysDifferenceOutput = document.getElementById('days_difference');
    const circulationInput = document.getElementById(formIds.circulationNumber);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;


    function calculateDaysDifference() {
        if (!previousInspectionInput.value) {
            daysDifferenceOutput.value = '-';
            return;
        }

        const previousDate = previousInspectionInput.value;
        const currentDate = currentInspectionInput.value;

        const url = `${calculateDaysDifferenceUrl}?previous_date=${encodeURIComponent(previousDate)}&current_date=${encodeURIComponent(currentDate)}`;

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error); // Εμφάνιση μηνύματος λάθους
                daysDifferenceOutput.value = 'Σφάλμα';
            } else {
                daysDifferenceOutput.value = data.days_difference;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            daysDifferenceOutput.value = 'Σφάλμα';
        });
    }


    /**
     * Φιλτράρει και επαναριθμεί τον πίνακα παραβάσεων με βάση την αναζήτηση
     */
    function handleViolationSearch() {
        const searchInput = document.getElementById('violationSearchInput');
        if (!searchInput) return;

        searchInput.addEventListener('input', function() {
            const searchText = this.value.toLowerCase().trim();
            const table = document.getElementById('violationsTable');
            if (!table) return;

            const rows = table.querySelectorAll('tbody tr');
            let visibleCount = 0;

            rows.forEach(function(row) {
                const codeCell = row.querySelector('td:nth-child(2)');
                if (codeCell) {
                    const code = codeCell.textContent || codeCell.innerText;
                    if (code.toLowerCase().includes(searchText)) {
                        row.style.display = '';
                        visibleCount++;
                        const indexCell = row.querySelector('td:first-child');
                        if (indexCell) {
                            indexCell.textContent = visibleCount;
                        }
                    } else {
                        row.style.display = 'none';
                    }
                }
            });
        });
    }


    /**
     * Ρυθμίζει τη λειτουργία εκτύπωσης
     */
    function setupPrintButton() {
        const printButton = document.getElementById('printButton');
        if (printButton) {
            printButton.addEventListener('click', function() {
                window.print();
            });
        }
    }


    /**
     * Διαχειρίζεται την αυτόματη αναζήτηση με βάση τον αριθμό κυκλοφορίας
     */
    function setupCirculationLookup() {
        if (!circulationInput) return;

        circulationInput.addEventListener('blur', function() {
            if (this.value) {
                window.location.href = `?circulation_number=${encodeURIComponent(this.value)}`;
            }
        });


        circulationInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Αποτρέπουμε την υποβολή της φόρμας
                if (this.value) {
                    window.location.href = `?circulation_number=${encodeURIComponent(this.value)}`;
                }
            }
        });
    }


    if (previousInspectionInput && currentInspectionInput) {
        previousInspectionInput.addEventListener('change', calculateDaysDifference);
        currentInspectionInput.addEventListener('change', calculateDaysDifference);

        if (previousInspectionInput.value && currentInspectionInput.value) {
            calculateDaysDifference();
        }
    }

    handleViolationSearch();
    setupPrintButton();
    setupCirculationLookup();
});