# Drei Austria (Hutchison Drei Austria) - Technical Specifications

## Operator Information
- **Country**: Austria
- **Operator**: Drei Austria (3 / Hutchison Drei Austria)
- **Parent Company**: CK Hutchison Holdings
- **Technical Keywords**: OTT streaming, TV apps, mobile TV, streaming service

## Specification Status

### Availability
- **Status**: ⚠️ PENDING VERIFICATION
- **Last Checked**: December 2025

### Access Methods
- **Public Documentation**: To be verified
- **Developer Portal**: To be verified
- **Technical Standards**: To be verified
- **Contact Required**: ⚠️ Yes - for operator-specific documentation

### Technical Standards Used

#### OTT/Streaming Platform
- **Status**: ✅ Primary delivery method - Drei TV is an OTT streaming service
- **Technology**: App-based OTT streaming, works across any broadband network
- **Platform**: Not tied to proprietary set-top boxes or multicast
- **Delivery**: More OTT/app-centric than traditional IPTV boxes
- **Features**: Live TV, time-shifted viewing, personal recorder options

#### HLS (HTTP Live Streaming)
- **Status**: ✅ Supported
- **Version**: HLS Version 7 with CMAF/fMP4 support
- **Purpose**: Adaptive streaming protocol over HTTP
- **Usage**: Common for OTT video delivery (live/VOD) on apps and Smart TV clients
- **Note**: De-facto standard for live and VOD OTT delivery. Support for CMAF/fMP4 segments and modern adaptive live/VOD delivery required.

#### MPEG-DASH
- **Status**: ✅ Supported
- **Version**: ISO/IEC 23009-1:2022 (Edition 5)
- **Purpose**: Adaptive streaming protocol (MPD, segments) used by OTT TV services
- **DASH-IF Interoperability Points**: Common industry-accepted guidance (e.g., DASH-AVC/264, CMAF constraints) to ensure devices and services interoperate smoothly
- **Note**: Required for modern OTT TV service delivery

#### OTT App Platforms
- **Status**: ✅ Supported
- **Platforms**: Tizen, webOS, Android TV, and other Smart TV OSes
- **Purpose**: Device-level apps for Smart TV viewing
- **Integration**: Bespoke apps on major smart TV OSes
- **Note**: Third-party integrators (e.g., 3SS) build these apps

#### Mobile TV / TV Everywhere
- **Status**: ✅ Supported
- **Platform**: Android app available (hundreds of thousands of downloads)
- **Devices**: Phones and connected devices
- **Delivery**: OTT streaming via app

#### HbbTV (Hybrid Broadcast Broadband TV)
- **Status**: ⚠️ Limited adoption for TV delivery
- **Recommended Version**: HbbTV 2.0.4 (TS 102 796 v1.7.1) - preferred for broad hybrid support in Europe
- **Available Versions**:
  - HbbTV 1.5 (TS 102 796 v1.2.1) - Introduced adaptive streaming via MPEG-DASH
  - HbbTV 2.0.3 (TS 102 796 v1.6.1) - Adds better OTT support & modern web platform integration
  - HbbTV 2.0.4 (TS 102 796 v1.7.1) - Latest mainstream version with accessibility, DVB-I integration, updated web APIs
- **Usage**: Primarily used for audience measurement in Austria
- **HbbTV OpApp Specification**: Enables operator's app to behave like built-in STB UI on Smart TVs
- **Note**: In practice, Austrian telco TV services are OTT/IPTV first. HbbTV adoption is stronger on broadcaster side and measurement.
- **URL**: https://www.hbbtv.org/

#### Conditional Access Systems
- **Status**: To be verified
- **Systems**: To be verified
- **Access**: Vendor-specific (may require NDA)

### Operator-Specific Documentation
- **Status**: ⚠️ May require partnership/NDA
- **Access**: Contact Drei Austria directly
- **Developer Portal**: Check Drei Austria website
- **API Documentation**: May require registration

## Market Position
- **Market Share**: Smaller relative footprint compared to A1 and Magenta
- **Subscribers**: No authoritative public subscriber tally available
- **Service Type**: OTT streaming TV service
- **Positioning**: App-centric service, strategically positioned offering

## Smart TV OS Partnership Likelihood
- **Rating**: ⭐⭐ (Medium)
- **Reason**: App-centric service is inherently compatible with smart TV platforms, but operator size and strategic focus might be narrower than A1/Magenta.

## Smart TV OS Integration Requirements

### Streaming & Playback Standards

#### Streaming Protocols
- **HLS (HTTP Live Streaming)**: ✅ Required
  - **Version**: HLS Version 7 with CMAF/fMP4 support
  - **Purpose**: De-facto standard for live and VOD OTT delivery
