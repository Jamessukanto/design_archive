/**
 * Shared utilities for the Design Archive website
 */

// Site utilities namespace
const SiteUtils = {
	
	// Email copy functionality
	copyEmail() {
		const email = window.CONFIG?.site?.email || 'jamessukanto@gmail.com';
		navigator.clipboard.writeText(email)
			.then(() => alert('Email copied!'))
			.catch((err) => {
				console.error('Failed to copy email:', err);
				alert('Failed to copy email');
			});
	},

	// Enhanced image loading with error handling
	loadImage(imgElement, fallbackSrc = null) {
		if (!imgElement) return;
		
		imgElement.onerror = function() {
			if (fallbackSrc) {
				this.onerror = null; // Prevent infinite loop
				this.src = fallbackSrc;
			} else {
				console.warn('Failed to load image:', this.src);
			}
		};
	},

	// Smooth scroll to element
	scrollToElement(selector, offset = 0) {
		const element = document.querySelector(selector);
		if (element) {
			const top = element.offsetTop - offset;
			window.scrollTo({
				top: top,
				behavior: 'smooth'
			});
		}
	},

	// Debounce utility for performance
	debounce(func, wait) {
		let timeout;
		return function executedFunction(...args) {
			const later = () => {
				clearTimeout(timeout);
				func(...args);
			};
			clearTimeout(timeout);
			timeout = setTimeout(later, wait);
		};
	},

	// Add floating home button to project pages
	addFloatingHomeButton() {
		// Only add to project pages (those containing "proj_" in URL)
		if (!window.location.pathname.includes('proj_')) {
			return;
		}

		// Check if button already exists
		if (document.querySelector('.back-btn')) {
			return;
		}

		// Create the floating home button
		const homeButton = document.createElement('a');
		homeButton.href = 'index.html';
		homeButton.className = 'back-btn';
		homeButton.innerHTML = '← Home';
		homeButton.setAttribute('aria-label', 'Go back to home page');

		// Add to the page
		document.body.appendChild(homeButton);

		// Add smooth scroll behavior if needed
		homeButton.addEventListener('click', function(e) {
			// Let the default navigation behavior work
			// Could add custom transition here if needed
		});
	}
};

// Backward compatibility
function copyEmail() {
	SiteUtils.copyEmail();
}

// Initialize site utilities when DOM is ready
function initSiteUtils() {
	// Add floating home button on project pages
	SiteUtils.addFloatingHomeButton();

	// Initialize image error handling
	const images = document.querySelectorAll('img');
	images.forEach(img => SiteUtils.loadImage(img));

	console.log('Site utilities initialized');
}

// Auto-initialize when DOM is loaded
if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', initSiteUtils);
} else {
	// DOM already loaded
	initSiteUtils();
}

// Expose globally for manual calls if needed
window.SiteUtils = SiteUtils;
window.initSiteUtils = initSiteUtils; 