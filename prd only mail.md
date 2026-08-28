# ClickWise - Product Requirements Document (PRD)

## Executive Summary

**Product Name:** ClickWise  
**Version:** 1.0  
**Last Updated:** August 27, 2026  
**Status:** Development Phase

ClickWise is a browser extension that provides real-time, autonomous email threat investigation directly within Gmail. It combines agentic AI with forensic analysis to detect phishing, spoofing, and business email compromise (BEC) attacks at the moment of maximum risk—when a user opens a suspicious email.

---

## 1. Problem Statement

### 1.1 Current Challenges
- **Email remains the #1 attack vector** for phishing, BEC, and credential theft
- **Hidden evidence** exists in email headers but requires expert-level analysis
- **Existing solutions are disconnected** from the user's workflow:
  - Spam filters give silent yes/no verdicts with no explanation
  - Forensic tools exist separately from email clients
  - Manual header analysis requires specialized knowledge
- **Critical timing gap:** No protection at the moment when a user is about to click a malicious link

### 1.2 Target Problem
Users need **immediate, evidence-based warnings** when opening suspicious emails, with investigation happening automatically and results presented in plain language, directly within their inbox.

---

## 2. Goals & Objectives

### 2.1 Primary Goals
1. **Autonomous Investigation:** Automatically analyze suspicious emails without user action
2. **Real-time Warning:** Provide immediate threat assessment as emails are opened
3. **Explainable Evidence:** Present technical findings in accessible language
4. **Zero Friction:** Integrate seamlessly into existing Gmail workflow

### 2.2 Success Criteria
- **Detection Performance:**
  - Precision: ≥ 95% (minimize false positives)
  - Recall: ≥ 90% (catch most threats)
  - False Positive Rate: ≤ 5%
- **Speed:** Warning displayed within 3 seconds of opening suspicious email
- **User Experience:** Non-technical users understand warnings without training
- **Reliability:** 99%+ success rate in extracting and analyzing headers

### 2.3 SDG Alignment
| SDG | Contribution |
|-----|-------------|
| **SDG 9** | Innovation in browser-native forensic tooling |
| **SDG 16** | Supports cybercrime investigation and evidence gathering |
| **SDG 10** | Democratizes analyst-grade security capabilities |
| **SDG 1** | Prevents financial fraud before money transfer |

---

## 3. User Personas

### 3.1 Primary Personas

#### Persona 1: Corporate Employee (Sarah)
- **Role:** Marketing Manager at mid-size company
- **Tech Proficiency:** Intermediate
- **Pain Points:**
  - Receives dozens of emails daily from unknown senders
  - Has clicked phishing links in the past
  - Doesn't know how to verify email authenticity
- **Goals:** 
  - Quickly identify dangerous emails
  - Understand why an email is suspicious
  - Avoid embarrassing security incidents

#### Persona 2: IT Security Analyst (Raj)
- **Role:** Security Operations Center (SOC) Analyst
- **Tech Proficiency:** Advanced
- **Pain Points:**
  - Manually investigates reported phishing emails
  - Needs evidence for incident reports
  - Limited time for each investigation
- **Goals:**
  - Automated first-pass analysis of reported emails
  - Structured forensic evidence for documentation
  - Identify campaigns affecting multiple users

#### Persona 3: Senior Citizen (Maria)
- **Role:** Retiree using Gmail for personal correspondence
- **Tech Proficiency:** Basic
- **Pain Points:**
  - Unsure which emails are legitimate
  - Targeted by financial scams
  - Doesn't understand technical jargon
- **Goals:**
  - Simple yes/no guidance on email safety
  - Protection without needing to learn new tools
  - Peace of mind when reading email

### 3.2 Secondary Personas
- **Government staff** handling sensitive communications
- **Students** managing academic and personal email
- **Small business owners** without dedicated IT staff
- **Banking customers** targeted by credential phishing

---

## 4. Core Features & Requirements

### 4.1 Must-Have Features (MVP)

