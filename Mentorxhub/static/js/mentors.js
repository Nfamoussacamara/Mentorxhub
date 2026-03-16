// MentorXHub - Mentors Logic

document.addEventListener('DOMContentLoaded', () => {
    const mentorsListContainer = document.getElementById('mentorsList');

    if (mentorsListContainer) {
        // fetchMentors();
    }
});

async function fetchMentors() {
    try {
        const response = await fetch('/mentoring/api/mentors/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const mentors = await response.json();
        renderMentors(mentors);
    } catch (error) {
        console.error('Error fetching mentors:', error);
        // Fallback to empty list or show error
        renderMentors([]);
    }
}

function renderMentors(mentors) {
    const container = document.getElementById('mentorsList');
    if (!container) return;

    container.innerHTML = mentors.map(mentor => `
        <div class="card flex gap-4 items-center fade-in">
            <div style="width: 60px; height: 60px; background-color: #eee; border-radius: 50%;"></div>
            <div>
                <h4>${mentor.name}</h4>
                <p class="text-sm text-muted">${mentor.title}</p>
                <button onclick="viewProfile(${mentor.id})" class="btn btn-sm btn-outline mt-4" style="padding: 0.25rem 0.75rem; font-size: 0.875rem;">View Profile</button>
            </div>
        </div>
    `).join('');
}

function viewProfile(id) {
    console.log('View profile:', id);
    window.location.href = `mentor-profile.html?id=${id}`;
}
