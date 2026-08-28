# ClickWise
### The Browser Extension That Investigates Your Email Before You Click

**One-line pitch:** ClickWise watches over your inbox — when a suspicious email opens, it autonomously opens its own investigation tab, traces the email back to its real source, and warns you with plain-language evidence, right inside Gmail.

**Aligned to:** SIH PS26106 — AI-Powered Email Threat Detection, GeoLocation and Forensic Intelligence Platform
**Theme:** Blockchain & Cybersecurity
**Category:** Software Edition

---

## 1. The Problem

Email remains the top attack vector for phishing, business email compromise, and credential theft across government, banking, and enterprise systems. Attackers spoof domains, fake display names, and manipulate relay chains to make fraudulent emails look legitimate.

The technical evidence of fraud is almost always sitting right there in the email's hidden headers — but no ordinary user, and few institutional staff, ever look at it. Digging through raw headers, checking SPF/DKIM/DMARC results, and tracing an IP's origin currently requires manual, expert-level effort. Existing spam filters give a yes/no verdict with no investigation and no evidence trail; dedicated forensic tools exist, but they're separate from where people actually read email, so nobody opens them in the moment that matters.

**ClickWise closes that gap by bringing the investigation directly into the inbox, automatically, the moment a suspicious email is opened.**

---

## 2. Who This Protects

**Everyday Gmail users (students, staff, families)** — get a plain-language warning with real evidence, not a cryptic spam-folder decision made silently on their behalf.

**Institutional IT / cybersecurity teams** — get the same investigation at scale across an organization's inbox traffic, with structured evidence instead of manual header-reading.

**First-time digital users and less tech-confident people** — the extension does the technical work invisibly; the person just sees a clear warning banner, not a wall of headers they wouldn't understand anyway.

---

## 3. SDG Alignment

| SDG | Contribution |
|---|---|
| **SDG 9 — Industry, Innovation & Infrastructure** | Browser-native agentic forensic tooling — a novel application of autonomous agents to a widely-used communication channel. |
| **SDG 16 — Peace, Justice & Strong Institutions** | Supports investigation and evidence-gathering for cybercrime, aligned directly with the PS's law-enforcement support goal. |
| **SDG 10 — Reduced Inequalities** | Puts analyst-grade investigation capability into a free browser extension — anyone gets the same protection a trained security analyst would provide. |
| **SDG 1 — No Poverty** | Faster, earlier warning reduces successful financial fraud before money changes hands. |

---

## 4. The Core Novel Feature: Autonomous In-Browser Investigation

### 4.1 What makes ClickWise different

Every existing email-security tool works **before** the email reaches the inbox (spam filtering) or **outside** the inbox entirely (a separate forensics dashboard analysts have to remember to open). ClickWise works at the exact moment of risk — **when the user opens the email** — and does something no current tool does: it **opens its own second tab, autonomously, to go investigate**, then reports back into the first tab. The user watches the investigation happen in real time instead of receiving a silent verdict.

### 4.2 The loop: Watch → Trigger → Investigate → Fuse → Warn

```
   User opens an email in Gmail
              │
              ▼
   ┌───────────────────────┐
   │  CONTENT WATCHER       │  Runs inside the Gmail tab, detects an email
   │  (Chrome Extension)    │  was opened, reads sender/subject/body
   └───────────┬────────────┘
               │ looks suspicious (heuristic + quick ML pass)?
               ▼
   ┌───────────────────────┐
   │  INVESTIGATION TRIGGER │  Extension programmatically opens Gmail's
   │                        │  "Show Original" raw-header view in a new tab
   └───────────┬────────────┘  (or pulls raw headers via Gmail API directly)
               ▼
   ┌───────────────────────┐
   │  HEADER FORENSICS AGENT│  Parses Received chain, validates SPF/DKIM/DMARC,
   │                        │  detects forged sender fields
   └───────────┬────────────┘
               ▼
   ┌───────────────────────┐
   │  ORIGIN TRACE AGENT    │  Extracts earliest reliable sending IP,
   │                        │  geolocates it, flags VPN/hosting/proxy infra
   └───────────┬────────────┘
               ▼
   ┌───────────────────────┐
   │  DOMAIN INTEL AGENT    │  WHOIS + DNS/MX lookup, domain-age risk score
   └───────────┬────────────┘
               ▼
   ┌───────────────────────┐
   │  EVIDENCE FUSION       │  Combines all signals into one confidence-scored,
   │                        │  explainable verdict
   └───────────┬────────────┘
               ▼
   ┌───────────────────────┐
   │  BANNER INJECTOR       │  Injects a plain-language warning banner back
   │                        │  into the ORIGINAL Gmail tab — closes the loop
   └────────────────────────┘
```

