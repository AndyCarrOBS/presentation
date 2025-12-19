# ServusTV - Technical Specifications

## Operator Information
- **Country**: Austria
- **Operator**: ServusTV
- **Type**: Commercial Broadcaster
- **Technical Keywords**: HbbTV, broadcast, OTT, on-demand

## Specification Status

### Availability
- **Status**: ✅ VERIFIED - HbbTV services deployed
- **Last Checked**: December 2025

### Access Methods
- **Public Documentation**: ✅ Available for HbbTV standards
- **Developer Portal**: To be verified
- **Technical Standards**: ✅ HbbTV standards publicly available
- **Contact Required**: ⚠️ May require contact for broadcaster-specific integration

### Technical Standards Used

#### HbbTV (Hybrid Broadcast Broadband TV)
- **Status**: ✅ Actively Used
- **Version**: HbbTV 2.0.4 (TS 102 796 v1.7.1) - preferred for broad hybrid support
- **Deployment**: ServusTV has deployed HbbTV services
- **Launch**: In 2020, ServusTV launched a catch-up/on-demand service using HbbTV 2.0 standard
- **Features**: 
  - Enables viewers with HbbTV-compatible TVs to access additional content from the broadcaster
  - Access via the red button interface on remote control
  - Catch-up and on-demand services
- **Portal Integration**: ServusTV content is included in HbbTV portals in Austria alongside other broadcasters when viewers press the red button on their remote
- **Measurement**: Testing of HbbTV-based measurement and data tools has specifically involved ServusTV, indicating active engagement with the standard from a measurement integration perspective
- **Access**: HbbTV Consortium specifications (standardized)
- **URL**: https://www.hbbtv.org/

#### OTT/Streaming Platform
- **Status**: ✅ Supported
- **Service**: ServusTV On Demand
- **Platform**: OTT streaming service
- **Note**: Commercial broadcaster with OTT streaming capabilities

### Operator-Specific Documentation
- **Status**: ⚠️ May require partnership/contact
- **Access**: Contact ServusTV directly
- **Developer Portal**: Check ServusTV website
- **API Documentation**: May require registration

## Market Position
- **Type**: Commercial broadcaster in Austria
- **Service**: Free-to-air commercial TV with HbbTV interactive services
- **OTT Service**: ServusTV On Demand

## Smart TV OS Integration Requirements

### Streaming & Playback Standards
- **HLS (HTTP Live Streaming)**: ✅ Required
  - **Version**: HLS Version 7 with CMAF/fMP4 support
- **MPEG-DASH**: ✅ Required
  - **Version**: ISO/IEC 23009-1:2022 (Edition 5)

#### Codec Support
- **H.264/AVC**: ✅ Required
- **HEVC (H.265)**: ✅ Required for UHD/4K content
- **AV1**: Optional - where possible

#### DRM & Content Protection
- **Widevine Modular**: ✅ Required
- **Microsoft PlayReady**: ✅ Required
  - **Version**: PlayReady 3.3+ on newer TVs
- **CENC Common Encryption (ISO-BMFF)**: ✅ Required
- **HDCP**: ✅ Required
  - **HDCP 1.4**: Required for <1080p content
  - **HDCP 2.2**: Required for UHD/4K

### Service Integration
- **Authentication**: OAuth/OpenID Connect for login & entitlements APIs
- **EPG / Metadata APIs**: Required for program guides and metadata sync
- **Push Notifications**: For updates, billing, service alerts
- **DVB-I Service Discovery**: Emerging standard for internet-delivered TV channel lists

### Smart TV Integration Paths
1. **Hybrid / HbbTV** (Primary)
   - **HbbTV Version**: Target HbbTV 2.0.4 (TS 102 796 v1.7.1) compliance
   - **HbbTV OpApp**: Support operator app extension spec (enabling operator UI)
   - **Signal Discovery**: Required for hybrid broadcast + broadband
   - **Web Technologies**: 
     - ECMAScript / HTML5 / CSS3 - latest recommended features for interactive UI
     - Encrypted Media Extensions (EME) - required in browsers/HTML5 players for DRM integration
   - **Red Button Interface**: Access to HbbTV services via red button on remote control

2. **OTT App Integration** (Secondary)
   - Build native Smart TV app supporting HLS/DASH playback, authentication, UI/UX, EPG data
   - Deploy to major ecosystems (Tizen, webOS, Android TV)
   - Integrate with ServusTV backend APIs for login, entitlements, recommendations and playback

### Media Container Standards
- **ISO BMFF (ISO/IEC 14496-12)**: ✅ Required - base file format for DASH & CMAF
- **CMAF (ISO/IEC 23000-19)**: ✅ Required - increasingly used for converged DASH/HLS content delivery

### Testing & Certification

#### Test Suites & Tools
- **HbbTV Test Suite**: v2025-2 - latest comprehensive set of conformance tests
- **DASH-IF / HbbTV Adaptive Streaming Validator**: Verifies MPD and segment conformance

#### Test Houses / Labs
- **HbbTV Test Centre** (Digital TV Labs / Sofia Digital): Full HbbTV conformance testing
- **iWedia**: Provides test tools (HbbTV Harness) to support compliance
- **ACCESS Europe / NetRange**: Integrated HbbTV browser and test environments
- **DVB/HbbTV Interop events & labs**: Multi-vendor interoperability events

#### Certification Requirements
- **Android TV/Google**: Platform certification required
- **webOS**: Platform certification required
- **Tizen**: Platform certification required

## Notes
- ServusTV is a commercial broadcaster in Austria
- Actively uses HbbTV 2.0 for catch-up and on-demand services
- Part of the Austrian HbbTV ecosystem alongside ORF
- HbbTV services accessible via red button interface on compatible Smart TVs
- Engaged with HbbTV-based measurement and data tools

## Contact Information
- **Website**: https://www.servustv.com/
- **Note**: Contact ServusTV business development for technical specifications and HbbTV integration

