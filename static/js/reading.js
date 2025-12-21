// State
let fontSize = 21;
let focusMode = false;
let pagefind = null;
let searchTimeout = null;

// Get stored state
const bookSlugElement = document.querySelector('[data-book-slug]');
const chapterIdElement = document.querySelector('[data-chapter-id]');
const bookSlug = bookSlugElement ? bookSlugElement.dataset.bookSlug : '';
const chapterId = chapterIdElement ? chapterIdElement.dataset.chapterId : '';
const storageKey = `${bookSlug}-${chapterId}`;

// Progress tracking
function updateProgress() {
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;
    const progressBar = document.getElementById('progress');
    if (progressBar) {
        progressBar.style.width = progress + '%';
    }
}

// Top bar scroll effects
let lastScrollTop = 0;
function handleTopBarScroll() {
    const topBar = document.getElementById('topBar');
    if (!topBar) return;

    const scrollTop = window.scrollY;

    // Add scrolled class when scrolled down
    if (scrollTop > 100) {
        topBar.classList.add('scrolled');
    } else {
        topBar.classList.remove('scrolled');
    }

    lastScrollTop = scrollTop;
}

window.addEventListener('scroll', () => {
    updateProgress();
    handleTopBarScroll();
});

// Menu panel toggle
function toggleMenu() {
    const menu = document.getElementById('menuPanel');
    const overlay = document.getElementById('overlay');
    if (menu && overlay) {
        const isOpen = menu.classList.contains('open');
        if (isOpen) {
            menu.classList.remove('open');
            overlay.classList.remove('show');
        } else {
            menu.classList.add('open');
            overlay.classList.add('show');
        }
    }
}

// Close menu
function closeMenu() {
    const menu = document.getElementById('menuPanel');
    const overlay = document.getElementById('overlay');
    if (menu) menu.classList.remove('open');
    if (overlay) overlay.classList.remove('show');
}

// Focus mode
function toggleFocusMode() {
    focusMode = !focusMode;
    document.body.classList.toggle('focus-mode');
    closeMenu();
    showShortcutHint(focusMode ? 'Focus mode on - Press F to exit' : 'Focus mode off');
}

// Font size adjustment
function adjustSize(delta) {
    if (delta === 0) {
        fontSize = 21;
    } else {
        fontSize = Math.max(17, Math.min(27, fontSize + delta));
    }

    // Apply to reading text
    const textElement = document.querySelector('.text');
    if (textElement) {
        textElement.style.fontSize = fontSize + 'px';
        localStorage.setItem(`fontSize-${bookSlug}`, fontSize);
    }

    updateFontSizeButtons();
}

function updateFontSizeButtons() {
    const container = document.querySelector('.menu-section');
    if (!container) return;
    const buttons = container.querySelectorAll('.setting-btn');

    buttons.forEach(btn => btn.classList.remove('active'));

    if (fontSize === 21) {
        buttons[1]?.classList.add('active'); // Default button
    } else if (fontSize < 21) {
        buttons[0]?.classList.add('active'); // Smaller button
    } else {
        buttons[2]?.classList.add('active'); // Larger button
    }
}

// Theme switching
function setTheme(theme) {
    document.body.className = theme === 'light' ? '' : theme;
    if (focusMode) document.body.classList.add('focus-mode');
    localStorage.setItem('theme', theme);
    updateThemeButtons(theme);
}

function updateThemeButtons(theme) {
    const groups = document.querySelectorAll('.setting-group');
    if (groups.length < 2) return;
    const buttons = groups[1].querySelectorAll('.setting-btn');

    buttons.forEach(btn => btn.classList.remove('active'));

    if (theme === 'light') {
        buttons[0]?.classList.add('active');
    } else if (theme === 'dark') {
        buttons[1]?.classList.add('active');
    } else if (theme === 'sepia') {
        buttons[2]?.classList.add('active');
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    switch(e.key.toLowerCase()) {
        case 's':
            e.preventDefault();
            openMenuAndFocusSearch();
            break;
        case 'm':
            e.preventDefault();
            toggleMenu();
            showShortcutHint('Menu');
            break;
        case 'f':
            e.preventDefault();
            toggleFocusMode();
            break;
        case 'arrowleft':
            e.preventDefault();
            navigateToPrev();
            break;
        case 'arrowright':
            e.preventDefault();
            navigateToNext();
            break;
        case 'escape':
            closeMenu();
            if (focusMode) toggleFocusMode();
            break;
    }
});

