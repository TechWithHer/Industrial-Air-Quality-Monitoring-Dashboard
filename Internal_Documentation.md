Section 3 — Industrial Air Quality Analytics Dashboard
WHY THIS PROJECT (replaces Oil Price)
This project is stronger than the oil price version for Singapore-targeted roles. It maps to themes Singapore employers care about: environmental data, government open data, regional health/sustainability, time-series analytics. Singapore's NEA open data API for PSI/PM2.5 means you're working with locally relevant, real data — recruiters at GovTech and sustainability-tech firms recognise this instantly.
Project Quick Facts
Time required	1 week focused (7 days) or 2 weeks part-time
AWS cost	~SGD 1–3 per month (well within free tier for personal use)
Difficulty	Easy–Medium
Priority	MEDIUM-HIGH — strongest serverless showcase
Pairs with	Terraform Associate; AWS SAA-C03 (serverless patterns)
Data Sources (all free)
Primary: data.gov.sg API
•	Singapore NEA real-time PSI: https://api.data.gov.sg/v1/environment/psi
•	Singapore NEA PM2.5: https://api.data.gov.sg/v1/environment/pm25
•	Air temperature: https://api.data.gov.sg/v1/environment/air-temperature
•	No API key required, no rate limits for reasonable use, updates hourly
Secondary: OpenAQ (for regional comparison)
•	Global open-source air quality API; no key for basic use
•	Endpoint: https://api.openaq.org/v2/measurements
•	Covers Jakarta, KL, Manila — enables multi-country haze-season comparison narrative
Optional Tertiary
•	WAQI (aqicn.org): free tier with API key, 1000 req/min, 130+ countries
•	IQAir AirVisual: free tier with key, 10,000 calls/month
Tech Stack — Exact Components
Ingestion Layer
•	AWS EventBridge — schedule rules every 15 minutes (data.gov.sg updates hourly; OpenAQ varies)
•	AWS Lambda (Python) — two ingestion functions, one per data source, each with retry + DLQ
•	AWS SQS (Dead Letter Queue) — captures failed ingestion events for inspection
•	AWS Secrets Manager — store WAQI/IQAir API keys if added; data.gov.sg + OpenAQ need none (positive talking point)
Storage Layer
•	S3 raw bucket — JSON in raw/ prefix partitioned by year=/month=/day=/hour=
•	S3 processed bucket — transformed Parquet in processed/ (Athena queries faster + cheaper)
•	AWS Glue Crawler — auto-discover schema (optional but resume-worthy)
•	S3 Lifecycle Policy — transition raw data to Glacier after 90 days, delete after 1 year
Query Layer
•	Athena with partition projection (no Glue Crawler runs needed — cheaper)
•	Saved queries for: PM2.5 trend over 7 days, AQI by region, haze event detection, 24-hour rolling average
Visualization Layer
•	Chart.js dashboard (lightweight) — or upgrade to Grafana with Athena data source plugin
•	CloudFront + S3 for static hosting with global CDN + HTTPS
CI/CD + Security
•	GitHub Actions pipeline with DevSecOps gates
•	Trivy + Checkov for container and IaC scanning
•	Terraform for the entire infrastructure (showcase your June 12 cert)
Observability
•	CloudWatch Alarms on Lambda errors, duration, DLQ depth
•	X-Ray distributed tracing end-to-end (set sampling 10% to control cost)
•	CloudWatch Dashboard showing pipeline health metrics
•	SNS topic for email/Slack alerts on alarms
Interesting Engineering Challenges (become interview stories)
1. Schema Drift Handling
OpenAQ occasionally changes their JSON structure. Build a transformation Lambda that validates against a JSON schema and routes malformed records to a quarantine S3 prefix.
Interview story: "How did you handle upstream schema changes?"
2. Late-Arriving Data
Some sensor stations report 2–3 hours late. Implement a backfill Lambda that re-processes the last 24 hours of data nightly to capture late arrivals.
Interview story: "How did you handle data quality and completeness?"
3. Multi-Region Comparison
Build the dashboard to compare Singapore PSI vs Jakarta + KL + Manila PM2.5. Critical detail: the indices use different scales — normalise them before plotting.
Interview story: "How did you reconcile different data formats across sources?"
4. Haze Event Detection
Add a simple anomaly detection Lambda — if Singapore PSI > 100 for 6 consecutive hours, trigger an SNS alert. This turns a passive dashboard into an active monitoring system.
Interview story: "How did you build event-driven alerting on top of streaming data?"
5. Cost Optimisation Narrative
Document your use of S3 Intelligent-Tiering, Parquet + Snappy compression, Athena partition projection, and Lambda right-sizing. Track and document the cost savings.
Interview story: "Walk me through how you optimised cloud costs on this project."
Build Sequence (7-day focused plan)
•	Day 1–2: Terraform skeleton, S3 buckets with proper structure, data.gov.sg ingestion Lambda + EventBridge schedule. Confirm data flowing into S3.
•	Day 3: Add OpenAQ ingestion Lambda. Build transformation Lambda (JSON → Parquet) with schema validation and quarantine routing.
•	Day 4: Configure Athena with partition projection. Write 3–5 saved queries. Set up Glue Catalog manually (skip crawler unless needed).
•	Day 5: Build Chart.js dashboard, host on S3 + CloudFront. Add GitHub Actions CI/CD pipeline with security gates.
•	Day 6: Observability — CloudWatch dashboard, alarms, SNS, DLQ. Add X-Ray tracing.
•	Day 7: Haze anomaly detection Lambda. Write README with architecture diagram. Record 2-minute Loom demo.
"Wow" Additions (if you have an extra weekend)
•	Forecasting endpoint: a tiny Lambda using Amazon Forecast or statsmodels ARIMA to project PM2.5 24 hours ahead. Transforms "dashboard" into "analytics platform."
•	SES email digests: daily 8 AM SGT summary email for subscribed users. Adds SES + DynamoDB (user subscriptions) — tells a fuller end-to-end story.
CV Claim
CV CLAIM (copy-paste ready)
Serverless Air Quality Analytics Platform — Regional Environmental Monitoring
Designed an event-driven serverless data pipeline on AWS ingesting from data.gov.sg (NEA PSI/PM2.5) and OpenAQ — EventBridge-scheduled Lambdas write raw JSON to partitioned S3, a transformation Lambda converts to compressed Parquet with schema validation and quarantine routing for malformed records, Athena enables ad-hoc SQL with partition projection, and a Chart.js dashboard on CloudFront delivers near real-time multi-country comparison. Implemented anomaly detection for haze events (sustained PSI > 100) with SNS alerting, X-Ray distributed tracing, SQS DLQ + CloudWatch alarms, and a hardened GitHub Actions pipeline with Trivy + Checkov security gates. Entire infrastructure provisioned via Terraform.
Tech: AWS (Lambda, EventBridge, S3, Athena, CloudFront, SNS, X-Ray, CloudWatch, SQS), Terraform, GitHub Actions, Python, Chart.js, Trivy, Checkov