#### F1: Automatic Suspicious Email Detection
**Priority:** P0  
**Description:** Monitor Gmail inbox and identify potentially malicious emails as they are opened

**Acceptance Criteria:**
- Content script activates on all Gmail pages
- Detects email open event via DOM observation
- Extracts sender, subject, and body content
- Runs lightweight heuristic check (< 100ms)
- Triggers investigation for high-risk emails

**Technical Requirements:**
- Manifest V3 content script injection
- MutationObserver for Gmail DOM changes
- Pattern matching for common phishing indicators
- Local storage for user preferences

---

#### F2: Autonomous Header Investigation
**Priority:** P0  
**Description:** Automatically open raw email source and extract headers for analysis

**Acceptance Criteria:**
- Programmatically triggers Gmail's "Show Original" view
- Opens investigation in background tab (non-intrusive)
- Extracts complete header chain
- Parses Received headers in chronological order
- Handles Gmail API fallback if DOM method fails

**Technical Requirements:**
- Chrome tabs API for programmatic tab management
- Gmail DOM selector targeting (with version resilience)
- Gmail API integration (messages.get endpoint)
- Header parsing library (Python email.parser)

---

#### F3: Email Authentication Analysis
**Priority:** P0  
**Description:** Validate SPF, DKIM, and DMARC authentication results

**Acceptance Criteria:**
- Extracts authentication headers from raw email
- Interprets SPF result (pass/fail/softfail/neutral/none)
- Validates DKIM signature authenticity
- Checks DMARC policy and alignment
- Identifies authentication bypass attempts

**Technical Requirements:**
- SPF record DNS lookup and validation
- DKIM public key retrieval and signature verification
- DMARC policy parsing (p=quarantine/reject/none)
- RFC 7489 compliance

**Risk Scoring:**
```
S_auth = w₁·(1 - SPF_pass) + w₂·(1 - DKIM_valid) + w₃·(1 - DMARC_pass)
where w₁=0.3, w₂=0.4, w₃=0.3
```

---

#### F4: IP Geolocation & Origin Trace
**Priority:** P0  
**Description:** Trace email origin through relay chain and geolocate sending infrastructure

**Acceptance Criteria:**
- Parses complete Received header chain
- Identifies earliest reliable sending IP
- Geolocates IP to country/region/city/ISP
- Flags VPN/hosting/proxy infrastructure
- Detects geographic inconsistencies with claimed sender

**Technical Requirements:**
- MaxMind GeoIP2 database integration
- IP reputation database (AbuseIPDB, IPQualityScore)
- ASN lookup for infrastructure typing
- Reverse DNS validation

**Infrastructure Risk Indicators:**
- Tor exit nodes
- VPN endpoints (known providers)
- Bulletproof hosting services
- Cloud hosting (AWS/Azure/GCP) for personal sender
- Geographic mismatch (claimed US company, routed through Eastern Europe)

---

#### F5: Domain Intelligence Check
**Priority:** P0  
**Description:** Analyze sender domain for legitimacy indicators

**Acceptance Criteria:**
- Performs WHOIS lookup on sender domain
- Calculates domain age from creation date
- Checks registrar reputation
- Validates MX records exist and are consistent
- Detects newly registered domains (< 30 days)
- Identifies lookalike/typosquatting domains

**Technical Requirements:**
- WHOIS API integration (WHOIS XML API or similar)
- DNS resolver for MX/TXT/A record lookups
- Levenshtein distance for domain similarity detection
- Database of legitimate corporate domains

**Domain Age Risk Score:**
```
Risk_domain = e^(-d / τ)
where d = domain age in days, τ = 30 days
```

---

#### F6: Evidence Fusion & Threat Scoring
**Priority:** P0  
**Description:** Combine all investigation signals into unified threat assessment

**Acceptance Criteria:**
- Aggregates findings from all analysis agents
- Produces confidence score (0-100%)
- Generates plain-language explanation
- Identifies primary risk factors
- Provides severity level (Critical/High/Medium/Low)