// Chapter navigation
function navigateToPrev() {
    const prevLink = document.querySelector('.chapter-nav .nav-link.prev');
    if (prevLink) {
        showShortcutHint('Previous Chapter');
        window.location.href = prevLink.href;
    }
}

function navigateToNext() {
    const nextLink = document.querySelector('.chapter-nav .nav-link.next');
    if (nextLink) {
        showShortcutHint('Next Chapter');
        window.location.href = nextLink.href;
    }
}

// Book search
async function initBookSearch() {
    if (pagefind) return;
    pagefind = await import('/pagefind/pagefind.js');
    await pagefind.options({ excerptLength: 20 });
}

async function handleBookSearch(query) {
    const resultsContainer = document.getElementById('bookSearchResults');
    if (!resultsContainer) return;

    if (!query || query.length < 2) {
        resultsContainer.innerHTML = '';
        return;
    }

    await initBookSearch();

    const menuPanel = document.getElementById('menuPanel');
    const currentBookSlug = menuPanel?.dataset.bookSlug;

    const search = await pagefind.search(query, {
        filters: { book: currentBookSlug }
    });

    const results = await Promise.all(
        search.results.slice(0, 10).map(r => r.data())
    );

    renderBookSearchResults(results);
}

function renderBookSearchResults(results) {
    const container = document.getElementById('bookSearchResults');
    if (!container) return;

    if (results.length === 0) {
        container.innerHTML = '<div class="no-results">No results found</div>';
        return;
    }

    container.innerHTML = results.map(r => `
        <a href="${r.url}" class="book-search-result">
            <span class="result-title">${r.meta.title || 'Untitled'}</span>
            <span class="result-excerpt">${r.excerpt}</span>
        </a>
    `).join('');
}

function setupBookSearch() {
    const input = document.getElementById('bookSearchInput');
    if (!input) return;

    input.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            handleBookSearch(e.target.value);
        }, 200);
    });
}

function openMenuAndFocusSearch() {
    const menu = document.getElementById('menuPanel');
    const overlay = document.getElementById('overlay');
    const input = document.getElementById('bookSearchInput');

    if (menu && overlay) {
        menu.classList.add('open');
        overlay.classList.add('show');
    }

    if (input) {
        setTimeout(() => input.focus(), 100);
    }

    showShortcutHint('Search Book');
}

// Position memory
window.addEventListener('beforeunload', () => {
    if (storageKey) {
        localStorage.setItem(`scroll-${storageKey}`, window.scrollY);
    }
});

window.addEventListener('load', () => {
    // Restore scroll position
    if (storageKey) {
        const savedPos = localStorage.getItem(`scroll-${storageKey}`);
        if (savedPos) window.scrollTo(0, parseInt(savedPos));
    }

    // Restore font size
    if (bookSlug) {
        const savedSize = localStorage.getItem(`fontSize-${bookSlug}`);
        if (savedSize) {
            fontSize = parseInt(savedSize);
            const textElement = document.querySelector('.text');
            if (textElement) {
                textElement.style.fontSize = fontSize + 'px';
            }
        }
    }

    // Restore theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme && savedTheme !== 'light') {
        setTheme(savedTheme);
    } else {
        updateThemeButtons('light');
    }

    updateFontSizeButtons();
    updateProgress();
    setupBookSearch();
});

// Shortcut hints
function showShortcutHint(text) {
    const hint = document.getElementById('shortcutHint');
    if (hint) {
        hint.textContent = text;
        hint.classList.add('show');
        setTimeout(() => hint.classList.remove('show'), 2000);
    }
}
