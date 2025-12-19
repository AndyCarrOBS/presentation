# Magenta TV - Technical Specifications

## Operator Information
- **Country**: Austria
- **Operator**: Magenta TV
- **Technical Keywords**: IPTV operator STBs HbbTV OTT apps

## Specification Status

### Availability
- **Status**: ✅ PARTIALLY VERIFIED - Standard specs available, operator-specific may require NDA
- **Last Checked**: Mon Dec 15 12:37:51 PM GMT 2025

### Access Methods
- **Public Documentation**: ✅ Available for CI+ and HbbTV standards
- **Developer Portal**: To be verified
- **Technical Standards**: ✅ CI+ and HbbTV standards publicly available
- **Contact Required**: To be verified

### Technical Standards Used
Based on keywords: IPTV operator STBs HbbTV OTT apps

#### CI+ (Common Interface Plus)
- **Status**: To be verified
- **Version**: To be verified
- **Access**: CI+ Consortium specifications (standardized)
- **URL**: https://www.ci-plus.com/

#### IPTV (Internet Protocol Television)
- **Status**: ✅ Primary delivery method
- **Technology**: TV delivered over managed broadband networks
- **Delivery**: Linear, catch-up, and on-demand content using IP networks
- **Transport**: Multicast and unicast streaming
- **Note**: IPTV is the core delivery method for Magenta TV service

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

#### Cloud PVR / CDN / Streaming Backend
- **Status**: ✅ Supported
- **Purpose**: Backend services for time-shift and cloud DVR
- **Technology**: Cloud DVR/CDN infrastructure (Broadpeak) for scalable catch-up and start-over capabilities
- **Note**: Enables unlimited recording, catch-up, and cloud PVR features

#### OTT App Platforms
- **Status**: ✅ Supported
- **Platforms**: Tizen, webOS, Android TV, and other Smart TV OSes
- **Purpose**: Device-level apps for Smart TV viewing
- **Integration**: Bespoke apps on major smart TV OSes to reach viewers outside managed IPTV boxes
- **Note**: Third-party integrators (e.g., 3SS) build these apps

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

#### Other Technologies
- **IPTV**: To be verified
- **OTT**: To be verified
- **STB Specifications**: To be verified

## Search Queries Performed
1. "Magenta TV technical specifications"
2. "Magenta TV CI+ HbbTV specifications"
3. "Magenta TV developer portal"
4. "Magenta TV API documentation"

## Findings

### Standard Specifications Available

#### HbbTV (Hybrid Broadcast Broadband TV)
- **Status**: Available
- **Version**: HbbTV 2.0.1 (latest)
- **Access**: Public - HbbTV Consortium
- **URL**: https://www.hbbtv.org/
- **Notes**: Standardized specifications available publicly

### Operator-Specific Documentation
- **Status**: ⚠️ May require partnership/NDA
- **Access**: Contact operator directly
- **Developer Portal**: Check operator website
- **API Documentation**: May require registration

### Search Summary
- Standard specifications (CI+, HbbTV) are publicly available
- Operator-specific technical details may require partnership
- CAS vendor documentation may require NDA
- Contact operator for integration support
### Standard Specifications Available

#### HbbTV (Hybrid Broadcast Broadband TV)
- **Status**: Available
- **Version**: HbbTV 2.0.1 (latest)
- **Access**: Public - HbbTV Consortium
- **URL**: https://www.hbbtv.org/
- **Notes**: Standardized specifications available publicly

### Operator-Specific Documentation
- **Status**: ⚠️ May require partnership/NDA
- **Access**: Contact operator directly
- **Developer Portal**: Check operator website
- **API Documentation**: May require registration

### Search Summary
- Standard specifications (CI+, HbbTV) are publicly available
- Operator-specific technical details may require partnership
- CAS vendor documentation may require NDA
- Contact operator for integration support

## Contact Information

### Technical Specifications Access

- **Website**: https://www.magenta.at/
- **Parent Company**: Deutsche Telekom
- **Developer Portal**: Check Deutsche Telekom developer resources

**Note**: Contact Deutsche Telekom partner program or Magenta business development

### Senior Leadership (Deutsche Telekom / T-Mobile)

**CEO T-Mobile US (Former CEO Telekom Deutschland)**
- **Name**: Srini Gopalan
- **Title**: Current CEO of T-Mobile US, previously served as CEO of Telekom Deutschland (Germany)
- **Email**: srini.gopalan@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: United States / Germany
- **Note**: Responsible for fixed-network, broadband business, and IPTV product development in previous role at Telekom Deutschland. Magenta TV is a key product under his previous leadership.

**Board of Management Member - Europe Segment**
- **Name**: Dominique Leroy
- **Title**: Member of the Board of Management for Deutsche Telekom AG, responsible for the Europe segment
- **Email**: dominique.leroy@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Europe
- **Note**: Has experience managing European operations, including interim CEO role at Magenta Telekom in Austria. Responsible for Europe segment where Magenta TV operates.