**Technical Requirements:**
- Machine learning meta-classifier (logistic regression baseline)
- Trained on labeled phishing dataset (Enron + PhishTank)
- Feature engineering for heterogeneous signals
- Explainable AI (SHAP values for feature importance)

**Fusion Model:**
```
P(threat | evidence) = σ(w₀ + w₁·S_content + w₂·S_auth + w₃·Risk_domain + w₄·S_geo + w₅·S_link)

where:
- S_content: content-based suspicion score
- S_auth: authentication failure score
- Risk_domain: domain age/reputation risk
- S_geo: geographic inconsistency score
- S_link: malicious URL detection score
- σ: sigmoid activation function
```

**Training Dataset:**
- Legitimate emails: 10,000+ (Enron corpus)
- Phishing emails: 5,000+ (PhishTank verified)
- BEC examples: 500+ (FBI IC3 samples)
- Split: 70% train, 15% validation, 15% test

---

#### F7: In-Gmail Warning Banner
**Priority:** P0  
**Description:** Inject clear, actionable warning into Gmail interface

**Acceptance Criteria:**
- Banner appears at top of email body
- Uses traffic-light color coding (red/yellow/green)
- Displays threat level and primary risk factor
- Shows warning within 3 seconds of investigation start
- Non-blocking (user can still read email)
- Dismissable but persistent across sessions for same email

**Design Requirements:**
- **Critical Threat (Red):**
  ```
  ⚠️ WARNING: This email is likely fraudulent
  • Domain registered 4 days ago
  • Failed authentication checks (DMARC)
  • Routed through high-risk infrastructure in [Country]
  [View Full Evidence] [Report Phishing]
  ```

- **Suspicious (Yellow):**
  ```
  ⚠ CAUTION: This email shows suspicious characteristics
  • Sender domain recently created
  • Some authentication checks failed
  [View Details]
  ```

- **Safe (Green - Optional):**
  ```
  ✓ This email passed security checks
  [View Analysis]
  ```

**Technical Requirements:**
- Shadow DOM injection for style isolation
- Responsive design (mobile/desktop)
- Accessibility compliance (WCAG 2.1 AA)
- Animation for attention without annoyance

---

#### F8: Expandable Evidence View
**Priority:** P0  
**Description:** Detailed forensic report for advanced users and analysts

**Acceptance Criteria:**
- Accessible via "View Full Evidence" link
- Displays complete investigation findings
- Shows relay path visualization
- Includes authentication results with technical details
- Presents WHOIS record and domain history
- Provides IP geolocation map
- Exportable as PDF/JSON for documentation

**Content Sections:**
1. **Executive Summary:** Plain-language threat overview
2. **Authentication Analysis:** SPF/DKIM/DMARC detailed results
3. **Relay Path:** Visual timeline of email journey
4. **Origin Intelligence:** IP geolocation, ISP, infrastructure type
5. **Domain Analysis:** Registration date, registrar, DNS records
6. **Content Analysis:** Suspicious patterns detected
7. **Recommended Actions:** User guidance based on threat level
8. **Raw Evidence:** Exportable JSON of all findings

**Technical Requirements:**
- Modal overlay UI component
- D3.js or similar for relay path visualization
- Leaflet.js for geolocation map
- PDF generation library (jsPDF)
- JSON export functionality

---

### 4.2 Should-Have Features (Post-MVP)

#### F9: Multi-Email Campaign Detection
**Priority:** P1  
**Description:** Correlate flagged emails to identify coordinated phishing campaigns

**Acceptance Criteria:**
- Identifies common patterns across flagged emails
- Groups emails by shared infrastructure/sender
- Alerts when multiple users receive similar threats
- Provides campaign-level statistics

**Technical Requirements:**
- Graph database for relationship modeling (Neo4j)
- Clustering algorithms (DBSCAN for temporal/content similarity)
- Shared backend for cross-user correlation

---

#### F10: Institutional Dashboard
**Priority:** P1  
**Description:** Centralized view for security teams monitoring organizational email threats

