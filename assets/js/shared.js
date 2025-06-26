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
	}
};

// Backward compatibility
function copyEmail() {
	SiteUtils.copyEmail();
}

// Initialize site utilities when DOM is loaded
if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', initSiteUtils);
} else {
	initSiteUtils();
}

function initSiteUtils() {
	// Initialize image error handling for all images
	document.querySelectorAll('img').forEach(img => {
		SiteUtils.loadImage(img);
	});
}

// Make utilities globally available
if (typeof window !== 'undefined') {
	window.SiteUtils = SiteUtils;
} 