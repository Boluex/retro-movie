// Define the base URL for your API
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Updated Cartoon interface to match backend schema
interface Cartoon {
    id: number;
    title: string;
    year: number;
    description: string;
    poster_url: string;
    hero_image_url?: string | null; // Allow null from backend
    video_url?: string | null;    // Allow null
    created_at: string;
    updated_at: string;
}

// Movie Request Data interface
interface MovieRequestData {
    movie_name: string;
    user_email: string;
}

// --- DOM Elements ---
// Movie Request Modal
const movieRequestModal = document.getElementById('movieRequestModal') as HTMLElement;
const movieRequestBtn = document.getElementById('movieRequestBtn');
const movieRequestModalCloseBtn = document.getElementById('movieRequestModalCloseBtn'); // Corrected ID
const movieRequestForm = document.getElementById('movieRequestForm') as HTMLFormElement;

// Video Player Modal
const videoPlayerModal = document.getElementById('videoPlayerModal') as HTMLElement;
const cartoonPlayer = document.getElementById('cartoonPlayer') as HTMLVideoElement;
const videoPlayerModalHeading = document.getElementById('videoPlayerModalHeading') as HTMLElement; // Corrected ID
const videoModalCloseBtn = document.getElementById('videoModalCloseBtn');

// Notification
const notificationElement = document.getElementById('notification') as HTMLElement;

// --- Initialize Page ---
document.addEventListener('DOMContentLoaded', () => {
    async function initializePage() {
        try {
            await populateHeroSection();
            await populateCartoonRows();
            setupEventListeners();
            updateCopyrightYear();
        } catch (error) {
            console.error("Error initializing page:", error);
            showNotification("Could not initialize the page. Please try refreshing.", true);
        }
    }
    initializePage();
});

// --- Data Fetching and Population ---
async function populateHeroSection() {
    const heroSection = document.getElementById('heroSection') as HTMLElement;
    const heroPoster = document.getElementById('heroPoster') as HTMLImageElement;
    const heroTitle = document.getElementById('heroTitle') as HTMLElement;
    const heroDescription = document.getElementById('heroDescription') as HTMLElement;
    const watchButton = heroSection?.querySelector('.watch-button') as HTMLButtonElement;

    try {
        const response = await fetch(`${API_BASE_URL}/cartoons/featured`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} for featured cartoon`);
        }
        const featuredCartoon: Cartoon | null = await response.json();

        if (heroSection && featuredCartoon) {
            heroSection.style.backgroundImage = `url('${featuredCartoon.hero_image_url || featuredCartoon.poster_url}')`;
            if (heroPoster) {
                heroPoster.src = featuredCartoon.poster_url;
                heroPoster.alt = `${featuredCartoon.title} Poster`;
            }
            if (heroTitle) heroTitle.textContent = featuredCartoon.title;
            if (heroDescription) heroDescription.textContent = `${featuredCartoon.description.substring(0, 120)}... (${featuredCartoon.year})`;

            if (watchButton) {
                watchButton.style.display = 'inline-block'; // Make sure it's visible
                watchButton.setAttribute('aria-label', `Watch ${featuredCartoon.title}`);
                watchButton.onclick = () => {
                    if (featuredCartoon.video_url) {
                        openVideoPlayer(featuredCartoon.video_url, featuredCartoon.title);
                    } else {
                        showNotification(`Video for ${featuredCartoon.title} is not available yet.`, true);
                    }
                };
            }
        } else { // Handles null or if elements are missing
            if (heroTitle) heroTitle.textContent = "No Featured Cartoon Available";
            if (heroDescription) heroDescription.textContent = "Please check back later.";
            if (heroPoster) heroPoster.src = "https://via.placeholder.com/150x220.png?text=Not+Available"; // Fallback image
            if (watchButton) watchButton.style.display = 'none';
        }
    } catch (error) {
        console.error('Failed to load featured cartoon:', error);
        if (heroTitle) heroTitle.textContent = "Error Loading Featured";
        if (heroDescription) heroDescription.textContent = "Could not fetch featured content.";
        if (heroPoster) heroPoster.src = "https://via.placeholder.com/150x220.png?text=Error"; // Error image
        if (watchButton) watchButton.style.display = 'none';
    }
}

function createCartoonCard(cartoon: Cartoon): HTMLElement {
    const card = document.createElement('div');
    card.className = 'cartoon-card';
    card.setAttribute('role', 'button'); // Make it interactive
    card.setAttribute('tabindex', '0'); // Make it focusable
    card.setAttribute('aria-label', `Play ${cartoon.title}`);

    card.innerHTML = `
        <img src="${cartoon.poster_url}" alt="${cartoon.title} Poster" loading="lazy" onerror="this.onerror=null;this.src='https://via.placeholder.com/180x250.png?text=Image+Missing';">
        <div class="cartoon-card-info">
            <h3>${cartoon.title}</h3>
            <p>${cartoon.year}</p>
        </div>
    `;
    const playAction = () => {
        if (cartoon.video_url) {
            openVideoPlayer(cartoon.video_url, cartoon.title);
        } else {
            showNotification(`Video for ${cartoon.title} is not available yet.`, true);
        }
    };
    card.addEventListener('click', playAction);
    card.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault(); // Prevent page scroll on space
            playAction();
        }
    });
    return card;
}

async function populateCartoonRow(rowId: string, endpoint: string) {
    const cartoonRow = document.getElementById(rowId);
    if (!cartoonRow) {
        console.warn(`Cartoon row with ID '${rowId}' not found.`);
        return;
    }
    cartoonRow.innerHTML = ''; // Clear existing content

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} for ${rowId} (${endpoint})`);
        }
        const cartoons: Cartoon[] = await response.json();

        if (cartoons.length > 0) {
            cartoons.forEach(cartoon => {
                cartoonRow.appendChild(createCartoonCard(cartoon));
            });
        } else {
            cartoonRow.innerHTML = '<p style="color: var(--text-secondary);">No cartoons found in this category yet.</p>';
        }
    } catch (error) {
        console.error(`Failed to load cartoons for ${rowId}:`, error);
        cartoonRow.innerHTML = '<p style="color: var(--accent-hover);">Error loading cartoons. Please try again later.</p>';
    }
}

