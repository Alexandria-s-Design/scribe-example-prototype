# Scribe Onboarding Simulation - Design Specifications

## Extracted from Screenshots - November 19, 2025

---

## 🎨 SCREEN 1: HOMEPAGE - "Brilliantly Efficient"

### Colors
```css
/* Hero Gradient Background */
background: linear-gradient(180deg, #4F46E5 0%, #7C3AED 100%);

/* Text Colors */
--hero-headline: #FFFFFF;
--hero-subtext: rgba(255, 255, 255, 0.9);
--card-background: #FFFFFF;
--card-text-primary: #111827;
--card-text-secondary: #6B7280;
```

### Typography
```css
/* Font Family */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Hero Section */
--hero-headline-size: 56px;
--hero-headline-weight: 700;
--hero-headline-line-height: 1.1;
--hero-subtext-size: 20px;
--hero-subtext-weight: 400;

/* Use Case Cards */
--card-title-size: 18px;
--card-title-weight: 600;
--card-description-size: 14px;
--card-description-weight: 400;
```

### Layout & Spacing
```css
/* Hero Section */
--hero-padding: 80px 40px;
--hero-text-gap: 16px;

/* Use Case Card Grid */
--card-grid-columns: 3;
--card-grid-gap: 24px;
--card-padding: 32px;
--card-border-radius: 16px;
--card-min-height: 240px;

/* Container */
--max-width: 1200px;
```

### Effects
```css
/* Card Shadows */
--card-shadow-default: 0 4px 24px rgba(0, 0, 0, 0.06);
--card-shadow-hover: 0 8px 32px rgba(0, 0, 0, 0.12);

/* Transitions */
--transition-default: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Card Hover State */
transform: translateY(-4px);
border: 2px solid #4F46E5;
```

### Use Case Cards (6 Total)
1. **Onboard new hires** - Icon: User with checklist
2. **Create SOPs** - Icon: Document with lightning bolt
3. **Build training docs** - Icon: Book/document
4. **Answer questions** - Icon: Question mark in circle
5. **Assist customers** - Icon: Headset
6. **Something else** - Icon: Cursor/pointer

---

## 🎨 SCREEN 2: SIGN IN PAGE

### Colors
```css
/* Background */
--page-background: #FFFFFF;

/* Card */
--card-background: #FFFFFF;
--card-border: none;

/* Buttons */
--google-button-background: #4285F4;
--google-button-text: #FFFFFF;
--google-button-hover: #357ABD;

/* Input Fields */
--input-border: #E5E7EB;
--input-border-focus: #4F46E5;
--input-background: #FFFFFF;
--input-text: #111827;
--input-placeholder: #9CA3AF;
```

### Typography
```css
/* Sign In Heading */
--signin-heading-size: 24px;
--signin-heading-weight: 600;
--signin-heading-color: #111827;

/* Subtitle */
--subtitle-size: 14px;
--subtitle-weight: 400;
--subtitle-color: #6B7280;

/* Button Text */
--button-text-size: 16px;
--button-text-weight: 500;
```

### Layout & Spacing
```css
/* Sign In Card */
--card-max-width: 480px;
--card-padding: 48px;
--card-border-radius: 20px;
--card-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);

/* Input Fields */
--input-height: 48px;
--input-padding: 12px 16px;
--input-border-radius: 8px;
--input-margin-bottom: 16px;

/* Google Button */
--button-height: 48px;
--button-padding: 0 24px;
--button-border-radius: 8px;
--button-gap: 12px; /* space between icon and text */

/* Divider */
--divider-margin: 24px 0;
--divider-text-size: 14px;
--divider-text-color: #9CA3AF;
```

### Effects
```css
/* Input Focus State */
box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);

/* Button Hover */
transform: translateY(-1px);
box-shadow: 0 4px 12px rgba(66, 133, 244, 0.3);
```

---

## 🎨 SCREEN 3: GOOGLE ACCOUNT CHOOSER

### Colors
```css
/* Backdrop */
--backdrop-background: rgba(0, 0, 0, 0.5);
--backdrop-blur: blur(4px);

/* Modal Card */
--modal-background: #FFFFFF;
--modal-border-radius: 12px;

/* Account Option */
--account-option-background: #FFFFFF;
--account-option-border: #E5E7EB;
--account-option-hover-background: #F9FAFB;
--account-option-hover-border: #4F46E5;

/* Avatar */
--avatar-background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
--avatar-text: #FFFFFF;

/* Text */
--account-name-color: #111827;
--account-name-weight: 500;
--account-email-color: #6B7280;
--account-email-weight: 400;
```

