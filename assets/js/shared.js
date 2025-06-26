/**
 * Shared utilities for the Design Archive website
 */

// Site utilities namespace
const SiteUtils = {
	
	// Email copy functionality
	copyEmail() {
		const email = window.CONFIG?.site?.email || 'jamessukanto@gmail.com';
		navigator.clipboard.writeText(email)
			.then(() => this.showToast('Email copied!', 'success'))
			.catch((err) => {
				console.error('Failed to copy email:', err);
				this.showToast('Failed to copy email', 'error');
			});
	},

	// Show toast notification
	showToast(message, type = 'info') {
		// Remove existing toast if any
		const existingToast = document.querySelector('.toast-notification');
		if (existingToast) {
			existingToast.remove();
		}

		// Create toast element
		const toast = document.createElement('div');
		toast.className = `toast-notification toast-${type}`;
		toast.textContent = message;

		// Add to page
		document.body.appendChild(toast);

		// Show with animation
		setTimeout(() => toast.classList.add('toast-show'), 100);

		// Auto-hide after 3 seconds
		setTimeout(() => {
			toast.classList.remove('toast-show');
			setTimeout(() => toast.remove(), 300);
		}, 3000);
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
function copyEmail(event) {
	// If called with an event (from footer link), prevent mailto and copy instead
	if (event) {
		event.preventDefault();
	}
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