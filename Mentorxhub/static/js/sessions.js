// MentorXHub - Sessions Logic

document.addEventListener('DOMContentLoaded', () => {
    // Logic to load sessions if on dashboard
});

function bookSession(mentorId, timeSlot) {
    console.log(`Booking session with mentor ${mentorId} at ${timeSlot}`);
    // API call to book session
    alert('Session booked successfully!');
}

function cancelSession(sessionId) {
    if (confirm('Are you sure you want to cancel this session?')) {
        console.log(`Cancelling session ${sessionId}`);
        // API call to cancel
    }
}