### Typography
```css
/* Heading */
--modal-heading-size: 24px;
--modal-heading-weight: 600;

/* Account Name */
--account-name-size: 16px;

/* Account Email */
--account-email-size: 14px;

/* Subtitle */
--modal-subtitle-size: 14px;
--modal-subtitle-color: #6B7280;
```

### Layout & Spacing
```css
/* Modal */
--modal-max-width: 480px;
--modal-padding: 32px;
--modal-shadow: 0 24px 80px rgba(0, 0, 0, 0.2);

/* Account Option */
--account-option-height: 72px;
--account-option-padding: 16px;
--account-option-border-radius: 8px;
--account-option-gap: 16px;
--account-option-margin: 12px 0;

/* Avatar */
--avatar-size: 40px;
--avatar-border-radius: 50%;
--avatar-font-size: 18px;
--avatar-font-weight: 600;
```

### Effects
```css
/* Account Option Hover */
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
```

### Account Data
```
Name: Alexandria's World
Email: alexandriasworld1234@gmail.com
Avatar Letter: A
```

---

## 🎨 SCREEN 4: GOOGLE OAUTH PERMISSIONS

### Colors
```css
/* Google Branding */
--google-blue: #4285F4;
--google-blue-hover: #357ABD;

/* Buttons */
--allow-button-background: #1A73E8;
--allow-button-text: #FFFFFF;
--cancel-button-background: transparent;
--cancel-button-text: #1A73E8;
--cancel-button-border: #DADCE0;

/* Permission Icons */
--checkmark-color: #34A853;

/* Text */
--permission-text-color: #374151;
--app-name-color: #111827;
--app-name-weight: 600;
```

### Typography
```css
/* Modal Heading */
--oauth-heading-size: 20px;
--oauth-heading-weight: 600;

/* Permission Text */
--permission-text-size: 14px;
--permission-text-weight: 400;
--permission-text-line-height: 1.5;

/* App Name */
--app-name-size: 16px;
```

### Layout & Spacing
```css
/* Permission Item */
--permission-item-height: 64px;
--permission-item-gap: 16px;
--permission-item-padding: 12px 0;

/* Permission Icon */
--permission-icon-size: 24px;

/* Buttons */
--allow-button-height: 40px;
--allow-button-padding: 0 24px;
--allow-button-border-radius: 4px;

--cancel-button-height: 40px;
--cancel-button-padding: 0 24px;
--cancel-button-border-radius: 4px;

/* Button Container */
--button-container-gap: 16px;
--button-container-margin-top: 24px;
```

### Permissions List
```
1. See your personal info, including email and name
2. See your primary Google Account email address
3. Associate you with your personal info on Google
```

---

## 🎨 SCREEN 5: TEAM NAMING MODAL

### Colors
```css
/* Modal Background */
--modal-background: #FFFFFF;

/* Input Field */
--input-background: #FFFFFF;
--input-border: #E5E7EB;
--input-border-focus: #4F46E5;
--input-border-error: #EF4444;
--input-border-success: #10B981;

/* Button */
--submit-button-background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
--submit-button-text: #FFFFFF;
--submit-button-disabled-opacity: 0.5;

/* Validation Messages */
--error-text-color: #EF4444;
--success-text-color: #10B981;
```

### Typography
```css
/* Modal Heading */
--team-heading-size: 28px;
--team-heading-weight: 700;

/* Subtitle */
--team-subtitle-size: 16px;
--team-subtitle-weight: 400;
--team-subtitle-color: #6B7280;

/* Input Label */
--label-size: 14px;
--label-weight: 500;
--label-color: #374151;

/* Input Text */
--input-text-size: 18px;
--input-text-weight: 400;

/* Button Text */
--submit-button-size: 18px;
--submit-button-weight: 600;

/* Validation Message */
--validation-text-size: 14px;
```

