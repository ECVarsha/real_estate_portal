// dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Toggle between agent and user views
    const toggleViews = document.querySelectorAll('.view-toggle');
    if (toggleViews.length > 0) {
        toggleViews.forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.view-section').forEach(section => {
                    section.style.display = 'none';
                });
                document.getElementById(this.dataset.target).style.display = 'block';
            });
        });
    }

    // Initialize any charts or stats (placeholder)
    if (typeof Chart !== 'undefined') {
        const ctx = document.getElementById('statsChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Properties', 'Inquiries', 'Favorites'],
                    datasets: [{
                        label: 'Your Activity',
                        data: [12, 8, 5],
                        backgroundColor: [
                            'rgba(90, 111, 148, 0.7)',
                            'rgba(213, 191, 196, 0.7)',
                            'rgba(70, 63, 55, 0.7)'
                        ],
                        borderColor: [
                            'rgb(90, 111, 148)',
                            'rgb(213, 191, 196)',
                            'rgb(70, 63, 55)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }

    // Handle favorite property removal
    document.querySelectorAll('.remove-favorite').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const propertyId = this.dataset.id;
            if (confirm('Remove this property from favorites?')) {
                // In a real app, this would make an API call
                this.closest('.favorite-item').remove();
            }
        });
    });

    // Mark inquiries as contacted
    document.querySelectorAll('.mark-contacted').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const inquiryId = this.dataset.id;
            // In a real app, this would make an API call
            this.textContent = '✓ Contacted';
            this.classList.add('contacted');
        });
    });
});