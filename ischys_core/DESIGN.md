---
name: Ischys Core
colors:
  surface: '#fbf9f2'
  surface-dim: '#dcdad3'
  surface-bright: '#fbf9f2'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f4ec'
  surface-container: '#f0eee7'
  surface-container-high: '#eae8e1'
  surface-container-highest: '#e4e2dc'
  on-surface: '#1b1c18'
  on-surface-variant: '#454841'
  inverse-surface: '#30312c'
  inverse-on-surface: '#f3f1ea'
  outline: '#757871'
  outline-variant: '#c5c7bf'
  surface-tint: '#596153'
  primary: '#474f42'
  on-primary: '#ffffff'
  primary-container: '#5f6759'
  on-primary-container: '#dde5d4'
  inverse-primary: '#c1c9b8'
  secondary: '#7f5533'
  on-secondary: '#ffffff'
  secondary-container: '#fec69c'
  on-secondary-container: '#79512f'
  tertiary: '#424e5b'
  on-tertiary: '#ffffff'
  tertiary-container: '#5a6673'
  on-tertiary-container: '#d7e4f3'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde5d4'
  primary-fixed-dim: '#c1c9b8'
  on-primary-fixed: '#161e13'
  on-primary-fixed-variant: '#41493c'
  secondary-fixed: '#ffdcc3'
  secondary-fixed-dim: '#f2bb92'
  on-secondary-fixed: '#2f1500'
  on-secondary-fixed-variant: '#633e1e'
  tertiary-fixed: '#d7e4f3'
  tertiary-fixed-dim: '#bbc8d7'
  on-tertiary-fixed: '#101d28'
  on-tertiary-fixed-variant: '#3c4854'
  background: '#fbf9f2'
  on-background: '#1b1c18'
  surface-variant: '#e4e2dc'
  background-ivory: '#F2F0E9'
  text-charcoal: '#1A1A1A'
  sage-muted: '#5F6759'
  clay-warm: '#C6946D'
  slate-blue: '#313D49'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '600'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 28px
    fontWeight: '500'
    lineHeight: 36px
  headline-md:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.03em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  section-gap: 80px
  content-gap: 32px
  margin-desktop: 64px
  margin-mobile: 20px
  gutter: 24px
---

## Brand & Style
The design system is built on the philosophy of "unhurried excellence." For a boutique psychiatric practice, the UI must balance medical credibility with a deeply human, personal touch. It rejects the cold, sterile nature of large health-tech platforms in favor of a "digital sanctuary"—a space that feels as intentional and calm as a well-appointed private office.

The aesthetic blends **Minimalism** with **Modern-Organic** influences. It prioritizes clarity and breathability, using generous whitespace to reduce cognitive load for patients who may be in distress. The visual language is restrained and sophisticated, avoiding typical wellness clichés to maintain an atmosphere of professional wisdom and compassionate authority.

## Colors
The palette is rooted in a warm, non-white foundation to avoid clinical coldness. 
- **Primary (Sage):** Used for key structural elements and primary actions, representing growth and stability.
- **Secondary (Clay):** An accent for warmth and human connection, used sparingly for highlights or subtle callouts.
- **Tertiary (Slate Blue-Gray):** Provides professional grounding and is used for secondary interactive elements.
- **Neutral (Ivory/Cream):** The primary background color, creating a soft, paper-like surface.
- **Typography:** Deep charcoal (#1A1A1A) is used instead of pure black to maintain high contrast while appearing more organic and softer on the eyes.

## Typography
The typography strategy pairings "Authority" with "Accessibility."
- **Headlines:** Playfair Display is used for its scholarly and timeless character. It should be typeset with slightly tighter letter-spacing in larger sizes to maintain a bespoke, editorial feel.
- **Body & Labels:** Inter provides a clean, neutral counterpoint. It ensures that critical medical information is legible and accessible.
- **Hierarchy:** Use large display type for welcoming moments and strictly controlled heading levels for structured information. Labels use slightly increased letter-spacing and semi-bold weights for clear categorization.

## Layout & Spacing
This design system utilizes a **Fixed Grid** on desktop (max-width 1200px) and a fluid layout on mobile devices. 
- **The "Unhurried" Rhythm:** Spacing is intentionally generous. Section gaps are larger than standard SaaS patterns to allow the user's eyes to rest.
- **Grid:** A 12-column grid for desktop with 24px gutters. Content should often be centered or offset to create an asymmetrical, custom-designed feel.
- **Mobile:** On mobile, margins reduce to 20px, and vertical spacing remains high to prevent the "cramped" feeling often associated with medical forms.

## Elevation & Depth
Depth is conveyed through **Tonal Layers** rather than heavy shadows. 
- **Surface Tiers:** Use subtle shifts in background color (e.g., a slightly darker ivory or a very soft sage tint) to differentiate content blocks.
- **Subtle Dividers:** Use 1px borders in a low-opacity version of the text color (10-15% opacity) to separate sections without creating visual noise.
- **Shadows:** If used for high-priority modals, shadows must be extremely diffused and "ambient," utilizing a tint of the tertiary blue-gray color instead of pure gray to maintain the palette's warmth.

## Shapes
The shape language is consistently **Rounded**. 
- A 0.5rem (8px) base radius is applied to standard components like inputs and small cards. 
- Larger containers or sections can use `rounded-xl` (24px) to create a softer, more approachable frame for the content.
- Circles are reserved exclusively for avatars or specific status indicators to maintain the "medically credible" structure.

## Components
- **Buttons:** Primary buttons use the Sage green with white text. Secondary buttons use a Slate Blue-Gray outline. Buttons should have a generous internal padding (16px top/bottom, 32px left/right) to feel significant and easy to interact with.
- **Inputs:** Form fields use a solid ivory background with a 1px border. Focus states should use a soft Sage glow. Labels are always positioned above the field for maximum legibility.
- **Cards:** Cards should have no border; instead, use a slightly different tonal background from the main page or a very soft ambient shadow. They are used to group therapist bios or service descriptions.
- **Chips/Tags:** Used for "Specialties" or "Focus Areas," these should use a soft Clay or Sage background with low saturation to remain secondary to the main text.
- **Minimal Icons:** Icons should be thin-stroke (2pt) and strictly functional. Use them for navigation or contact methods only, avoiding decorative or "playful" iconography.