# A1 Telekom Austria - Technical Specifications

## Operator Information
- **Country**: Austria
- **Operator**: A1 Telekom Austria (A1 TV)
- **Parent Company**: A1 Group (Telekom Austria AG)
- **Technical Keywords**: IPTV, OTT, operator STBs, HbbTV, A1 TV platform

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

#### IPTV (Internet Protocol Television)
- **Status**: ✅ Primary delivery method
- **Technology**: TV delivered over managed broadband networks
- **Delivery**: Linear, catch-up, and on-demand content using IP networks
- **Transport**: Multicast and unicast streaming
- **Note**: IPTV is the core delivery method for A1 TV service

#### HLS (HTTP Live Streaming)
- **Status**: ✅ Supported
- **Version**: HLS Version 7 with CMAF/fMP4 support
- **Purpose**: Adaptive streaming protocol over HTTP
- **Usage**: Common for OTT video delivery (live/VOD) on apps and Smart TV clients
- **Implementation**: A1's media player supports HLS for adaptive bitrate streaming
- **Note**: De-facto standard for live and VOD OTT delivery. Support for CMAF/fMP4 segments and modern adaptive live/VOD delivery required.

#### OTT App Platforms
- **Status**: ✅ Supported
- **Platforms**: Tizen, webOS, Android TV, and other Smart TV OSes
- **Purpose**: Device-level apps for Smart TV viewing
- **Integration**: Bespoke apps on major smart TV OSes to reach viewers outside managed IPTV boxes
- **Note**: A1 has delivered smart TV apps in other markets (e.g., Android TV deployments)

#### Cloud PVR / CDN / Streaming Backend
- **Status**: ✅ Supported
- **Purpose**: Backend services for time-shift and cloud DVR
- **Technology**: Cloud DVR/CDN infrastructure for scalable catch-up and start-over capabilities
- **Note**: Enables time-shifted viewing and cloud recording features

#### MPEG-DASH
- **Status**: ✅ Supported
- **Version**: ISO/IEC 23009-1:2022 (Edition 5)
- **Purpose**: Adaptive streaming protocol (MPD, segments) used by OTT TV services
- **DASH-IF Interoperability Points**: Common industry-accepted guidance (e.g., DASH-AVC/264, CMAF constraints) to ensure devices and services interoperate smoothly
- **Note**: Required for modern OTT TV service delivery

#### HbbTV (Hybrid Broadcast Broadband TV)
- **Status**: ⚠️ Limited adoption for TV delivery
- **Recommended Version**: HbbTV 2.0.4 (TS 102 796 v1.7.1) - preferred for broad hybrid support in Europe
- **Available Versions**:
  - HbbTV 1.5 (TS 102 796 v1.2.1) - Introduced adaptive streaming via MPEG-DASH
  - HbbTV 2.0.3 (TS 102 796 v1.6.1) - Adds better OTT support & modern web platform integration
  - HbbTV 2.0.4 (TS 102 796 v1.7.1) - Latest mainstream version with accessibility, DVB-I integration, updated web APIs
- **Usage**: Primarily used for audience measurement in Austria
- **HbbTV OpApp Specification**: Enables operator's app to behave like built-in STB UI on Smart TVs
- **Note**: In practice, Austrian telco TV services are OTT/IPTV first. HbbTV adoption is stronger on broadcaster side and measurement. HbbTV doesn't replace OTT/IPTV apps but complements them where broadcast channels and hybrid interactive services are desired.
- **URL**: https://www.hbbtv.org/

#### Conditional Access Systems
- **Status**: To be verified
- **Systems**: To be verified
- **Access**: Vendor-specific (may require NDA)

### Operator-Specific Documentation
- **Status**: ⚠️ May require partnership/NDA
- **Access**: Contact A1 Group directly
- **Developer Portal**: Check A1 Group website
- **API Documentation**: May require registration

## Market Position
- **Market Share**: ~26-27% of IPTV market share in Austria
- **Subscribers**: Part of A1 Group with ~5.1M mobile subs and 2.7M RGUs overall
- **Service Type**: IPTV + OTT bundled TV service
- **Integration**: Part of converged telco portfolio (fixed, mobile, digital services)

## Smart TV OS Partnership Likelihood
- **Rating**: ⭐⭐⭐ (Medium-High)
- **Reason**: A1 already has IPTV + OTT services and has delivered smart TV apps in other markets (e.g., Android TV deployments). Adding Austrian smart TV OS deals fits its tech profile.

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
1. **OTT App Integration** (Primary)
   - Build native Smart TV app supporting HLS/DASH playback, authentication, UI/UX, EPG data, and optional DRM
   - Deploy to major ecosystems (Tizen, webOS, Android TV) following platform guidelines
   - Integrate with A1 backend APIs for login, entitlements, recommendations and playback

2. **IPTV Multicast Support** (Optional)
   - **IGMP/DVB-IPI**: Support IPTV stacks via DVB-IPI or IGMP Multicast transport within managed home networks
   - **Note**: Less common for mass Smart TV app platforms (usually operator STBs handle IPTV). Only relevant if direct IPTV multicast support on the platform is targeted (often in managed operator STB worlds).

3. **Hybrid / HbbTV** (Optional)
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
1. **Technical Pre-Sales**: Share standards support matrix (HLS/DASH, DRM, HbbTV, IPTV)
2. **Developer Integration**: Integrate A1 APIs for streaming, authentication, entitlement enforcement
3. **Testing & QA**: Co-test on platform early, use test houses for pre-certification
4. **Commercial & Deployment**: Provide certification documentation, define operational support

## Notes
- A1 Group reported strong financial performance: 3.1% revenue growth (€5.41 billion, 2024)
- SimpliTV SAT and SimpliTV Terrestrial are also operated by A1 Telekom Austria
- A1 TV is bundled with broadband and mobile offerings
- Part of A1 Group's converged services strategy
- Primary integration path: OTT App Integration (most common route for OTT-centric operators)

## Contact Information
- **Website**: https://www.a1.net/
- **Parent Company**: A1 Group (Telekom Austria AG)
- **Note**: Contact A1 Group business development for technical specifications

