# Europe Map Source Information

## Recommended Sources for Europe SVG Map

### Option 1: SimpleMaps (Recommended)
- **URL**: https://simplemaps.com/resources/svg-europe
- **License**: Free for commercial and personal use (attribution appreciated)
- **File Size**: ~59 KB
- **Features**: 
  - Individual country paths with ISO codes
  - Optimized for web use
  - Ready for interactive features

**Download Instructions**:
1. Visit the URL above
2. Click the download button
3. Save as `img/europe-map.svg`
4. The SVG will have country paths with IDs like `id="AT"` (Austria), `id="BE"` (Belgium), etc.

### Option 2: Ultimaps
- **URL**: https://ultimaps.com/blank-maps/europe/
- **License**: Free for personal and commercial use with attribution
- **Formats**: SVG, PNG, PDF
- **Features**: High-resolution, blank maps suitable for presentations

### Option 3: Use JavaScript Library

Instead of a static SVG, you can use a JavaScript library that generates the map:

#### Leaflet.js + GeoJSON
- Library: https://leafletjs.com/
- Requires: GeoJSON data for Europe
- Pros: Well-documented, mobile-friendly

#### D3.js + TopoJSON
- Library: https://d3js.org/
- Requires: TopoJSON data
- Pros: Highly customizable, powerful

#### jsVectorMap
- Library: https://github.com/themustafaomar/jsvectormap
- Pros: Lightweight, simple API
- Cons: May require paid version for commercial use

## Current Status

A placeholder SVG file has been created at `img/europe-map.svg`. 

**Next Steps**:
1. Download a full SVG map from one of the sources above
2. Replace `img/europe-map.svg` with the downloaded file
3. Ensure country paths have identifiable IDs or classes matching country names from `country.md`

## Country Name Mapping

The `country.md` file uses these country names:
- Austria, Belgium, Croatia, Czech, Denmark, Estonia, Finland, France, Germany, Hungary, Ireland, Italy, Luxemburg, Netherlands, Norway, Poland, Romania, Serbia, Slovakia, Spain, Sweden, Switzerland, UK

When implementing the interactive map, you'll need to map these names to the SVG path IDs/classes in the downloaded map.