**Board Member & Managing Director Telekom Deutschland**
- **Name**: Rodrigo Diehl
- **Title**: Board member at Deutsche Telekom AG and Managing Director of Telekom Deutschland GmbH
- **Email**: rodrigo.diehl@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Germany
- **Note**: Managing Director of Telekom Deutschland GmbH, the German subsidiary where Magenta TV service originates. Previously served as CEO of Magenta Telekom in Austria.

**CEO Magenta Telekom (Austria)**
- **Name**: Thomas Kicker
- **Title**: CEO of Magenta Telekom (Austria) since August 2025
- **Email**: thomas.kicker@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Current CEO of Magenta Telekom (Austria) with long history at the company, focusing on telecommunications, digital services, and AI.

**CFO Deutsche Telekom AG**
- **Name**: Dr. Christian P. Illek
- **Title**: CFO of Deutsche Telekom AG and T-Mobile US board member
- **Email**: christian.illek@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Germany
- **Note**: Previously oversaw international product development for Deutsche Telekom's fixed network, including IP TV, in a prior marketing director role at Telekom Deutschland.

**Magenta Telekom Austria Board Members**

**Chief Financial Officer**
- **Name**: Aleksander Bek
- **Title**: Chief Financial Officer, Magenta Telekom Austria
- **Email**: aleksander.bek@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Chief Financial Officer and Member of the Board at Magenta Telekom Austria

**Chief Human Resources Officer**
- **Name**: Christian Hauer
- **Title**: Chief Human Resources Officer, Magenta Telekom Austria
- **Email**: christian.hauer@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Chief Human Resources Officer and Member of the Board at Magenta Telekom Austria

**Chief Commercial Officer, Business**
- **Name**: Werner Kraus
- **Title**: Chief Commercial Officer, Business, Magenta Telekom Austria
- **Email**: werner.kraus@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Chief Commercial Officer, Business and Member of the Board at Magenta Telekom Austria

**Chief Technology & Information Officer**
- **Name**: Volker Libovsky
- **Title**: Chief Technology & Information Officer, Magenta Telekom Austria
- **Email**: volker.libovsky@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Chief Technology & Information Officer and Member of the Board at Magenta Telekom Austria. Key contact for technical specifications and Magenta TV platform.

**Chief Commercial Officer, Consumer**
- **Name**: Branko Stanchev
- **Title**: Chief Commercial Officer, Consumer, Magenta Telekom Austria
- **Email**: branko.stanchev@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Chief Commercial Officer, Consumer and Member of the Board at Magenta Telekom Austria. Key contact for consumer-facing products including Magenta TV.

**Chief Corporate Affairs Officer**
- **Name**: Anja Tretbar-Bustorf
- **Title**: Chief Corporate Affairs Officer and Member of the Board, Magenta Telekom Austria
- **Email**: anja.tretbar-bustorf@telekom.de (predicted)
- **Platform**: Corporate
- **Location**: Austria
- **Note**: Chief Corporate Affairs Officer and Member of the Board at Magenta Telekom Austria

### Detailed Contacts by Role

#### Market-Facing / Executive

**Market-facing (product/content)**
- **Name**: Christoph Ewerth
- **Title**: Head of Product & Content B2C (Magenta TV area)
- **Source**: LinkedIn
- **Note**: Market-facing (product/content)

#### Technology / Specifications

**Technology / onboarding owner**
- **Title**: Technology / onboarding owner
- **Note**: Technology / onboarding owner

### Recommended Contact Points
- **Business Development Department**: For partnership and integration discussions
- **Technical/Engineering Department**: For technical specifications and API access
- **Partner/Developer Relations**: For developer portal access and documentation
- **API/Integration Support Team**: For technical integration support

### Access Process
1. Visit operator website and look for 'Partner', 'Developer', or 'Business' sections
2. Contact business development department via website contact form or email
3. Request access to technical specifications and developer documentation
4. May require partnership agreement or NDA for detailed specifications
5. For M7 Group operators, contact M7 Group directly for unified platform specifications

## Next Steps
1. Perform web search for technical specifications
2. Check operator's developer portal (if available)
3. Contact operator for technical documentation
4. Review industry standard specifications (CI+, HbbTV)
5. Check for public API documentation

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
   - Integrate with Magenta backend APIs for login, entitlements, recommendations and playback
   - **Note**: Widely used by Magenta for smart TV clients

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
2. **Developer Integration**: Integrate Magenta APIs for streaming, authentication, entitlement enforcement
3. **Testing & QA**: Co-test on platform early, use test houses for pre-certification
4. **Commercial & Deployment**: Provide certification documentation, define operational support

## Notes
- This is an automated template - requires manual verification
- Specifications may require NDA or partnership agreement
- Some technical details may be proprietary
- Magenta TV is part of Deutsche Telekom's Europe TV portfolio
- Strong focus on live sports & OTT rights
- Modern cloud-based TV platform with features like unlimited recording
- Primary integration path: OTT App Integration (widely used by Magenta for smart TV clients)
- Cloud PVR/CDN infrastructure provided by Broadpeak
