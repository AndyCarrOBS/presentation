# OBS Presentation - Operator Markets Overview

An interactive presentation showcasing European TV operator markets with an interactive map, country data, and flow diagrams.

## Quick Start

### Option 1: Python HTTP Server (Recommended)

1. Open a terminal in this directory
2. Run one of these commands:

**Python 3:**
```bash
python3 -m http.server 8000
```

**Python 2:**
```bash
python -m SimpleHTTPServer 8000
```

3. Open your browser and navigate to:
   ```
   http://localhost:8000/index.html
   ```

### Option 2: Node.js HTTP Server

If you have Node.js installed:

```bash
npx http-server -p 8000
```

Then open: `http://localhost:8000/index.html`

### Option 3: VS Code Live Server

If you're using VS Code:
1. Install the "Live Server" extension
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 4: PHP Built-in Server

If you have PHP installed:

```bash
php -S localhost:8000
```

Then open: `http://localhost:8000/index.html`

## Project Structure

```
presentation/
├── index.html              # Main presentation file
├── img/                    # Image assets
│   ├── OBS-Logo.png       # OBS logo
│   └── roku-logo.png      # Roku logo
└── README.md              # This file
```

## Features

- **Slide 1**: Title screen with OBS branding
- **Slide 2**: Agenda
- **Slide 3**: Interactive Europe map with country data
  - Filter by CI+ countries
  - Filter by Nordic DVB countries
  - Filter by HbbTV countries
  - Click countries to see operator details
- **Slide 4**: Two-column flow diagrams (Spec Based & Test Strategy)
- **Slide 5**: Framework diagram with ellipses and numbered boxes

## Navigation

- Use the **←** and **→** arrow buttons to navigate between slides
- Click on countries in the map to view operator information
- Use filter buttons to highlight specific country groups

## Requirements

- A modern web browser (Chrome, Firefox, Safari, Edge)
- A local HTTP server (cannot use `file://` protocol due to browser security restrictions)
- Internet connection (for loading Leaflet.js and map data from CDN)

## Dependencies

All dependencies are loaded from CDN:
- Leaflet.js (for interactive maps)
- TopoJSON Client (for map data processing)

No installation or build process required!

## Exporting/Sharing

To share this presentation:

1. **Zip the entire folder** including:
   - `index.html`
   - `img/` folder with all images
   - `README.md` (optional but helpful)

2. **Share the zip file** with recipients

3. **Recipients should**:
   - Extract the zip file
   - Follow the Quick Start instructions above
   - Open `http://localhost:8000/index.html` in their browser

## Troubleshooting

**Map not loading?**
- Make sure you're using `http://localhost` and not `file://`
- Check your internet connection (map data loads from CDN)
- Check browser console for errors (F12)

**Images not showing?**
- Ensure the `img/` folder is in the same directory as `index.html`
- Check that image filenames match exactly (case-sensitive)

**Port 8000 already in use?**
- Use a different port: `python3 -m http.server 8080`
- Update the URL accordingly: `http://localhost:8080/index.html`

## Browser Compatibility

Tested and working on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

Internal use only - OBS Presentation