### 4.3 What the user actually sees

1. Opens an email.
2. A small tab briefly opens in the background — a subtle "investigating…" indicator appears in Gmail (not a jarring popup).
3. Within seconds, a banner appears at the top of the email itself:

> ⚠️ **This email may not be from who it claims.** Sender domain was registered 6 days ago. Authentication check failed (DMARC). Message was routed through a server in [Region], inconsistent with the claimed sender. **[View full evidence]**

4. Clicking "View full evidence" expands the actual forensic detail — relay path, IP trace map, WHOIS record — for anyone who wants to dig deeper (or for an institutional analyst who needs it for a report).

This is the demo moment: judges watch the agent *actually go investigate*, live, instead of being told about a backend process they can't see.

---

## 5. Extension Architecture

### 5.1 Components

| Component | Responsibility |
|---|---|
| **`manifest.json` (Manifest V3)** | Declares permissions (`tabs`, `scripting`, `storage`), content-script injection rules for `mail.google.com` |
| **Content script — Gmail Watcher** | Runs on `mail.google.com`; detects opened emails via DOM observation, extracts visible sender/subject/body |
| **Content script — Header Scraper** | Runs on the "Show Original" raw-source tab (or calls Gmail API directly); extracts headers |
| **Background service worker** | Orchestrates the flow — receives watcher events, opens/manages the investigation tab, calls the backend API, relays the verdict back |
| **Backend API (FastAPI)** | Hosts the Header Forensics, Origin Trace, Domain Intel agents and the evidence-fusion model; does the lookups the browser can't (CORS-restricted geolocation/WHOIS calls) |
| **Content script — Banner Injector** | Injects the warning banner UI back into the original Gmail tab once a verdict is ready |

### 5.2 Why a backend is required (not everything can run client-side)

Browsers block many cross-origin lookups (WHOIS, IP geolocation databases, some DNS queries) directly from a content script. ClickWise's extension therefore does the *watching and reading* client-side, but ships the raw extracted evidence to a backend for the actual forensic analysis — mirroring the same "agent-as-brain, tool-as-hands" pattern from your earlier browser-automation projects, just split across the extension/backend boundary instead of within one script.

### 5.3 Reliability note (learned from the government-portal automation discussion)

Automating Gmail's UI directly (clicking through to "Show Original") is great for the demo, but fragile if Gmail changes its interface. The more robust path — worth building toward even if the UI-automation version is what's demoed live — is calling the **Gmail API's `messages.get`** endpoint directly for raw headers, which doesn't depend on Gmail's visual layout at all. Plan to demo the UI-automation version (it's visually compelling) while noting the API-based version as the production-grade approach.

---

## 6. Agent Details

| Agent | Input | Output | Technique |
|---|---|---|---|
| **Content Watcher** | DOM of open Gmail message | Sender, subject, body text, "worth investigating?" flag | DOM observation + lightweight heuristic/NLP pass |
| **Header Forensics Agent** | Raw email headers | SPF/DKIM/DMARC pass/fail, relay-path anomalies, forged-field flags | Header parsing + protocol validation rules |
| **Origin Trace Agent** | Extracted relay IP chain | Earliest reliable IP, geolocation (country/region/ISP), VPN/hosting flag | IP geolocation lookup + infrastructure-type heuristics |
| **Domain Intelligence Agent** | Claimed sender domain | Domain age, registrar, DNS/MX record consistency | WHOIS + DNS lookups |
| **Evidence Fusion Reasoner** | All agent outputs | Single confidence-scored, explainable verdict | Stacked meta-classifier (logistic regression over agent signals) |
| **Banner Injector** | Final verdict | Warning banner UI in Gmail | DOM injection content script |