**Acceptance Criteria:**
- Real-time threat feed across organization
- Summary statistics (threats detected, users protected)
- Drill-down into individual incidents
- Export bulk reports for compliance
- User activity tracking (who's clicking warnings)

**Technical Requirements:**
- Web dashboard (React + TypeScript)
- Backend API for aggregated data
- Role-based access control (RBAC)
- PostgreSQL for historical data storage

---

#### F11: Threat Intelligence Integration
**Priority:** P1  
**Description:** Cross-reference findings with external threat feeds

**Acceptance Criteria:**
- Checks URLs against PhishTank, OpenPhish databases
- Validates sender IPs against threat intelligence feeds
- Queries VirusTotal for attachment hashes
- Updates local threat database nightly

**Technical Requirements:**
- PhishTank API integration
- OpenPhish feed parsing
- VirusTotal API (rate-limited free tier)
- Local Redis cache for performance

---

#### F12: Visual Brand Impersonation Detection
**Priority:** P2  
**Description:** Detect fake logos and visual phishing attempts in email body

**Acceptance Criteria:**
- Extracts images from email HTML
- Compares against known brand logos
- Uses perceptual hashing for similarity
- Flags impersonation attempts

**Technical Requirements:**
- Image extraction from HTML/base64
- pHash or similar perceptual hashing algorithm
- Database of legitimate brand logos
- CNN-based logo classifier for precision

---

### 4.3 Nice-to-Have Features (Future Roadmap)

#### F13: Multi-Client Support
- Outlook Web App integration
- Yahoo Mail support
- Standalone email client plugins

#### F14: Machine Learning Improvements
- Deep learning for content analysis (BERT-based)
- Behavioral anomaly detection (user-specific baselines)
- Active learning from user feedback

#### F15: Advanced Reporting
- Automated incident reports for security teams
- Chain-of-custody evidence logging
- Integration with SIEM systems (Splunk, ELK)

#### F16: User Education
- In-app security tips based on detected threats
- Phishing awareness training modules
- Gamified security challenges

---

## 5. User Experience Requirements

### 5.1 Installation & Onboarding
1. **Install from Chrome Web Store** (< 30 seconds)
2. **Grant Gmail permissions** (explicit consent screen)
3. **Optional: Connect institutional dashboard** (for enterprise users)
4. **Brief tutorial** (optional, 3 slides showing how warnings appear)

### 5.2 Core User Flows

#### Flow 1: Safe Email (No Warning)
```
User opens email → Extension monitors → No threats detected → No banner shown
```
**Experience:** Completely invisible, zero friction

---

#### Flow 2: Suspicious Email (Warning)
```
User opens email
    ↓
Extension detects suspicious patterns
    ↓
Investigation tab opens briefly in background (subtle indicator)
    ↓
Warning banner appears within 3 seconds
    ↓
User reads plain-language summary
    ↓
[Option A] User closes email (protected)
[Option B] User clicks "View Full Evidence" → Modal opens with forensics
[Option C] User clicks "Report Phishing" → Forwards to security team
```

---

#### Flow 3: Analyst Deep Dive
```
Security analyst receives alert from dashboard
    ↓
Opens email investigation report
    ↓
Reviews relay path, authentication results, domain intel
    ↓
Exports PDF for incident documentation
    ↓
Marks as confirmed phishing or false positive
    ↓
System learns from feedback
```

---

### 5.3 Performance Requirements
- **Background monitoring:** < 10ms overhead per Gmail page load
- **Investigation trigger:** < 500ms from email open to tab creation
- **Analysis completion:** < 3 seconds for complete investigation
- **Banner rendering:** < 100ms from results received
- **Memory footprint:** < 50MB RAM for extension
- **Network usage:** < 100KB per investigation (excluding geolocation database)

### 5.4 Accessibility Requirements
- **WCAG 2.1 AA compliance** for all UI elements
- **Keyboard navigation** for all interactive components
- **Screen reader support** (ARIA labels for warnings)
- **Color-blind safe** palette (not relying solely on red/green)
- **High-contrast mode** support

---

## 6. Technical Requirements

### 6.1 Browser Support
- **Primary:** Chrome 120+ (Manifest V3)
- **Secondary:** Edge 120+ (Chromium-based)
- **Future:** Firefox (Manifest V3 when stable)

### 6.2 Gmail Compatibility
- **Gmail Web UI:** Full support (standard and compact views)
- **Gmail API:** Fallback for reliable header extraction
- **G Suite/Workspace:** Full compatibility
- **Legacy Gmail:** Not supported (< 5% user base)

### 6.3 Backend Infrastructure
- **API Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15+ for persistent data, Redis for caching
- **Hosting:** Cloud-agnostic (AWS/GCP/Azure), containerized (Docker)
- **Scaling:** Horizontal with load balancer (target: 10K concurrent users)

### 6.4 Security Requirements
- **User data:** Never stored on backend (privacy-first design)
- **Headers only:** Backend receives only email headers, not content
- **Encryption:** TLS 1.3 for all network communication
- **API authentication:** JWT tokens for institutional dashboard access
- **Rate limiting:** 100 requests/minute per user to prevent abuse
- **Audit logging:** All investigations logged with timestamps (retention: 90 days)

### 6.5 Data Privacy & Compliance
- **GDPR compliant:** No PII stored without consent
- **User control:** Settings to disable investigation for specific senders/domains
- **Transparency:** Clear privacy policy explaining what data is processed
- **Data minimization:** Only headers needed for analysis are transmitted
- **Right to deletion:** Users can clear all stored preferences on demand

---

## 7. Non-Functional Requirements

### 7.1 Reliability
- **Uptime:** 99.5% for backend API
- **Graceful degradation:** If backend unavailable, fall back to local heuristics
- **Error handling:** Silent failures with option to retry manually
- **Gmail UI changes:** Resilient selectors with fallback strategies

### 7.2 Scalability
- **User base:** Support 100K+ active users
- **Concurrent investigations:** 1000+ simultaneous
- **Database:** Optimized queries with indexing (< 100ms response time)
- **CDN:** Static assets served via CDN for global performance

### 7.3 Maintainability
- **Code quality:** Type-safe (TypeScript for extension, Python type hints for backend)
- **Testing:** 80%+ code coverage (unit + integration tests)
- **Documentation:** API docs (OpenAPI/Swagger), code comments, architecture diagrams
- **Monitoring:** Application performance monitoring (APM) with alerts

### 7.4 Localization (Future)
- **Phase 1:** English only
- **Phase 2:** Hindi, Spanish, French, German, Japanese
- **Considerations:** Technical terms vs. plain language in warnings

---

## 8. Success Metrics & KPIs

### 8.1 Detection Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Precision | ≥ 95% | (True Positives) / (True Positives + False Positives) |
| Recall | ≥ 90% | (True Positives) / (True Positives + False Negatives) |
| F1 Score | ≥ 0.92 | Harmonic mean of precision and recall |
| False Positive Rate | ≤ 5% | (False Positives) / (False Positives + True Negatives) |

### 8.2 User Experience Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to Warning | < 3 seconds | Investigation start to banner display |
| User Satisfaction | ≥ 4.5/5 | Post-interaction survey |
| Warning Click-Through | 20-40% | Users viewing full evidence |
| False Positive Reports | < 2% | User-reported incorrect warnings |

### 8.3 Business Metrics
| Metric | Target (6 months) | Measurement |
|--------|---------|-------------|
| Active Installations | 50,000+ | Chrome Web Store analytics |
| Daily Active Users (DAU) | 10,000+ | Extension telemetry |
| Emails Investigated | 100,000+/day | Backend API logs |
| Threats Blocked | 5,000+/day | High-confidence warnings shown |
| Institutional Customers | 10+ organizations | Dashboard sign-ups |

### 8.4 Technical Performance Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time | < 2 seconds | 95th percentile |
| Extension CPU Usage | < 5% | Chrome Task Manager |
| Investigation Success Rate | ≥ 99% | Completed analyses / triggered investigations |
| Backend Uptime | ≥ 99.5% | Uptime monitoring service |

---

## 9. Risk Assessment & Mitigation

### 9.1 Technical Risks

#### Risk 1: Gmail UI Changes Breaking Extension
**Probability:** Medium | **Impact:** High  
**Mitigation:**
- Use Gmail API as primary method (not dependent on UI)
- Maintain multiple DOM selector strategies
- Automated daily tests against live Gmail
- Alert system for detection failures
- Fast-track updates when Gmail changes

#### Risk 2: Performance Impact on Gmail
**Probability:** Low | **Impact:** High  
**Mitigation:**
- Lazy loading of analysis components
- Debounced event listeners
- Background processing via service worker
- Performance profiling in development
- Memory leak prevention (proper cleanup)

#### Risk 3: False Positives Eroding Trust
**Probability:** Medium | **Impact:** High  
**Mitigation:**
- Conservative initial thresholds (favor false negatives over false positives)
- User feedback loop to improve model
- Severity levels (critical vs. suspicious) to set expectations
- Clear "Report Incorrect Warning" option
- Monthly model retraining with new data

#### Risk 4: Backend Infrastructure Costs
**Probability:** Medium | **Impact:** Medium  
**Mitigation:**
- Client-side caching of investigation results (7 days)
- Rate limiting to prevent abuse
- Tiered service (free tier with daily limits, paid for unlimited)
- Optimize database queries and indexing
- Auto-scaling with cost alerts

---

### 9.2 Privacy & Security Risks

#### Risk 5: User Privacy Concerns
**Probability:** Medium | **Impact:** High  
**Mitigation:**
- Transparent privacy policy (no email content stored)
- Local processing where possible
- Open-source extension code for audit
- Privacy-focused marketing messaging
- GDPR/CCPA compliance from day one

#### Risk 6: Extension Compromised
**Probability:** Low | **Impact:** Critical  
**Mitigation:**
- Code signing for all releases
- Automated security scanning (Snyk, SonarQube)
- Minimal permissions requested
- Regular security audits
- Bug bounty program

#### Risk 7: API Key Exposure
**Probability:** Low | **Impact:** High  
**Mitigation:**
- Never embed API keys in extension code
- Server-side API key management
- Key rotation policy (quarterly)
- Rate limiting per API key
- Monitor for unusual API usage patterns

---

### 9.3 Business Risks

#### Risk 8: Low User Adoption
**Probability:** Medium | **Impact:** High  
**Mitigation:**
- Clear value proposition in onboarding
- Viral social proof (share protection statistics)
- Partnerships with cybersecurity communities
- Media outreach (tech press, security blogs)
- Free for individuals, paid for enterprises

#### Risk 9: Competition from Gmail Native Features
**Probability:** Low | **Impact:** Critical  
**Mitigation:**
- Focus on explainability (Gmail doesn't show evidence)
- Advanced forensics beyond basic spam filtering
- Institutional dashboard as differentiator
- Faster to market with novel features
- Pivot to API service if Gmail absorbs core functionality

#### Risk 10: Legal Liability for Missed Threats
**Probability:** Low | **Impact:** High  
**Mitigation:**
- Clear terms of service (best-effort, not guaranteed protection)
- Disclaimer in warnings ("Exercise caution even with checked emails")
- Professional liability insurance
- Transparent about detection limitations
- Regular accuracy reporting to set realistic expectations

---

## 10. Regulatory & Compliance Requirements

### 10.1 Data Protection
- **GDPR (EU):** Right to access, delete, portability; lawful basis for processing
- **CCPA (California):** Disclosure of data collection, opt-out mechanisms
- **PIPEDA (Canada):** Consent for data collection, secure handling

### 10.2 Accessibility
- **ADA (US):** Accessible to users with disabilities
- **AODA (Ontario):** WCAG 2.0 Level AA compliance
- **EN 301 549 (EU):** European accessibility standard

### 10.3 Security Standards
- **OWASP Top 10:** Protection against common web vulnerabilities
- **CWE/SANS Top 25:** Mitigate most dangerous software weaknesses
- **Chrome Web Store Policies:** Compliance with extension guidelines

---

## 11. Timeline & Milestones

### Phase 1: MVP Development (Weeks 1-8)
| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 1-2 | Core Extension Framework | Manifest V3 setup, Gmail injection, basic monitoring |
| 3-4 | Header Extraction | "Show Original" automation, Gmail API integration |
| 5-6 | Forensic Analysis Agents | SPF/DKIM/DMARC validation, IP geolocation, WHOIS lookup |
| 7 | Evidence Fusion Model | ML classifier training, scoring system |
| 8 | Warning UI | Banner injection, basic evidence view |

**MVP Demo Ready:** Week 8

---

### Phase 2: Polish & Testing (Weeks 9-12)
| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 9 | UI/UX Refinement | Design polish, accessibility testing |
| 10 | Performance Optimization | Caching, lazy loading, profiling |
| 11 | Security Audit | Penetration testing, code review |
| 12 | Beta Testing | 100 user pilot, feedback integration |

**Public Beta Launch:** Week 12

---

### Phase 3: Post-MVP Features (Weeks 13-20)
| Week | Milestone | Deliverables |
|------|-----------|--------------|
| 13-14 | Campaign Detection | Graph database, correlation algorithms |
| 15-16 | Institutional Dashboard | Web app, RBAC, reporting |
| 17-18 | Threat Intel Integration | PhishTank, OpenPhish, VirusTotal APIs |
| 19-20 | Visual Brand Detection | Logo extraction, perceptual hashing |

**Full Feature Release:** Week 20

---

## 12. Dependencies & Assumptions

### 12.1 External Dependencies
- **Gmail API:** Stable and accessible (no breaking changes during development)
- **Geolocation Database:** MaxMind GeoIP2 or similar available
- **WHOIS API:** Reliable service with adequate rate limits
- **PhishTank/OpenPhish:** Threat feeds remain freely accessible
- **Chrome Web Store:** Approval process < 7 days for updates

### 12.2 Assumptions
- Users have Chrome 120+ installed
- Users grant necessary Gmail permissions
- Network connectivity available for backend calls
- Gmail remains primary email client for target users
- Email authentication (SPF/DKIM/DMARC) continues to be standard practice

---

## 13. Open Questions

1. **Monetization Strategy:** Free forever, freemium, or enterprise-only paid tier?
2. **Data Retention:** How long should investigation results be cached locally?
3. **User Feedback Loop:** How to collect ground truth labels without violating privacy?
4. **False Positive Handling:** Should users be able to whitelist senders/domains?
5. **Offline Mode:** What functionality is available without backend connectivity?
6. **Multi-Account Support:** How to handle users with multiple Gmail accounts?
7. **Mobile Support:** Is Gmail mobile app extension architecture feasible?

---

## 14. Appendix

### 14.1 Glossary
- **SPF (Sender Policy Framework):** Email authentication that verifies sender IP authorization
- **DKIM (DomainKeys Identified Mail):** Cryptographic signature validating message integrity
- **DMARC (Domain-based Message Authentication):** Policy framework building on SPF/DKIM
- **BEC (Business Email Compromise):** Targeted phishing attacking business transactions
- **Relay Path:** Sequence of mail servers an email passed through
- **Manifest V3:** Latest Chrome extension platform specification

### 14.2 References
- SIH Problem Statement PS26106: AI-Powered Email Threat Detection
- RFC 7208: Sender Policy Framework (SPF)
- RFC 6376: DomainKeys Identified Mail (DKIM)
- RFC 7489: Domain-based Message Authentication (DMARC)
- OWASP Email Security Cheat Sheet
- Google Chrome Extension Best Practices

---

**Document Control:**  
- **Author:** ClickWise Development Team  
- **Reviewers:** Security Team, UX Team, Engineering Leads  
- **Next Review Date:** September 27, 2026  
- **Change History:** Version 1.0 - Initial Release
