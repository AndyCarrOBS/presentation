# Project Requirements: OBS Presentation Website

## Project Overview
A website to present a set of slide decks to a partner. The presentation should be branded with OBS and include a footer indicating it was prepared for Roku.

## Branding Requirements

### Logo Assets
- **OBS Logo**: `img/OBS-Logo.png` (exists)
- **Roku Logo**: `img/roku-logo.png` (exists)

### Branding Elements
- All pages must be branded with OBS logo
- Footer on all pages must display: "prepared for Roku"
- Footer should include Roku logo

## Slide Structure

### Slide 1: Title Screen
- Simple title screen
- Should include OBS branding
- Footer: "prepared for Roku"

### Slide 2: Agenda Page
- Display agenda items:
  1. Overview of Operator Markets
  2. 2 ways to approach the problem
  3. What has worked
  4. Key Steps for Success
- OBS branding
- Footer: "prepared for Roku"

### Slide 3: Interactive Europe Map
- Display a map of Europe
- **Hover Functionality**:
  - As mouse moves around the map, highlight the country under the cursor
  - Display the country name when hovering
- **Click Functionality**:
  - When a country is clicked, display an overlay/modal
  - Overlay should show information about the selected country
  - Country information source: `country.md` file
- OBS branding
- Footer: "prepared for Roku"

## Data Source

### Country Information
- Country data is stored in `country.md`
- Format: Markdown table with country names and associated operators/services
- Countries included: Austria, Belgium, Croatia, Czech Republic, Denmark, Estonia, Finland, France, Germany, Hungary, Ireland, Italy, Luxembourg, Netherlands, Norway, Poland, Romania, Serbia, Slovakia, Spain, Sweden, Switzerland, UK, and others

## Technical Requirements

### Interactive Map Features
- Map of Europe with clickable countries
- Hover effects for country highlighting
- Country name display on hover
- Click-to-view country details overlay
- Parse and display country information from `country.md`

### User Experience
- Smooth transitions between slides
- Responsive design
- Professional presentation appearance
- Easy navigation between slides

## File Structure
```
presentation/
├── country.md          # Country data source
├── img/
│   ├── OBS-Logo.png   # OBS branding logo
│   └── roku-logo.png  # Roku branding logo
└── req.md             # This requirements document
```

