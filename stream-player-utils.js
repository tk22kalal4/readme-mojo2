/**
 * Stream Player Utilities
 * Replaces Stream/Download buttons with a single "Open" button
 * that redirects to the new stream-player.html with reCAPTCHA verification
 */

// Function to open the stream player with reCAPTCHA verification
function openStreamPlayer(streamUrl, downloadUrl, title) {
    if (!streamUrl) {
        alert('Stream URL not available');
        return;
    }

    // Build the URL with parameters
    const params = new URLSearchParams({
        stream: streamUrl,
        title: title || 'Lecture Video'
    });

    // Add download URL if available
    if (downloadUrl) {
        params.append('download', downloadUrl);
    }

    // Open in the same window/tab
    // Get the base path relative to current location
    const currentPath = window.location.pathname;
    
    // Split path and remove empty strings and the current filename
    const pathParts = currentPath.split('/').filter(p => p);
    
    // Remove the filename (last part) to get directory depth
    const directoryParts = pathParts.slice(0, -1);
    
    // Calculate how many levels deep we are from the root
    // For GitHub Pages, we need to account for the repo name
    // Example: /readme-mojo2/1234xx/dams/damsb2benglish/anatomy.html
    // Parts: ['readme-mojo2', '1234xx', 'dams', 'damsb2benglish']
    // We need to go up to readme-mojo2 level, so 3 levels up
    const depth = directoryParts.length - 1; // -1 because we don't count the root repo folder
    
    const basePath = '../'.repeat(depth > 0 ? depth : 0);
    window.location.href = `${basePath}stream-player.html?${params.toString()}`;
}

// Function to replace Stream/Download buttons with Open button
function replaceStreamDownloadButtons(container) {
    // Find all lecture cards in the container
    const lectureCards = container ? 
        container.querySelectorAll('.lecture-card') : 
        document.querySelectorAll('.lecture-card');

    lectureCards.forEach(card => {
        const buttonContainer = card.querySelector('.button-container');
        if (!buttonContainer) return;

        const streamBtn = buttonContainer.querySelector('.stream-button');
        const downloadBtn = buttonContainer.querySelector('.download-button');

        if (!streamBtn) return;

        // Get URLs from onclick attributes
        const streamUrl = extractUrlFromOnclick(streamBtn.getAttribute('onclick'), 'openPopup');
        const downloadUrl = downloadBtn ? 
            extractUrlFromOnclick(downloadBtn.getAttribute('onclick'), 'openPopup') : null;

        // Get title from card
        const titleElement = card.querySelector('h3');
        const title = titleElement ? titleElement.textContent.trim() : 'Lecture Video';

        // Create new Open button
        const openBtn = document.createElement('button');
        openBtn.className = 'open-button';
        openBtn.innerHTML = '<i class="fas fa-play-circle"></i> Open';
        openBtn.onclick = () => openStreamPlayer(streamUrl, downloadUrl, title);

        // Replace button container content
        buttonContainer.innerHTML = '';
        buttonContainer.appendChild(openBtn);
    });
}

// Helper function to extract URL from onclick attribute
function extractUrlFromOnclick(onclickStr, functionName) {
    if (!onclickStr) return null;
    
    // Match pattern: openPopup('url', 'title')
    const regex = new RegExp(`${functionName}\\s*\\(\\s*['"]([^'"]+)['"]`);
    const match = onclickStr.match(regex);
    
    return match ? match[1] : null;
}

// Add CSS for Open button (matching existing theme)
function addOpenButtonStyles() {
    if (document.getElementById('open-button-styles')) return;

    const style = document.createElement('style');
    style.id = 'open-button-styles';
    style.textContent = `
        .open-button {
            background: #2c5282;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(44, 130, 82, 0.3);
        }

        .open-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(44, 130, 82, 0.4);
        }

        .open-button:active {
            transform: translateY(0);
        }

        .open-button i {
            font-size: 1.1rem;
        }

        @media (max-width: 768px) {
            .open-button {
                width: 100%;
                justify-content: center;
            }
        }
    `;
    document.head.appendChild(style);
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        addOpenButtonStyles();
        replaceStreamDownloadButtons();
    });
} else {
    addOpenButtonStyles();
    replaceStreamDownloadButtons();
}

// Export for manual use
window.StreamPlayerUtils = {
    openStreamPlayer,
    replaceStreamDownloadButtons,
    addOpenButtonStyles
};
