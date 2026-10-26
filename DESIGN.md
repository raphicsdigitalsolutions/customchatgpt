---
version: alpha
colors:
  light:
    background: "#f3f2ec"
    surface: "#fffefa"
    ink: "#172b36"
    muted: "#61737a"
    line: "#dbe4df"
    accent: "#147d89"
    highlight: "#26aab0"
    gold: "#a77937"
  dark:
    background: "#07131d"
    surface: "#102431"
    ink: "#edf5f1"
    muted: "#a8b9bc"
    line: "#29434b"
    accent: "#63d6d4"
    highlight: "#a8eee4"
    gold: "#e0c47d"
typography:
  display:
    fontFamily: "Manrope, sans-serif"
  sans:
    fontFamily: "DM Sans, sans-serif"
rounded:
  control: "0.75rem"
  card: "1.1rem"
  feature: "1.7rem"
spacing:
  compact: "0.5rem"
  standard: "1rem"
  spacious: "1.75rem"
components:
  creatorSignature:
    surface: "theme aware glass card"
    size: "compact and prominent above the workspace"
  workspaceHeader:
    surface: "theme aware glass bar"
  assistantHero:
    layout: "asymmetric copy and animated robot"
  promptActions:
    layout: "four compact actions on desktop"
  conversation:
    scroll: "bounded transcript with fixed composer"
---

## Overview

NEXORA is a personal AI workspace. Its visual signature is a small, expressive glass-shell robot beside the welcome message. The screen should read as a focused workbench: creator credit, workspace identity, one clear prompt, useful starter actions, then the composer.

The existing ocean teal and champagne palette is the product identity. Day and night modes keep the same hierarchy and materials while changing contrast. Runtime theme values are owned by `chatgpt.py` (`_palette`) and `nexora_3d.py` (`_TOKENS`); CSS consumes the matching `--nx-*` variables.

## Colors

Use warm mineral white and deep blue-green as the two canvas surfaces. Teal signals the primary action and live assistant state. Champagne is reserved for small signature details, not large text or broad fills. Keep body text high contrast in both modes.

## Typography

Use Manrope for the main display heading and DM Sans for the interface, controls, and labels. The display title belongs in the hero only. Keep captions small and quiet while preserving readable contrast and complete labels.

## Layout

On desktop, fit the workspace within the visible app viewport. Keep the creator signature at the top, the workspace header below it, and the hero in a two-column grid with copy on the left and robot on the right. Keep starter actions compact and the message composer anchored at the bottom. Long conversation history scrolls inside its own panel. On narrow screens, stack the robot and copy and let the document grow naturally so controls remain reachable.

## Elevation & Depth

Use one consistent overhead highlight, translucent surfaces, thin inner edges, and shadows tinted toward blue-green. The robot uses dimensional shell highlights and slow orbit rings. Its motion should never compete with the prompt or chat input.

## Shapes

Use rounded rectangles for controls, larger radii for the creator signature and hero panel, and circular orbit details only around the robot. Avoid giving every element the same pill shape.

## Components

The creator signature preserves the wording “Created by Atta ur Rehman” and “A student of Sir Iqbal.” The hero robot is an inline SVG with CSS animation, theme-aware shell colors, and a reduced-motion state. Suggestion buttons continue to submit their existing prompt actions. The chat transcript owns its overflow; the page shell does not scroll on standard desktop screens.

## Do's and Don'ts

Do keep the assistant face, creator credit, prompt, and message field visible together on desktop. Do keep controls keyboard accessible and preserve the reduced-motion preference. Don't add decorative cards that push the composer below the fold. Don't hide a scrollbar inside the conversation or sidebar.