---

## 7. The Math Underneath

### 7.1 Authentication signal scoring

  S_auth = w₁·(1 − SPF_pass) + w₂·(1 − DKIM_valid) + w₃·(1 − DMARC_pass)

### 7.2 Domain-age risk (newly registered domains are disproportionately used in fraud)

  Risk_domain = e^(−d / τ)

where *d* = domain age in days, *τ* = tunable decay constant.

### 7.3 Evidence fusion

  P(fraudulent | evidence) = σ( w₀ + w₁·S_content + w₂·S_auth + w₃·Risk_domain + w₄·S_geo_mismatch )

where σ is the sigmoid function and weights are learned on a labeled training set rather than hand-picked — giving a defensible answer if judges ask "why do you trust this score."

---

## 8. Features List

**Core:**
- Automatic detection of a suspicious email on open (no user action required)
- Autonomous "investigation tab" — the agent opens and reads the raw header source itself
- Header/authentication forensics (SPF/DKIM/DMARC)
- IP geolocation and hosting/VPN detection
- Domain age and registration-intelligence check
- In-Gmail warning banner with plain-language explanation
- Expandable "full evidence" view (relay path, trace map, WHOIS record) for advanced users/analysts

**Upgrades (build if time allows):**
- Graph-based correlation across multiple flagged emails to detect campaign-level fraud
- Institutional dashboard aggregating flagged emails across an organization
- Threat-intel feed cross-referencing (PhishTank, OpenPhish) where rate limits allow
- Visual/logo similarity check for embedded brand impersonation in email body
- Exportable forensic report (PDF) for institutional or investigative handoff

**Explicitly out of scope for the hackathon:**
- Full dark-web/threat-actor attribution
- Automated law-enforcement reporting integrations
- Support for email clients beyond Gmail (Outlook, etc.) — mention as roadmap only

---

## 9. Human-in-the-Loop Safety

| Autonomy Level | Examples |
|---|---|
| **Automatic** | Opening the investigation tab, parsing headers, running lookups, displaying the warning banner |
| **Requires user action** | Clicking "View full evidence" to expand technical detail, marking an email as reviewed |
| **Never done autonomously** | Deleting/moving the email, blocking the sender, taking any account-level action |

---

## 10. Build Roadmap

**Core build (demoed live):**
1. Chrome extension: Gmail content watcher + investigation-tab trigger + banner injector
2. Backend: header parser, SPF/DKIM/DMARC validator, IP geolocation lookup, WHOIS/domain-age check
3. Evidence fusion model, trained on a labeled phishing-email dataset
4. One flagship demo: a realistic spoofed-domain BEC email, opened live, investigated live, banner appears live

**Upgrades if time allows:** correlation graph across flagged emails → institutional dashboard → PDF report export → visual/logo check

---

## 11. Success Metrics

**Detection:** precision, recall, false-positive rate on phishing/spoofing classification.

**Investigation accuracy:** correct SPF/DKIM/DMARC interpretation, correct geolocation of originating IP, correct domain-age risk flagging.

**User impact:** time from opening a suspicious email to seeing an evidence-backed warning; clarity of the banner to a non-technical user.

**Reliability:** investigation-tab trigger success rate (does it consistently manage to extract headers without manual steps).

---

## 12. Problem Statement Alignment

> Develop a browser-integrated AI agent that autonomously investigates a suspicious email at the moment it is opened — analyzing headers, authentication results, and relay path; tracing its probable origin using IP geolocation and domain intelligence; and presenting a confidence-scored, explainable warning directly within the user's inbox, with an expandable forensic evidence view to support institutional or investigative review.
