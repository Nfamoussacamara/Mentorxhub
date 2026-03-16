// MentorXHub - Reviews Logic

document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('reviewForm');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Mock submission
            console.log('Submitting review...');

            // TODO: Replace with actual API call
            // await fetch('/api/reviews/', { method: 'POST', ... });

            alert('Review submitted successfully!');
            window.location.href = 'dashboard-mentee.html';
        });
    }
});
