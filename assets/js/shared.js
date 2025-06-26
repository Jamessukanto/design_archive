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

	// Detect mobile devices
	isMobileDevice() {
		// Check multiple indicators for mobile devices
		const userAgent = navigator.userAgent.toLowerCase();
		const isMobileUserAgent = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(userAgent);
		
		// Check for touch support
		const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
		
		// Check screen size (mobile-like dimensions)
		const isSmallScreen = window.innerWidth <= 768 || window.innerHeight <= 768;
		
		// Check CSS media query support
		const isMobileMediaQuery = window.matchMedia && window.matchMedia('(max-width: 768px)').matches;
		
		// Consider it mobile if multiple indicators suggest so
		return isMobileUserAgent || (isTouchDevice && (isSmallScreen || isMobileMediaQuery));
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

		// Position the button to align with content
		this.alignHomeButton(homeButton);

		// Re-align on window resize
		const debouncedAlign = this.debounce(() => this.alignHomeButton(homeButton), 100);
		window.addEventListener('resize', debouncedAlign);

		// Add smooth scroll behavior if needed
		homeButton.addEventListener('click', function(e) {
			// Let the default navigation behavior work
			// Could add custom transition here if needed
		});
	},

	// Align home button with content left edge
	alignHomeButton(homeButton) {
		if (!homeButton) return;

		// Wait for next frame to ensure layout is complete
		requestAnimationFrame(() => {
			// Find the content area to align with
			const contentInner = document.querySelector('#main .inner');
			if (!contentInner) {
				// Fallback to CSS positioning
				homeButton.style.left = '';
				return;
			}

			// Get the computed style left position of the content area
			const contentRect = contentInner.getBoundingClientRect();
			const leftPosition = contentRect.left;

			// Calculate minimum spacing based on screen width
			const screenWidth = window.innerWidth;
			let minSpacing;
			
			if (screenWidth <= 480) {
				minSpacing = 20; // More spacing on very small screens
			} else if (screenWidth <= 736) {
				minSpacing = 15; // Medium spacing on small screens
			} else {
				minSpacing = 10; // Standard spacing on larger screens
			}

			// Apply the position with responsive minimum distance from the edge
			homeButton.style.left = Math.max(minSpacing, leftPosition) + 'px';
		});
	},

	// Simple lazy loading implementation
	initLazyLoading() {
		// Auto-add lazy loading to project page images (but not homepage thumbnails)
		if (window.location.pathname.includes('proj_')) {
			const projectImages = document.querySelectorAll('.image.main img, img[style*="width: 100%"]');
			projectImages.forEach((img, index) => {
				// Skip the first image (likely above the fold)
				if (index > 0 && !img.hasAttribute('loading')) {
					img.setAttribute('loading', 'lazy');
				}
			});
		}

		// Check if browser supports native lazy loading
		if ('loading' in HTMLImageElement.prototype) {
			return; // Native lazy loading is supported, no fallback needed
		}

		// Simple intersection observer fallback for older browsers
		if ('IntersectionObserver' in window) {
			const lazyImages = document.querySelectorAll('img[loading="lazy"]');
			
			const imageObserver = new IntersectionObserver((entries, observer) => {
				entries.forEach(entry => {
					if (entry.isIntersecting) {
						const img = entry.target;
						// Image is already loaded with src, just remove the lazy attribute
						img.removeAttribute('loading');
						observer.unobserve(img);
					}
				});
			});

			lazyImages.forEach(img => imageObserver.observe(img));
		}
	},

	// Initialize project preview functionality
	initProjectPreviews() {
		// Only run on homepage
		if (!window.location.pathname.endsWith('index.html') && 
			!window.location.pathname.endsWith('/')) {
			return;
		}

		// Skip preview functionality on mobile devices to improve performance
		if (this.isMobileDevice()) {
			console.log('Mobile device detected: skipping project previews for better performance');
			return;
		}

		const previewWindow = document.getElementById('project-preview');
		const previewImage = document.getElementById('preview-image');
		const projectTiles = document.querySelectorAll('.tiles article[data-preview]');

		if (!previewWindow || !previewImage || projectTiles.length === 0) {
			return;
		}

		let currentHoverTile = null;
		let hoverTimeout = null;

		// Mouse move handler for preview window positioning
		const handleMouseMove = this.debounce((e) => {
			if (currentHoverTile) {
				// Center the preview window over the cursor
				const previewWidth = 400;
				const previewHeight = 240;
				
				let x = e.clientX - (previewWidth / 2);
				let y = e.clientY - (previewHeight / 2);
				
				// Keep preview window within viewport
				const windowWidth = window.innerWidth;
				const windowHeight = window.innerHeight;
				
				// Adjust if window would go outside viewport
				if (x < 10) {
					x = 10;
				}
				if (x + previewWidth > windowWidth - 10) {
					x = windowWidth - previewWidth - 10;
				}
				if (y < 10) {
					y = 10;
				}
				if (y + previewHeight > windowHeight - 10) {
					y = windowHeight - previewHeight - 10;
				}
				
				previewWindow.style.left = x + 'px';
				previewWindow.style.top = y + 'px';
			}
		}, 16); // ~60fps

		// Add event listeners to each project tile
		projectTiles.forEach(tile => {
			const previewImageSrc = tile.getAttribute('data-preview');
			
			tile.addEventListener('mouseenter', () => {
				currentHoverTile = tile;
				
				// Clear any existing timeout
				if (hoverTimeout) {
					clearTimeout(hoverTimeout);
				}
				
				// Load the preview image
				previewImage.src = 'images/' + previewImageSrc;
				previewImage.classList.remove('scrolling'); // Reset animation
				
				// Force reflow to restart animation
				void previewImage.offsetWidth;
				previewImage.classList.add('scrolling');
				
				// Show preview window immediately
				previewWindow.classList.add('visible');
			});

			tile.addEventListener('mouseleave', () => {
				currentHoverTile = null;
				previewWindow.classList.remove('visible');
				
				// Clear timeout if set
				if (hoverTimeout) {
					clearTimeout(hoverTimeout);
					hoverTimeout = null;
				}
			});

			tile.addEventListener('mousemove', handleMouseMove);
		});

		// Handle image load errors
		previewImage.addEventListener('error', () => {
			console.warn('Failed to load preview image:', previewImage.src);
		});

		console.log('Project previews initialized for', projectTiles.length, 'tiles');
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
	// Initialize lazy loading for images
	SiteUtils.initLazyLoading();

	// Add floating home button on project pages
	SiteUtils.addFloatingHomeButton();

	// Initialize project previews on homepage
	SiteUtils.initProjectPreviews();

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