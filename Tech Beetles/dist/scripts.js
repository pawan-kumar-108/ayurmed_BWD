const remediesContainer = document.getElementById('remedies-container');
const modal = document.getElementById('remedy-modal');
const modalContent = document.getElementById('modal-content');

// Sample data (replace with your own Ayurveda remedies data)
const remediesData = [
    { id: 1, title: 'Remedy 1', description: 'Details about Remedy 1', image: 'remedy1.jpg' },
    { id: 2, title: 'Remedy 2', description: 'Details about Remedy 2', image: 'remedy2.jpg' },
    // Add more remedies as needed
];

// Function to create a remedy card
function createRemedyCard(remedy) {
    const remedyCard = document.createElement('div');
    remedyCard.classList.add('remedy-card');
    remedyCard.innerHTML = `<img src="${remedy.image}" alt="${remedy.title}">
                            <h3>${remedy.title}</h3>`;
    remedyCard.addEventListener('click', () => openModal(remedy));
    return remedyCard;
}

// Function to populate remedies
function populateRemedies() {
    remediesData.forEach(remedy => {
        const remedyCard = createRemedyCard(remedy);
        remediesContainer.appendChild(remedyCard);
    });
}

// Function to open modal with remedy details
function openModal(remedy) {
    modalContent.innerHTML = `<img src="${remedy.image}" alt="${remedy.title}">
                              <h2>${remedy.title}</h2>
                              <p>${remedy.description}</p>`;
    modal.style.display = 'flex';
}

// Function to close modal
function closeModal() {
    modal.style.display = 'none';
}

// Populate remedies on page load
window.onload = populateRemedies;
