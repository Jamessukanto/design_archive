# Development Guide

## 🏗️ Architecture Overview

This portfolio site uses a modern, modular approach with clean separation of concerns:

### HTML Structure
- **Semantic markup** for accessibility and SEO
- **Modular templates** to reduce duplication
- **Progressive enhancement** ensuring core functionality without JavaScript

### CSS Architecture (Sass)
- **BEM methodology** for component naming
- **Mobile-first** responsive design
- **Component-based** organization
- **Design tokens** for consistent styling

### JavaScript Organization
- **Namespace pattern** to avoid global pollution
- **Module-like structure** for better organization
- **Event delegation** for performance
- **Utility-first** approach

## 🔧 Code Standards

### HTML
```html
<!-- Use semantic elements -->
<section class="portfolio-grid">
  <article class="project-card">
    <h2 class="project-title">Project Name</h2>
  </article>
</section>

<!-- Consistent class naming (BEM) -->
<div class="component__element component__element--modifier">
```

### CSS/Sass
```scss
// Component structure
.component {
  // Base styles
  
  &__element {
    // Element styles
  }
  
  &--modifier {
    // Modifier styles
  }
  
  // Responsive design
  @include breakpoint('<=medium') {
    // Mobile styles
  }
}
```

### JavaScript
```javascript
// Use namespace pattern
const ComponentName = {
  init() {
    this.bindEvents();
  },
  
  bindEvents() {
    // Event binding logic
  }
};

// Avoid global variables
// Use meaningful function names
// Add error handling
```

## 📱 Responsive Design

### Breakpoints
```scss
$breakpoints: (
  xxsmall:  360px,
  xsmall:   480px,
  small:    736px,
  medium:   980px,
  large:    1280px,
  xlarge:   1680px
);
```

### Grid System
- **Flexbox-based** layout
- **CSS Grid** for complex layouts
- **Fluid typography** using clamp()
- **Container queries** where supported

## 🎨 Design System

### Colors
```scss
$palette: (
  primary:   #f2849e,
  secondary: #7ecaf6,
  accent:    #7bd0c1,
  text:      #585858,
  bg:        #ffffff
);
```

### Typography
```scss
$font-stack: (
  primary: ('Source Sans Pro', Helvetica, sans-serif),
  mono:    ('Courier New', monospace)
);
```

### Spacing
```scss
$spacing: (
  xs:  0.5rem,
  sm:  1rem,
  md:  1.5rem,
  lg:  2rem,
  xl:  3rem
);
```

## 🚀 Performance Optimization

### Images
- **Responsive images** with srcset
- **Lazy loading** for below-fold content
- **WebP format** with fallbacks
- **Proper alt text** for accessibility

### CSS
- **Critical CSS** inlined in head
- **Non-critical styles** loaded asynchronously
- **Minification** for production
- **Unused CSS** removal

### JavaScript
- **Minimal dependencies** (only jQuery for legacy support)
- **Code splitting** by page
- **Async loading** for non-critical scripts
- **Error boundaries** for graceful degradation

## 🧪 Testing Strategy

### Manual Testing
- **Cross-browser** compatibility
- **Device testing** (mobile, tablet, desktop)
- **Accessibility** with screen readers
- **Performance** with DevTools

### Automated Testing
```bash
# Lighthouse CI for performance
npm run lighthouse

# HTML validation
npm run validate:html

# CSS linting
npm run lint:css

# JavaScript linting
npm run lint:js
```

## 🔍 Debugging

### Common Issues
1. **Images not loading**: Check file paths and formats
2. **Styles not applying**: Verify CSS specificity
3. **JavaScript errors**: Check console for syntax errors
4. **Responsive issues**: Test across breakpoints

### Debug Tools
- **Browser DevTools**: Primary debugging interface
- **Responsive Mode**: Test different screen sizes
- **Console Logging**: Strategic console.log() placement
- **Network Tab**: Monitor resource loading

## 📦 Build Process

### Development
```bash
npm run dev     # Start development server
npm run watch   # Watch for file changes
```

### Production
```bash
npm run deploy  # Deploy to GitHub Pages
npm run preview # Show live URL
```

## 🚀 Deployment (GitHub Pages)

### Current Setup
This site is configured for automatic GitHub Pages deployment:

1. **Automatic**: Push to `main` branch triggers deployment
2. **GitHub Actions**: Uses `.github/workflows/pages.yml` for deployment
3. **Live URL**: https://jamessukanto.github.io/design_archive
4. **Deploy Command**: `npm run deploy` (alias for `git push origin main`)

### GitHub Pages Setup
If setting up from scratch:
1. Go to repository Settings → Pages
2. Set Source to "GitHub Actions"
3. Ensure the workflow file exists in `.github/workflows/`

### Alternative Deployment
For other hosting providers:
1. Static hosting: Upload files directly
2. CDN deployment: Connect repository for auto-deployment
3. Custom domain: Configure DNS and GitHub Pages settings

### Environment Configuration
```bash
# GitHub Pages (automatic)
GITHUB_PAGES=true
SITE_URL=https://jamessukanto.github.io/design_archive

# Local Development
NODE_ENV=development
PORT=8080
```

## 🔄 Maintenance

### Regular Tasks
- **Update dependencies** monthly
- **Check broken links** quarterly
- **Review analytics** for performance insights
- **Update content** as needed

### GitHub Pages Specific
- **Monitor Actions**: Check GitHub Actions for deployment status
- **Branch Protection**: Ensure main branch is protected
- **Security**: Regular dependency updates via Dependabot
- **Performance**: Monitor Core Web Vitals via GitHub insights

### Monitoring
- **Core Web Vitals** tracking
- **Error logging** for JavaScript issues
- **Analytics** for user behavior
- **Uptime monitoring** for availability 