- **MPEG-DASH**: ✅ Required
  - **Version**: ISO/IEC 23009-1:2022 (Edition 5)
  - **DASH-IF Interoperability Points**: DASH-AVC/264, CMAF constraints
  - **Purpose**: Adaptive streaming protocol (MPD, segments) used by OTT TV services

#### Codec Support
- **H.264/AVC**: ✅ Required
- **HEVC (H.265)**: ✅ Required for UHD/4K content
- **AV1**: Optional - where possible

#### DRM & Content Protection
- **Widevine Modular**: ✅ Required
  - **Profile**: Industry "Modular" DRM profile (common on Android TV, many smart TV platforms)
- **Microsoft PlayReady**: ✅ Required
  - **Version**: PlayReady 3.3+ on newer TVs (legacy support down to ~1.2/2.5 historically)
- **CENC Common Encryption (ISO-BMFF)**: ✅ Required
  - **Purpose**: Required for MPEG-DASH CMAF & HLS fMP4 DRM
- **HDCP**: ✅ Required
  - **HDCP 1.4**: Required for <1080p content
  - **HDCP 2.2**: Required for UHD/4K on devices enforcing secure output

### Service Integration
- **Authentication**: OAuth/OpenID Connect for login & entitlements APIs
- **EPG / Metadata APIs**: Required for program guides and metadata sync
- **Push Notifications**: For updates, billing, service alerts
- **DVB-I Service Discovery**: Emerging standard for internet-delivered TV channel lists (increasingly used in Europe)

### Smart TV Integration Paths
1. **OTT App Integration** (Primary - Most Common)
   - Build native Smart TV app supporting HLS/DASH playback, authentication, UI/UX, EPG data, and optional DRM
   - Deploy to major ecosystems (Tizen, webOS, Android TV) following platform guidelines
   - Integrate with Drei backend APIs for login, entitlements, recommendations and playback
   - **Note**: This is the most common route for OTT-centric operators like Drei

2. **Hybrid / HbbTV** (Optional)
   - **HbbTV Version**: Target HbbTV 2.0.4 (TS 102 796 v1.7.1) compliance for broad hybrid support in Europe
   - **HbbTV OpApp**: Support operator app extension spec (enabling operator UI)
   - **Signal Discovery**: Required for hybrid broadcast + broadband
   - **Web Technologies**: 
     - ECMAScript / HTML5 / CSS3 - latest recommended features for interactive UI
     - Encrypted Media Extensions (EME) - required in browsers/HTML5 players for DRM integration (Widevine/PlayReady)

### Media Container Standards
- **ISO BMFF (ISO/IEC 14496-12)**: ✅ Required - base file format for DASH & CMAF
- **CMAF (ISO/IEC 23000-19)**: ✅ Required - increasingly used for converged DASH/HLS content delivery

### Testing & Certification

#### Test Suites & Tools
- **HbbTV Test Suite**: v2025-2 - latest comprehensive set of conformance tests (DRM, web APIs, hybrid functions)
  - Available via Registered Test Centres or membership
- **DASH-IF / HbbTV Adaptive Streaming Validator**: Verifies MPD and segment conformance to ISO/IEC 23009-1 and CMAF profiles

#### Test Houses / Labs
- **HbbTV Test Centre** (Digital TV Labs / Sofia Digital): Full HbbTV conformance testing including OpApp, DRM test cases
- **iWedia**: Provides test tools (HbbTV Harness) to support compliance and streamline certification
- **ACCESS Europe / NetRange**: Integrated HbbTV browser and test environments for device platforms (HbbTV + operator apps)
- **DVB/HbbTV Interop events & labs**: Multi-vendor interoperability events covering DVB-I, DASH, HbbTV
- **Vendor DRM certification partners**: Required for certified Widevine/PlayReady device licensing
- **Platform test frameworks**: OS-specific CI/CD tests for media playback & DRM integration (Google/Tizen/webOS)

#### Certification Requirements
- **Android TV/Google**: Platform certification required
- **webOS**: Platform certification required
- **Tizen**: Platform certification required

### Engagement Strategy
1. **Technical Pre-Sales**: Share standards support matrix (HLS/DASH, DRM, HbbTV)
2. **Developer Integration**: Integrate Drei APIs for streaming, authentication, entitlement enforcement
3. **Testing & QA**: Co-test on platform early, use test houses for pre-certification
4. **Commercial & Deployment**: Provide certification documentation, define operational support

## Notes
- Drei offers mobile, fixed broadband and packages that include TV
- Drei TV Android app shows hundreds of thousands of downloads
- More OTT-focused than traditional IPTV operators
- Part of CK Hutchison's European operations
- Primary integration path: OTT App Integration (most common route for OTT-centric operators)

## Contact Information
- **Website**: https://www.drei.at/
- **Parent Company**: CK Hutchison Holdings
- **Note**: Contact Drei Austria business development for technical specifications

