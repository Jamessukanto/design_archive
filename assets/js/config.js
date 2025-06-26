/**
 * Site Configuration
 * Central configuration for the Design Archive website
 */

const CONFIG = {
	// Site metadata
	site: {
		title: 'James Sukanto Design Archive',
		description: 'UI/UX Designer specializing in Generative AI and Computer Vision',
		author: 'James Sukanto',
		email: 'jamessukanto@gmail.com',
		url: 'https://jamessukanto.github.io/design_archive',
		environment: 'github-pages'
	},

	// Social links
	social: {
		linkedin: 'https://www.linkedin.com/in/jamessukanto/',
		github: 'https://www.github.com/jamessukanto/'
	},

	// Project categories
	categories: {
		interfaces: 'Screen Interfaces',
		mixed_reality: 'Mixed Reality',
		miscellaneous: 'Miscellaneous'
	},

	// Animation settings
	animation: {
		menuTransition: 350,
		tileHoverDelay: 100
	}
};

// Make config globally available
if (typeof window !== 'undefined') {
	window.CONFIG = CONFIG;
} 