async function populateCartoonRows() {
    await populateCartoonRow('classicCartoonsRow', '/cartoons/sections/classics');
    await populateCartoonRow('goldenAgeGemsRow', '/cartoons/sections/golden-age');
    // Example for a new section - uncomment and use if you add "Recent"
    // await populateCartoonRow('recentCartoonsRow', '/cartoons/sections/recent');
}

// --- Event Listeners Setup ---
function setupEventListeners() {
    // Movie Request Modal
    if (movieRequestBtn && movieRequestModal) {
        movieRequestBtn.addEventListener('click', () => {
            movieRequestModal.style.display = 'flex';
            movieRequestModal.setAttribute('aria-hidden', 'false');
            (movieRequestModal.querySelector('input[type="text"]') as HTMLElement)?.focus();
        });
    }

    const closeMovieRequestModal = () => {
        if (movieRequestModal) {
            movieRequestModal.style.display = 'none';
            movieRequestModal.setAttribute('aria-hidden', 'true');
        }
    };
    
    if (movieRequestModalCloseBtn) {
        movieRequestModalCloseBtn.addEventListener('click', closeMovieRequestModal);
        movieRequestModalCloseBtn.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') closeMovieRequestModal();
        });
    }
    
    // Video Player Modal
    if (videoModalCloseBtn) {
        videoModalCloseBtn.addEventListener('click', closeVideoPlayer);
        videoModalCloseBtn.addEventListener('keydown', (e) => {
             if (e.key === 'Enter' || e.key === ' ') closeVideoPlayer();
        });
    }

    // Generic Modal Closing Logic (Escape key, click outside)
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            if (movieRequestModal && movieRequestModal.style.display === 'flex') {
                closeMovieRequestModal();
            }
            if (videoPlayerModal && videoPlayerModal.style.display === 'flex') {
                closeVideoPlayer();
            }
        }
    });

    [movieRequestModal, videoPlayerModal].forEach(modal => {
        if (modal) {
            modal.addEventListener('click', (event) => {
                if (event.target === modal) { // Clicked on the modal backdrop
                    if (modal === movieRequestModal) closeMovieRequestModal();
                    if (modal === videoPlayerModal) closeVideoPlayer();
                }
            });
        }
    });

    // Movie Request Form Submission
    if (movieRequestForm) {
        movieRequestForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const movieNameInput = document.getElementById('movieName') as HTMLInputElement;
            const emailInput = document.getElementById('email') as HTMLInputElement;
            const movieName = movieNameInput.value.trim();
            const email = emailInput.value.trim();

            if (movieName === '' || email === '') {
                showNotification('Please fill in all fields.', true);
                return;
            }

            const requestData: MovieRequestData = { movie_name: movieName, user_email: email };

            try {
                const response = await fetch(`${API_BASE_URL}/movie-requests/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData),
                });
                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({ detail: "Unknown server error."}));
                    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
                }
                closeMovieRequestModal();
                movieRequestForm.reset();
                showNotification('Request sent! You will be notified if the movie is added.');
            } catch (error) {
                console.error('Failed to submit movie request:', error);
                showNotification(`Error: ${error instanceof Error ? error.message : 'Could not submit request.'}`, true);
            }
        });
    }

    // Search Bar
    const searchInput = document.getElementById('searchInput') as HTMLInputElement;
    if (searchInput) {
        searchInput.addEventListener('keypress', async (event) => {
            if (event.key === 'Enter' && searchInput.value.trim() !== '') {
                const query = searchInput.value.trim();
                // showNotification(`Searching for: ${query}...`); // Optional: immediate feedback
                try {
                    const response = await fetch(`${API_BASE_URL}/cartoons/search?query=${encodeURIComponent(query)}`);
                    if(!response.ok) {
                        if (response.status === 404) {
                             showNotification(`No results found for "${query}".`, true);
                             return;
                        }
                        throw new Error(`Search HTTP error! status: ${response.status}`);
                    }
                    const searchResults: Cartoon[] = await response.json();
                    displaySearchResults(searchResults, query);
                } catch (error) {
                    console.error("Search failed:", error);
                    showNotification("Search failed. Please try again.", true);
                }
            }
        });
    }
}

// --- UI Helper Functions ---
function displaySearchResults(results: Cartoon[], query: string) {
    const mainContentContainer = document.getElementById('mainContentContainer'); // Target the main content area
    const firstSection = mainContentContainer?.querySelector('.content-section') as HTMLElement; // Get the first content section to replace or insert before

    if (!mainContentContainer) {
        console.error("Main content container not found for search results.");
        return;
    }
    
    // Clear all existing content sections for search results, or create a dedicated search results area
    // For simplicity, let's create a new section or replace one
    let searchResultsSection = document.getElementById('searchResultsSection');
    if (!searchResultsSection) {
        searchResultsSection = document.createElement('section');
        searchResultsSection.id = 'searchResultsSection';
        searchResultsSection.className = 'content-section';
        // Hide other sections if they exist
        document.getElementById('classicCartoonsSection')?.style.setProperty('display', 'none');
        document.getElementById('goldenAgeGemsSection')?.style.setProperty('display', 'none');
        // Add other sections you might have to hide them
        
        if (firstSection && mainContentContainer.firstChild === firstSection) {
            mainContentContainer.insertBefore(searchResultsSection, firstSection);
        } else {
            mainContentContainer.appendChild(searchResultsSection);
        }
    } else {
         // If search section exists, ensure others are hidden
        document.getElementById('classicCartoonsSection')?.style.setProperty('display', 'none');
        document.getElementById('goldenAgeGemsSection')?.style.setProperty('display', 'none');
    }

    searchResultsSection.innerHTML = `
        <h2 id="searchResultsTitle">Search Results for "${query}"</h2>
        <div class="cartoon-row" id="searchResultsRow"></div>
    `;
    const searchResultsRow = document.getElementById('searchResultsRow');

    if (searchResultsRow) {
        if (results.length > 0) {
            results.forEach(cartoon => {
                searchResultsRow.appendChild(createCartoonCard(cartoon));
            });
        } else {
            searchResultsRow.innerHTML = '<p style="color: var(--text-secondary);">No cartoons found matching your search.</p>';
        }
        searchResultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

function showNotification(message: string, isError: boolean = false) {
    if (notificationElement) {
        notificationElement.textContent = message;
        notificationElement.className = 'notification'; // Reset classes
        if (isError) {
            notificationElement.classList.add('error');
        }
        notificationElement.style.display = 'block';
        setTimeout(() => {
            notificationElement.style.display = 'none';
        }, 3500); // Increased duration slightly
    }
}

function updateCopyrightYear() {
    const yearSpan = document.getElementById('currentYear');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear().toString();
    }
}

// --- Video Player Functions ---
function openVideoPlayer(videoSrc: string, title: string) {
    if (videoPlayerModal && cartoonPlayer && videoPlayerModalHeading) {
        videoPlayerModalHeading.textContent = title;
        cartoonPlayer.src = videoSrc;
        videoPlayerModal.style.display = 'flex';
        videoPlayerModal.setAttribute('aria-hidden', 'false');
        cartoonPlayer.play().catch(error => {
            console.warn("Autoplay was prevented by the browser:", error);
            // Inform user or rely on them clicking play via controls
            showNotification("Autoplay blocked. Press play on the video.", true);
        });
        (videoModalCloseBtn as HTMLElement)?.focus();
    } else {
        console.error("Video player modal elements not found!");
        showNotification("Video player is not available.", true);
    }
}

function closeVideoPlayer() {
    if (videoPlayerModal && cartoonPlayer) {
        videoPlayerModal.style.display = 'none';
        videoPlayerModal.setAttribute('aria-hidden', 'true');
        cartoonPlayer.pause();
        cartoonPlayer.removeAttribute('src'); // Stop video from loading/playing in background
        cartoonPlayer.load(); // Resets the video element
    }
}