### Layout & Spacing
```css
/* Modal */
--modal-max-width: 520px;
--modal-padding: 48px;
--modal-border-radius: 16px;
--modal-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);

/* Icon */
--modal-icon-size: 64px;
--modal-icon-margin-bottom: 24px;

/* Input Field */
--input-height: 56px;
--input-padding: 16px 20px;
--input-border-radius: 12px;
--input-font-size: 18px;
--input-margin-bottom: 8px;

/* Submit Button */
--submit-button-height: 56px;
--submit-button-border-radius: 12px;
--submit-button-margin-top: 24px;

/* Skip Link */
--skip-link-size: 14px;
--skip-link-color: #6B7280;
--skip-link-margin-top: 16px;
```

### Validation Rules
```javascript
minLength: 2,
maxLength: 50,
required: true,
realTimeValidation: true
```

---

## 🎨 COVER SCREEN (Custom Design)

### Colors
```css
/* Background */
--cover-background: linear-gradient(135deg, #F8F9FF 0%, #FFFFFF 100%);

/* Card */
--cover-card-background: #FFFFFF;
--cover-card-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);

/* Button */
--start-button-background: #4F46E5;
--start-button-text: #FFFFFF;
--start-button-hover: #4338CA;

/* Text */
--cover-heading-color: #111827;
--cover-body-color: #374151;
--cover-list-color: #6B7280;
```

### Typography
```css
/* Cover Heading */
--cover-heading-size: 36px;
--cover-heading-weight: 700;

/* Body Text */
--cover-body-size: 18px;
--cover-body-weight: 400;

/* List Items */
--cover-list-size: 16px;
--cover-list-weight: 400;

/* Button */
--cover-button-size: 18px;
--cover-button-weight: 600;
```

---

## 🎨 COMPLETION SCREEN (Custom Design)

### Colors
```css
/* Background */
--completion-background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);

/* Success Icon */
--success-icon-background: #10B981;
--success-icon-color: #FFFFFF;

/* Confetti Colors */
--confetti-colors: ['#4F46E5', '#7C3AED', '#10B981', '#F59E0B', '#EF4444', '#EC4899'];

/* Buttons */
--restart-button-background: #4F46E5;
--restart-button-text: #FFFFFF;
--close-button-background: #E5E7EB;
--close-button-text: #374151;
```

---

## 🎨 GUIDANCE SYSTEM

### Tooltip
```css
/* Background */
--tooltip-background: #1F2937;
--tooltip-text: #FFFFFF;
--tooltip-border-radius: 8px;
--tooltip-padding: 12px 16px;
--tooltip-max-width: 280px;
--tooltip-font-size: 14px;
--tooltip-font-weight: 500;
--tooltip-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

/* Arrow */
--tooltip-arrow-size: 8px;
--tooltip-arrow-color: #1F2937;
```

### Arrow Indicator
```css
--arrow-size: 40px;
--arrow-color: #4F46E5;
--arrow-animation: bounce 1.5s ease-in-out infinite;
--arrow-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
```

---

## 🎨 ANIMATIONS

### Durations
```css
--duration-fast: 200ms;
--duration-normal: 300ms;
--duration-slow: 500ms;
--duration-screen-transition: 600ms;
```

### Easing Functions
```css
--ease-default: cubic-bezier(0.4, 0, 0.2, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
```

---

## 📐 RESPONSIVE BREAKPOINTS

```css
/* Desktop (Default) */
@media (min-width: 1024px) { /* styles above */ }

/* Tablet */
@media (max-width: 1023px) and (min-width: 640px) {
  --card-grid-columns: 2;
  --modal-max-width: 90%;
  --modal-padding: 32px;
}

/* Mobile */
@media (max-width: 639px) {
  --card-grid-columns: 1;
  --hero-headline-size: 32px;
  --modal-padding: 24px;
  --card-padding: 24px;
  /* Hide tooltips for clarity */
}
```

---

## 🔤 FONT LOADING

```html
<!-- Inter Font from Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 📏 Z-INDEX SCALE

```css
--z-base: 1;
--z-dropdown: 1000;
--z-sticky: 1100;
--z-fixed: 1200;
--z-modal-backdrop: 1300;
--z-modal: 1400;
--z-guidance: 1500;
--z-toast: 1600;
```

---

## ✅ VALIDATION STATES

### Input Field States
```css
/* Neutral (default) */
border: 2px solid #E5E7EB;

/* Focus */
border: 2px solid #4F46E5;
box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);

/* Error */
border: 2px solid #EF4444;
box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.1);

/* Success */
border: 2px solid #10B981;
box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1);
```

---

**Last Updated:** November 19, 2025
**Source:** Extracted from Scribe.com screenshots
**Status:** Ready for implementation
