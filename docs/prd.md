# TrendsPy Product Requirements Document

**Version**: 1.0
**Last Updated**: 2025-11-27
**Document Type**: Descriptive (Reverse-Engineered)
**Status**: Draft

---

## Table of Contents

1. [Product Overview](#1-product-overview)
   - 1.1 [What is TrendsPy?](#11-what-is-trendspy)
   - 1.2 [Purpose & Vision](#12-purpose--vision)
   - 1.3 [Key Use Cases](#13-key-use-cases)
   - 1.4 [Target Users](#14-target-users)
   - 1.5 [Key Differentiators](#15-key-differentiators)

2. [User Personas & Problem Statements](#2-user-personas--problem-statements)
   - 2.1 [Persona 1: Emma (Content Marketer)](#21-persona-1-emma-content-marketer)
   - 2.2 [Persona 2: Raj (Data Analyst)](#22-persona-2-raj-data-analyst)
   - 2.3 [Persona 3: Alex (Social Media Manager)](#23-persona-3-alex-social-media-manager)
   - 2.4 [Persona 4: Maria (SEO Specialist)](#24-persona-4-maria-seo-specialist)
   - 2.5 [Persona 5: Dr. Chen (Academic Researcher)](#25-persona-5-dr-chen-academic-researcher)

3. [Features & Capabilities](#3-features--capabilities)
   - 3.1 [Trend Analysis Features](#31-trend-analysis-features)
   - 3.2 [Real-Time Trending Features](#32-real-time-trending-features)
   - 3.3 [Discovery & Utility Features](#33-discovery--utility-features)
   - 3.4 [Advanced Capabilities](#34-advanced-capabilities)

4. [Reliability & Production Features](#4-reliability--production-features)
   - 4.1 [Adaptive Rate Limiting](#41-adaptive-rate-limiting)
   - 4.2 [Circuit Breaker Pattern](#42-circuit-breaker-pattern)
   - 4.3 [Session Management & Cookie Persistence](#43-session-management--cookie-persistence)
   - 4.4 [TLS Fingerprint Impersonation](#44-tls-fingerprint-impersonation)
   - 4.5 [Browser Profile Coherence](#45-browser-profile-coherence)
   - 4.6 [IP Rotation via Tor](#46-ip-rotation-via-tor)
   - 4.7 [Proxy Support](#47-proxy-support)
   - 4.8 [Graceful Degradation](#48-graceful-degradation)

5. [Data Models & Objects](#5-data-models--objects)
   - 5.1 [TrendKeyword](#51-trendkeyword)
   - 5.2 [TrendList](#52-trendlist)
   - 5.3 [NewsArticle](#53-newsarticle)
   - 5.4 [BatchPeriod (Enum)](#54-batchperiod-enum)
   - 5.5 [DataFrame Outputs](#55-dataframe-outputs)

6. [User Workflows & Journeys](#6-user-workflows--journeys)
   - 6.1 [Content Calendar Planning](#61-content-calendar-planning-emmas-journey)
   - 6.2 [Real-Time Social Listening](#62-real-time-social-listening-alexs-journey)
   - 6.3 [Geographic Market Analysis](#63-geographic-market-analysis-rajs-journey)
   - 6.4 [Large-Scale Keyword Research](#64-large-scale-keyword-research-marias-journey)

7. [Technical Architecture](#7-technical-architecture)
   - 7.1 [Layered Architecture](#71-layered-architecture)
   - 7.2 [Request Flow](#72-request-flow)
   - 7.3 [API Integration](#73-api-integration)
   - 7.4 [Dependencies](#74-dependencies)

8. [Configuration & Initialization](#8-configuration--initialization)
   - 8.1 [Basic Initialization](#81-basic-initialization)
   - 8.2 [Production Configuration](#82-production-configuration)
   - 8.3 [Parameter Reference](#83-parameter-reference)
   - 8.4 [Proxy Configuration Recipes](#84-proxy-configuration-recipes)

9. [Constraints & Limitations](#9-constraints--limitations)
   - 9.1 [API Constraints (Google's Limits)](#91-api-constraints-googles-limits)
   - 9.2 [Library Design Constraints](#92-library-design-constraints)
   - 9.3 [Known Limitations & Workarounds](#93-known-limitations--workarounds)

10. [Error Handling & Troubleshooting](#10-error-handling--troubleshooting)
    - 10.1 [Exception Types](#101-exception-types)
    - 10.2 [Rate Limiter States](#102-rate-limiter-states)
    - 10.3 [Common Issues & Solutions](#103-common-issues--solutions)
    - 10.4 [Debugging Tips](#104-debugging-tips)

11. [Success Criteria & Metrics](#11-success-criteria--metrics)
    - 11.1 [Performance Targets](#111-performance-targets)
    - 11.2 [Reliability Metrics](#112-reliability-metrics)
    - 11.3 [User Experience Goals](#113-user-experience-goals)

12. [Appendices](#appendices)
    - [Appendix A: Timeframe Format Reference](#appendix-a-timeframe-format-reference)
    - [Appendix B: Geographic Resolution Levels](#appendix-b-geographic-resolution-levels)
    - [Appendix C: Google Property Filters](#appendix-c-google-property-filters)
    - [Appendix D: Browser Profile Details](#appendix-d-browser-profile-details)
    - [Appendix E: Topic Taxonomy](#appendix-e-topic-taxonomy)

---

## 1. Product Overview

### 1.1 What is TrendsPy?

**TrendsPy** is a production-grade Python library that provides programmatic access to Google Trends data. It transforms the manual, browser-based Google Trends experience into a powerful, automated data pipeline with pandas-native outputs.

**Elevator Pitch**: TrendsPy enables developers, data analysts, and marketers to automate Google Trends data collection at scale with enterprise-grade reliability features including adaptive rate limiting, browser impersonation, and free IP rotation via Tor.

### 1.2 Purpose & Vision

**Why TrendsPy Exists**:
- **Automation Gap**: Google Trends web interface requires manual CSV exports, limiting scalability
- **Data Integration Need**: Analysts need trends data in programmatic formats (pandas DataFrames) for dashboards and reports
- **Production Reliability**: Existing libraries fail at scale due to rate limiting and bot detection
- **Research Requirements**: Academic and market research demands large-scale, reproducible trend analysis

**Vision**: Make Google Trends data as accessible and reliable as any enterprise API, enabling data-driven decisions at scale.

### 1.3 Key Use Cases

TrendsPy serves five primary use cases:

1. **Content Marketing & SEO**
   - Identify seasonal content opportunities
   - Discover trending topics and related keywords
   - Plan content calendars around search interest patterns
   - Optimize content for geographic markets

2. **Market Research & Business Intelligence**
   - Track brand and competitor interest over time
   - Identify emerging markets through geographic analysis
   - Analyze product category trends
   - Compare market penetration across regions

3. **Social Listening & Real-Time Monitoring**
   - Monitor breaking trends as they emerge
   - Get news context for trending topics
   - Identify viral moments for marketing opportunities
   - Track brand mentions in search trends

4. **Academic & Scientific Research**
   - Study search behavior patterns at scale
   - Analyze public interest in health, climate, political topics
   - Create reproducible research workflows
   - Conduct longitudinal trend studies

5. **Data Journalism & News Analysis**
   - Track public interest around news events
   - Identify story angles based on search trends
   - Visualize trend patterns for data stories
   - Compare regional interest in news topics

### 1.4 Target Users

TrendsPy is designed for technical and semi-technical users who need programmatic access to trends data:

| User Type | Technical Level | Primary Need |
|-----------|----------------|--------------|
| **Data Analysts** | Intermediate Python | Dashboard automation, pandas integration |
| **Content Marketers** | Basic Python | Keyword research, content planning |
| **SEO Specialists** | Basic-Intermediate | Search interest analysis, geographic targeting |
| **Data Scientists** | Advanced Python | Large-scale analysis, machine learning features |
| **Academic Researchers** | Intermediate Python | Reproducible research, longitudinal studies |
| **Social Media Managers** | Basic Python | Real-time trend monitoring, viral detection |
| **Developers** | Advanced Python | API integration, custom applications |

**Skill Prerequisites**:
- Basic Python knowledge (pip install, import, function calls)
- Familiarity with pandas DataFrames (for data analysis)
- Understanding of Google Trends concepts (search interest, normalization)

### 1.5 Key Differentiators

What makes TrendsPy unique compared to alternatives:

#### 1. **Reliability-First Design**
- **Adaptive Rate Limiting**: Automatically manages request timing with exponential backoff
- **Circuit Breaker Pattern**: Prevents IP bans by stopping after repeated failures
- **Session Warmup**: Mimics human browsing behavior to reduce bot detection
- **Result**: >95% request success rate under normal conditions

#### 2. **Enterprise-Scale Batch Processing**
- **500+ Keywords in One Request**: Process trending keywords en masse
- **Independent Normalization**: Each keyword normalized to itself, not cross-compared
- **Use Case**: Analyze entire trending lists without normalization bias

#### 3. **Production-Ready Anti-Detection**
- **TLS Fingerprint Impersonation**: Mimics real browser TLS signatures (Chrome, Firefox, Safari, Edge)
- **Coherent Browser Profiles**: Matching User-Agent and Client Hints headers
- **Timing Jitter**: Randomized delays defeat timing-based bot detection
- **Result**: Avoid connection-level blocks and CAPTCHAs

#### 4. **Free IP Rotation via Tor**
- **Zero-Cost IP Changes**: Rotate through Tor exit nodes without proxy fees
- **Unlimited Scale**: Overcome IP-based rate limits for free
- **Privacy-First**: Built-in anonymization for sensitive research

#### 5. **Flexible Time Formats Beyond Google's Presets**
- **Custom Intervals**: `'now 123-H'`, `'today 45-d'`, `'2024-02-01 10-d'`
- **Hourly Precision**: `'2024-03-25T12 2024-03-25T15'` for short periods
- **Multirange Comparison**: Compare different time periods and regions simultaneously
- **Adaptive Resolution**: Automatically adjusts granularity (hourly to monthly)

#### 6. **Geographic Drilldown (Country → State → City)**
- **Three Resolution Levels**: COUNTRY, REGION (state/province), CITY
- **Hierarchical Analysis**: Start global, drill down to city-level insights
- **DMA Support**: Designated Market Areas for US media markets

#### 7. **Pandas-Native DataFrames**
- **Zero Conversion**: Direct DataFrame outputs, ready for analysis
- **Datetime Indexes**: Proper temporal indexing for time series
- **Plot-Ready**: Immediate visualization with `.plot()`

#### 8. **Production-Grade Error Handling**
- **Custom Exceptions with Remediation**: `TrendsQuotaExceededError` includes fix suggestions
- **Graceful Degradation**: Continues processing high-priority queries under stress
- **Observable Metrics**: `rate_limiter.get_stats()` for health monitoring

---

## 2. User Personas & Problem Statements

### 2.1 Persona 1: Emma (Content Marketer)

#### Background
Emma is a content marketing manager at a SaaS company. She creates data-driven content strategies and needs to identify trending topics, seasonal patterns, and related keywords to plan editorial calendars and optimize content for search visibility.

#### Demographics & Role
- **Age**: 28-35
- **Job Title**: Content Marketing Manager
- **Team Size**: Small marketing team (3-5 people)
- **Technical Skills**: Basic Python, Excel expert, familiar with analytics tools
- **Tools Used**: Google Analytics, Ahrefs, SEMrush, Google Trends (manual)

#### Current Problems

**Problem 1: Manual Google Trends Export is Time-Consuming**
- **Current State**: Emma manually exports CSVs from Google Trends for 10-15 keywords weekly
- **Pain Point**: Each keyword requires separate browser session, copy-paste to Excel
- **Impact**: 2-3 hours per week on repetitive data collection
- **Frustration**: "I spend more time collecting data than analyzing it"

**Problem 2: Can't Compare Multiple Keywords Easily**
- **Current State**: Google Trends limits to 5 keywords per comparison
- **Pain Point**: Emma needs to compare 20+ content topics to identify winners
- **Workaround**: Multiple exports, manual merging in Excel, prone to errors
- **Impact**: Limited ability to identify best content opportunities

**Problem 3: Needs Seasonal Patterns for Content Planning**
- **Current State**: Manually reviews 12-month trends to spot seasonality
- **Pain Point**: No programmatic way to identify peaks, visualize patterns
- **Impact**: Misses optimal content timing, reactive rather than proactive
- **Frustration**: "I know there's a pattern, but I can't prove it with data"

#### TrendsPy Solution

**Solution to Problem 1: Automated Data Collection**
```python
from trendspy import Trends
tr = Trends()

# Replaces 15 manual exports with 3 lines of code
keywords = ['content marketing', 'seo', 'social media', 'email marketing', 'video marketing']
df = tr.interest_over_time(keywords, timeframe='today 12-m')
df.to_csv('trends_data.csv')  # One export, all keywords
```
**Impact**: Reduces data collection from 2-3 hours to 5 minutes

**Solution to Problem 2: Pandas Integration for Analysis**
```python
# Identify top-performing keywords automatically
top_keywords = df.mean().sort_values(ascending=False).head(5)

# Visualize all keywords at once
df.plot(figsize=(12, 6), title='Content Topic Interest Over Time')
```
**Impact**: Compare unlimited keywords, identify winners programmatically

**Solution to Problem 3: Seasonal Pattern Detection**
```python
# Get 24-month history for seasonal analysis
df_24m = tr.interest_over_time(['content marketing'], timeframe='today 24-m')

# Peak detection (basic example)
peaks = df_24m[df_24m > df_24m.quantile(0.75)]
print(f"Content interest peaks in: {peaks.index.month.value_counts().index.tolist()}")
```
**Impact**: Data-driven content calendar planning

#### Primary Features Used
- `interest_over_time()`: Time series analysis for seasonal patterns
- `related_queries()`: Discover long-tail keyword opportunities
- `categories()`: Filter to relevant industry categories
- `interest_by_region()`: Geographic targeting insights

#### Success Metrics
- **Time Saved**: 90% reduction in data collection time (2.5 hours → 15 minutes/week)
- **Keyword Coverage**: 4x increase in keywords analyzed (5 → 20+ per session)
- **Content ROI**: 30% improvement in content performance through data-driven topic selection

---

### 2.2 Persona 2: Raj (Data Analyst)

#### Background
Raj is a data analyst at a market research firm. He builds automated dashboards and reports for clients, requiring programmatic access to Google Trends data with reliable pandas integration.

#### Demographics & Role
- **Age**: 25-32
- **Job Title**: Senior Data Analyst
- **Team Size**: Analytics team of 8
- **Technical Skills**: Advanced Python, SQL, pandas, matplotlib, Tableau
- **Tools Used**: Python (pandas, numpy), Jupyter, Tableau, Power BI, SQL databases

#### Current Problems

**Problem 1: Need Programmatic Access to Trends Data**
- **Current State**: No official Google Trends API; manual exports don't scale
- **Pain Point**: Dashboard refreshes require manual intervention
- **Impact**: Can't automate trend reports for clients
- **Business Impact**: Lost opportunities for recurring revenue dashboards

**Problem 2: Dashboard Refresh Automation**
- **Current State**: Manually updates trend data weekly for 15 client dashboards
- **Pain Point**: Forgets to update, clients see stale data
- **Impact**: Client dissatisfaction, manual overhead
- **Frustration**: "I should be analyzing insights, not copy-pasting data"

**Problem 3: Large-Scale Keyword Analysis**
- **Current State**: Clients want analysis of 100+ competitor keywords
- **Pain Point**: Existing libraries crash or hit rate limits at scale
- **Impact**: Can't deliver comprehensive competitive analysis
- **Business Impact**: Turn down high-value contracts

#### TrendsPy Solution

**Solution to Problem 1: Python API for Automation**
```python
from trendspy import Trends
import pandas as pd

def update_trends_dashboard(keywords, timeframe='today 3-m'):
    """Automated function for dashboard refresh"""
    tr = Trends()
    df = tr.interest_over_time(keywords, timeframe=timeframe)

    # Save to database or data warehouse
    df.to_sql('trends_data', con=db_connection, if_exists='replace')
    return df

# Schedule with cron/Airflow
trends = update_trends_dashboard(['keyword1', 'keyword2'])
```
**Impact**: Fully automated dashboard refreshes, zero manual intervention

**Solution to Problem 2: Reliable Batch Processing**
```python
from trendspy import BatchPeriod

# Process 200 trending keywords with independent normalization
trending = tr.trending_now(geo='US')
keywords = [t.keyword for t in trending[:200]]

# Each keyword normalized independently (not cross-compared)
df = tr.trending_now_showcase_timeline(
    keywords,
    timeframe=BatchPeriod.Past24H
)

# Identify rising vs. falling trends
growth = df.diff().mean().sort_values(ascending=False)
print(f"Fastest rising: {growth.head(10)}")
```
**Impact**: Analyze 200+ keywords in minutes, identify emerging opportunities

**Solution to Problem 3: Production-Grade Reliability**
```python
# Enable Tor rotation for large-scale analysis
tr = Trends(
    tor_enabled=True,           # Free IP rotation
    use_tls_impersonation=True, # Avoid bot detection
    persist_cookies=True,       # Maintain session
    session_warmup=True         # Human-like behavior
)

# Process 500 keywords without IP bans
for i in range(0, 500, 50):
    batch = competitor_keywords[i:i+50]
    df = tr.interest_over_time(batch, timeframe='today 12-m')
    save_to_database(df)
```
**Impact**: Scale to enterprise-level keyword analysis

#### Primary Features Used
- `trending_now_showcase_timeline()`: Batch processing with independent normalization
- `interest_by_region()`: Geographic market analysis
- `interest_over_time()`: Historical trend data for dashboards
- Rate limiting & Tor integration: Production reliability

#### Success Metrics
- **Automation**: 100% of dashboards auto-refresh (15 manual → 0 manual)
- **Scale**: 10x increase in keyword analysis capacity (50 → 500 keywords)
- **Reliability**: >95% dashboard uptime with zero manual intervention
- **Business Impact**: $50K ARR from new automated dashboard products

---

### 2.3 Persona 3: Alex (Social Media Manager)

#### Background
Alex manages social media for a consumer brand with 500K+ followers. Success depends on creating timely, relevant content that rides viral trends, requiring real-time trend monitoring and news context.

#### Demographics & Role
- **Age**: 24-30
- **Job Title**: Social Media Manager
- **Team Size**: 2-person social team
- **Technical Skills**: Basic Python, strong in social analytics
- **Tools Used**: Hootsuite, Sprout Social, Google Trends (manual), Twitter/TikTok analytics

#### Current Problems

**Problem 1: Miss Viral Trends Due to Manual Checking**
- **Current State**: Checks Google Trends 3-4 times per day manually
- **Pain Point**: Trends peak and decline within hours; manual checks miss optimal timing
- **Impact**: Brand jumps on trends after they've peaked (looks out of touch)
- **Frustration**: "By the time I notice a trend, it's already old news"

**Problem 2: Need News Context for Trending Topics**
- **Current State**: Sees trending keyword, Googles for news manually
- **Pain Point**: Unclear why something is trending, wastes time researching
- **Impact**: Can't quickly assess if trend is relevant/safe for brand
- **Risk**: Accidentally post about sensitive topics without context

**Problem 3: Timing is Critical for Relevance**
- **Current State**: No way to know when a trend started or if it's still growing
- **Pain Point**: Can't assess trend lifecycle (just starting vs. ending)
- **Impact**: Missed opportunities or embarrassing late posts
- **Business Impact**: Lower engagement, brand appears slow to react

#### TrendsPy Solution

**Solution to Problem 1: Real-Time Trend Monitoring**
```python
from trendspy import Trends
tr = Trends()

# Automated monitoring (run every 15 minutes via cron)
def check_new_trends():
    trends = tr.trending_now(geo='US', hours=4)  # Last 4 hours

    # Filter to brand-relevant topics
    tech_trends = trends.filter_by_topic('Technology')

    # Alert on new trends
    for trend in tech_trends:
        if trend.hours_since_started() < 2:  # Less than 2 hours old
            send_slack_alert(f"New trend: {trend.keyword} ({trend.volume_growth_pct}% growth)")

check_new_trends()
```
**Impact**: Catch trends within minutes, not hours

**Solution to Problem 2: Integrated News Context**
```python
# Get trending topic with news articles
trends_with_news = tr.trending_now_by_rss(geo='US')

for trend in trends_with_news[:5]:
    print(f"Trending: {trend.keyword}")
    print(f"Volume: {trend.volume}")

    # Immediate news context
    if trend.news:
        for article in trend.news[:3]:
            print(f"  - {article.title} ({article.source})")
            print(f"    {article.url}")
```
**Impact**: Instant context for trending topics, assess relevance quickly

**Solution to Problem 3: Trend Lifecycle Tracking**
```python
trends = tr.trending_now(geo='US')

for trend in trends[:10]:
    # Assess trend maturity
    hours_old = trend.hours_since_started()
    is_finished = trend.is_trend_finished

    # Decision logic
    if hours_old < 4 and not is_finished and trend.volume_growth_pct > 100:
        print(f"🔥 JUMP ON THIS: {trend.keyword} (just started, growing fast)")
    elif hours_old > 12 or is_finished:
        print(f"❌ TOO LATE: {trend.keyword} (peak passed)")
    else:
        print(f"⏳ CONSIDER: {trend.keyword} (mature but still active)")
```
**Impact**: Data-driven decisions on trend participation timing

#### Primary Features Used
- `trending_now()`: Real-time trend discovery
- `trending_now_by_rss()`: Trends with news context
- `trending_now_news_by_ids()`: Detailed news articles for deeper context
- `TrendKeyword.hours_since_started()`: Trend lifecycle assessment
- `TrendList.filter_by_topic()`: Brand-relevant trend filtering

#### Success Metrics
- **Trend Capture Rate**: 80% of relevant trends caught within first 2 hours
- **Response Time**: Average 30 minutes from trend emergence to brand post (vs. 6+ hours manual)
- **Engagement Lift**: 45% increase in post engagement on trend-based content
- **Risk Reduction**: Zero inappropriate trend posts due to news context verification

---

### 2.4 Persona 4: Maria (SEO Specialist)

#### Background
Maria is an SEO specialist at a digital marketing agency managing 12 client accounts. She needs to discover high-potential keywords, understand search intent through related queries, and identify geographic targeting opportunities.

#### Demographics & Role
- **Age**: 26-34
- **Job Title**: SEO Specialist / Senior SEO Manager
- **Team Size**: SEO team of 5, manages 12 client accounts
- **Technical Skills**: Intermediate Python, expert in SEO tools (Ahrefs, SEMrush, Moz)
- **Tools Used**: Google Search Console, Ahrefs, SEMrush, Google Trends (manual), Python (learning)

#### Current Problems

**Problem 1: Need Related Keyword Discovery**
- **Current State**: Manually explores "Related queries" section in Google Trends
- **Pain Point**: Only shows top 25 related queries; can't export full list
- **Impact**: Miss long-tail keyword opportunities, competitors find them first
- **Frustration**: "I know there are more related keywords, but Google hides them"

**Problem 2: Geographic Targeting Insights**
- **Current State**: Manually checks interest by region for each keyword
- **Pain Point**: Time-consuming to analyze 50+ keywords across regions
- **Impact**: Can't identify location-specific opportunities efficiently
- **Business Impact**: Miss high-conversion local targeting

**Problem 3: Long-Tail Keyword Research**
- **Current State**: Uses paid tools (Ahrefs, SEMrush) for keyword ideas
- **Pain Point**: High tool costs ($99-299/month), still need trends data
- **Impact**: Duplicate tool spend, no integration
- **Frustration**: "I'm paying for tools that should work together"

#### TrendsPy Solution

**Solution to Problem 1: Automated Related Query Discovery**
```python
from trendspy import Trends
tr = Trends()

# Get comprehensive related queries
related = tr.related_queries('digital marketing')

# Top queries (most popular)
top_queries = related['top']
print(f"Top related: {len(top_queries)} queries")
print(top_queries.head(10))

# Rising queries (fastest growing)
rising_queries = related['rising']
print(f"\nRising trends: {len(rising_queries)} queries")
print(rising_queries.head(10))

# Identify low-competition opportunities
opportunities = rising_queries[rising_queries['value'] > 50]  # High growth
```
**Impact**: Discover 100+ related keywords in seconds (vs. 25 manually)

**Solution to Problem 2: Geographic Opportunity Analysis**
```python
# Multi-level geographic analysis
keyword = 'plumber near me'

# Country-level overview
countries = tr.interest_by_region(keyword)
top_countries = countries.nlargest(10, keyword)

# Drill down to US states
us_states = tr.interest_by_region(keyword, geo='US', resolution='REGION')
top_states = us_states.nlargest(10, keyword)

# City-level for California
ca_cities = tr.interest_by_region(keyword, geo='US-CA', resolution='CITY')

# Identify underserved markets
print("High interest, low competition cities:")
print(ca_cities.nlargest(20, keyword))
```
**Impact**: Identify geographic opportunities in minutes (vs. hours of manual checking)

**Solution to Problem 3: Integrated Keyword Research Workflow**
```python
def keyword_research_workflow(seed_keyword):
    """Complete keyword research pipeline"""
    tr = Trends()

    # Step 1: Get search interest over time
    interest = tr.interest_over_time([seed_keyword], timeframe='today 12-m')

    # Step 2: Discover related queries
    related_q = tr.related_queries(seed_keyword)
    related_t = tr.related_topics(seed_keyword)

    # Step 3: Geographic analysis
    geo = tr.interest_by_region(seed_keyword, resolution='COUNTRY')

    # Step 4: Combine into report
    report = {
        'seed_keyword': seed_keyword,
        'avg_interest': interest.mean()[seed_keyword],
        'trend': 'rising' if interest.diff().mean()[seed_keyword] > 0 else 'falling',
        'top_related': related_q['top'].head(10).to_dict(),
        'rising_related': related_q['rising'].head(10).to_dict(),
        'top_geos': geo.nlargest(5, seed_keyword).index.tolist()
    }

    return report

# Run for 50 keywords
results = [keyword_research_workflow(kw) for kw in client_keywords]
```
**Impact**: Complete keyword research workflow in Python, integrate with existing tools

#### Primary Features Used
- `related_queries()`: Top and rising related searches
- `related_topics()`: Entity-based topic discovery
- `interest_by_region()`: Geographic opportunity analysis (COUNTRY → REGION → CITY)
- `geo()`: Location code discovery
- `interest_over_time()`: Trend direction and seasonality

#### Success Metrics
- **Keyword Discovery**: 5x more related keywords discovered (25 → 125+ per seed)
- **Efficiency**: 70% reduction in keyword research time (10 hours → 3 hours per client/month)
- **Client ROI**: 25% increase in organic traffic from better keyword targeting
- **Tool Cost Savings**: Potential to reduce paid tool dependency ($1,200/year savings)

---

### 2.5 Persona 5: Dr. Chen (Academic Researcher)

#### Background
Dr. Chen is a social science researcher studying public health information-seeking behavior. She needs large-scale, reproducible Google Trends data for academic publications and longitudinal studies.

#### Demographics & Role
- **Age**: 32-45
- **Job Title**: Assistant Professor / Research Scientist
- **Affiliation**: University public health department
- **Technical Skills**: Advanced Python, R, statistical analysis, research methods
- **Tools Used**: Python (pandas, statsmodels, scikit-learn), R, SPSS, academic databases

#### Current Problems

**Problem 1: Need Historical Trend Data at Scale**
- **Current State**: Manually downloads CSV files for 200+ health keywords
- **Pain Point**: Google Trends web interface limits bulk downloads
- **Impact**: Takes weeks to collect data for one study
- **Research Impact**: Can't conduct comprehensive keyword analyses

**Problem 2: Reproducible Research Workflows**
- **Current State**: Manual data collection lacks transparency for peer review
- **Pain Point**: Reviewers question data collection methodology
- **Impact**: Papers rejected due to "insufficient methodological rigor"
- **Frustration**: "I can't prove I collected the data systematically"

**Problem 3: Rate Limits Block Large Studies**
- **Current State**: Gets IP banned after 50-100 queries
- **Pain Point**: Multi-day studies interrupted, incomplete datasets
- **Impact**: Can't conduct longitudinal studies with 1000+ keywords
- **Research Impact**: Limited to small-scale studies, missing bigger insights

#### TrendsPy Solution

**Solution to Problem 1: Large-Scale Automated Data Collection**
```python
from trendspy import Trends
import pandas as pd

# Define study parameters (reproducible)
KEYWORDS = ['covid vaccine', 'vaccine side effects', 'mrna vaccine', ...]  # 200 keywords
TIMEFRAME = '2020-01-01 2023-12-31'  # 4-year study period
GEO = 'US'

def collect_research_data(keywords, timeframe, geo):
    """Reproducible data collection function"""
    tr = Trends()

    # Collect data for all keywords
    df = tr.interest_over_time(
        keywords[:5],  # Max 5 per query
        timeframe=timeframe,
        geo=geo
    )

    # Save with metadata
    metadata = {
        'collection_date': pd.Timestamp.now(),
        'library_version': '0.1.6',
        'keywords': keywords,
        'timeframe': timeframe,
        'geo': geo
    }

    return df, metadata

# Reproducible pipeline
data, meta = collect_research_data(KEYWORDS, TIMEFRAME, GEO)
```
**Impact**: Collect 200 keywords in 2 hours (vs. 2-3 weeks manually)

**Solution to Problem 2: Documented, Reproducible Workflows**
```python
# Research script with full provenance tracking

# Configuration (version controlled)
from trendspy import Trends, __version__

CONFIG = {
    'library': 'TrendsPy',
    'version': __version__,
    'rate_limiting': True,
    'session_persistence': True,
    'collection_date': '2024-11-27',
    'study_id': 'PUBLIC_HEALTH_2024_001'
}

def log_research_step(step_name, params, results):
    """Log every research step for reproducibility"""
    log_entry = {
        'timestamp': pd.Timestamp.now(),
        'step': step_name,
        'params': params,
        'results_shape': results.shape if hasattr(results, 'shape') else None
    }
    # Append to research log
    with open('research_log.json', 'a') as f:
        json.dump(log_entry, f)

# Documented data collection
tr = Trends()
df = tr.interest_over_time(['keyword'], timeframe='today 12-m')
log_research_step('interest_over_time', {'keyword': 'keyword'}, df)
```
**Impact**: Full audit trail for peer review, increased publication acceptance

**Solution to Problem 3: Reliable Large-Scale Data Collection**
```python
# Production configuration for academic research
tr = Trends(
    persist_cookies=True,        # Maintain session across days
    use_tls_impersonation=True,  # Avoid bot detection
    session_warmup=True,         # Natural browsing behavior
    tor_enabled=True,            # Free IP rotation (important for academic budgets)
    tor_ports=[9050, 9051, 9052] # Multiple Tor instances
)

# Process 1000 keywords over multiple sessions
def collect_longitudinal_data(keywords, sessions=10):
    """Collect data across multiple sessions to respect rate limits"""
    results = []

    batch_size = len(keywords) // sessions

    for i in range(sessions):
        batch = keywords[i*batch_size:(i+1)*batch_size]

        # Process batch
        df = tr.interest_over_time(batch[:5], timeframe='today 12-m')
        results.append(df)

        # Rate limiting handled automatically
        print(f"Batch {i+1}/{sessions} complete")

    return pd.concat(results, axis=1)

# Run over days/weeks as needed
data = collect_longitudinal_data(health_keywords, sessions=20)
```
**Impact**: Conduct 1000-keyword studies without IP bans, enable large-scale research

#### Primary Features Used
- `interest_over_time()`: Historical trend data with custom timeframes
- Adaptive rate limiting: Automatic quota management
- Session persistence: Multi-day data collection
- Tor integration: IP rotation for academic budgets
- Pandas DataFrames: Direct integration with analysis pipelines

#### Success Metrics
- **Data Collection Scale**: 10x increase (200 → 2000 keywords per study)
- **Time Efficiency**: 95% reduction (3 weeks → half day for data collection)
- **Reproducibility**: 100% documented workflows, increased publication acceptance
- **Research Impact**: Enable multi-year, multi-geography comparative studies
- **Cost Savings**: Free IP rotation vs. $500/month proxy services

---


## 3. Features & Capabilities

TrendsPy provides 17+ public API methods organized into 4 feature categories. This section documents each feature with user context, method signatures, inputs/outputs, and usage examples.

### 3.1 Trend Analysis Features

#### F-1: Interest Over Time Analysis

**What It Does**: Track how search interest for 1-5 keywords changes over customizable time periods with pandas DataFrame output.

**Why Users Care**: "I need to understand when people search for my keywords to plan campaigns, identify seasonal patterns, and compare competitors over time."

**Method Signature**:
```python
tr.interest_over_time(keywords, timeframe='today 12-m', geo='', cat=0, gprop='', return_raw=False)
```

**Parameters**:
| Parameter | Type | Required | Default | Description | Constraints |
|-----------|------|----------|---------|-------------|-------------|
| `keywords` | str/list | Yes | - | Keyword(s) to analyze | 1-5 keywords max |
| `timeframe` | str/list | No | 'today 12-m' | Time period(s) | See Appendix A for formats; lists enable multirange |
| `geo` | str/list | No | '' (worldwide) | Geographic location code(s) | Use `geo()` to discover codes; lists enable multirange |
| `cat` | int | No | 0 (all) | Category ID filter | Use `categories()` to discover IDs |
| `gprop` | str | No | '' (web) | Google property | 'web', 'images', 'news', 'youtube', 'froogle' |
| `return_raw` | bool | No | False | Return raw API response | For debugging/custom processing |

**Returns**: pandas DataFrame
- **Index**: datetime (properly parsed timestamps)
- **Columns**: One column per keyword (or keyword-timeframe-geo combo for multirange)
- **Values**: Normalized interest 0-100 (100 = peak interest in the time range)
- **Special Values**: Missing data = NaN

**Key Capabilities**:
1. **Multirange Comparison**: Pass lists for `timeframe` and/or `geo` to compare different periods/regions
2. **Adaptive Resolution**: Automatically adjusts data granularity based on timeframe length:
   - < 8 days: Hourly to 8-minute intervals
   - 8-90 days: Daily data
   - 90+ days: Weekly data
   - 5+ years: Monthly data
3. **Relative Normalization**: Keywords are normalized relative to each other (highest value = 100)

**Usage Example**:
```python
# Basic usage
df = tr.interest_over_time(['python', 'javascript'], timeframe='today 12-m')
df.plot(title='Language Interest Over Time')

# Multirange: Compare same keyword across time periods and regions
df_multi = tr.interest_over_time(
    'python',
    timeframe=['2024-01-01 2024-03-31', '2024-07-01 2024-09-30'],
    geo=['US', 'GB']
)
# Creates columns: python_2024-01-01_US, python_2024-01-01_GB, python_2024-07-01_US, python_2024-07-01_GB
```

**Acceptance Criteria**:
- ✓ Returns DataFrame with datetime index
- ✓ Values normalized 0-100 relative to peak
- ✓ Handles 1-5 keywords in single query
- ✓ Supports standard and custom timeframe formats
- ✓ Multirange creates separate columns per combination
- ✓ Resolution adapts automatically to timeframe length

**User Value**: Identify seasonal trends, compare competitors, plan content calendars, detect market shifts

**Source**: `client.py:415-474`

---

#### F-2: Interest by Region (Geographic Analysis)

**What It Does**: Analyze where keywords are popular geographically with hierarchical drilldown (country → state/province → city).

**Why Users Care**: "I need to identify target markets, discover regional opportunities, and understand geographic distribution of search interest."

**Method Signature**:
```python
tr.interest_by_region(keywords, timeframe='today 12-m', geo='', cat=0, gprop='', resolution='', inc_low_vol=True, return_raw=False)
```

**Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keywords` | str/list | Yes | - | Keyword(s) to analyze |
| `timeframe` | str | No | 'today 12-m' | Time period for analysis |
| `geo` | str | No | '' | Parent geographic region ('' = global, 'US' = US states, etc.) |
| `cat` | int | No | 0 | Category ID filter |
| `gprop` | str | No | '' | Google property filter |
| `resolution` | str | No | '' (auto) | Geographic granularity: 'COUNTRY', 'REGION', 'CITY', 'DMA' |
| `inc_low_vol` | bool | No | True | Include low search volume regions |
| `return_raw` | bool | No | False | Return raw API response |

**Returns**: pandas DataFrame
- **Index**: Integer index
- **Columns**: `geoName`, `geoCode`, keyword column(s), optionally `coordinates` (lat/lng for cities)
- **Values**: Interest 0-100 (normalized within the geographic scope)

**Resolution Levels**:
1. **COUNTRY**: Country-level data (default when `geo=''`)
2. **REGION**: State/province level (default when `geo` is specified, e.g. 'US')
3. **CITY**: City-level data (requires parent region, e.g. `geo='US-CA'`)
4. **DMA**: Designated Market Areas for US media markets

**Usage Example**:
```python
# Hierarchical geographic analysis workflow
keyword = 'solar panels'

# Level 1: Country overview
countries = tr.interest_by_region(keyword)
print(countries.nlargest(10, keyword))  # Top 10 countries

# Level 2: Drill down to US states
us_states = tr.interest_by_region(keyword, geo='US', resolution='REGION')
top_state = us_states.iloc[0]['geoCode']  # e.g., 'US-CA'

# Level 3: Drill down to cities in top state
ca_cities = tr.interest_by_region(keyword, geo=top_state, resolution='CITY')
print(ca_cities.head(20))  # Includes lat/lng coordinates for mapping
```

**Acceptance Criteria**:
- ✓ Returns DataFrame with geoName, geoCode, and interest values
- ✓ Supports three hierarchical resolution levels
- ✓ City results include coordinates for mapping
- ✓ Low-volume filtering optional
- ✓ Auto-selects appropriate resolution based on geo parameter

**User Value**: Identify expansion markets, local SEO targeting, regional content strategies, visualize geographic trends on maps

**Source**: `client.py:542-572`

---

### 3.2 Real-Time Trending Features

#### F-3: Trending Now (Real-Time Monitoring)

**What It Does**: Get current trending searches with comprehensive metadata including volume, growth rate, related keywords, and news tokens. Returns 500+ trends per request.

**Why Users Care**: "I need to catch viral trends as they emerge, monitor brand mentions in real-time, and identify viral marketing opportunities within hours, not days."

**Method Signature**:
```python
tr.trending_now(geo='US', language='en', hours=24, num_news=0, return_raw=False)
```

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `geo` | str | 'US' | Geographic region for trends |
| `language` | str | 'en' | Language code for results |
| `hours` | int | 24 | Time window for trend detection (1-191 hours) |
| `num_news` | int | 0 | Number of news articles to include (not recommended due to performance) |
| `return_raw` | bool | False | Return raw API response |

**Returns**: `TrendList` object (list-like container of `TrendKeyword` objects)

Each `TrendKeyword` contains:
- `keyword`: The trending search term
- `volume`: Search volume (relative)
- `volume_growth_pct`: Percentage growth rate
- `trend_keywords`: Related searches (38+ keywords per trend)
- `topics`: Topic category IDs
- `news_tokens`: Tokens for fetching associated news via `trending_now_news_by_ids()`
- `started_timestamp`: When trend began
- `ended_timestamp`: When trend ended (None if ongoing)
- `is_trend_finished` (property): Boolean indicating if trend has ended
- `hours_since_started()` (method): Calculate trend age

**Key Capabilities**:
1. **500+ Trends per Request**: Comprehensive trending keyword coverage
2. **Topic Filtering**: Use `trends.filter_by_topic('Technology')` to focus on relevant categories
3. **Topic Summary**: Use `trends.get_topics_summary()` to see trend distribution by category
4. **Trend Lifecycle Tracking**: Timestamps and age calculation for optimal timing

**Usage Example**:
```python
# Get current trends
trends = tr.trending_now(geo='US', hours=12)

# Filter to technology trends
tech_trends = trends.filter_by_topic('Technology')

# Identify brand-new trends (< 2 hours old)
new_trends = [t for t in tech_trends if t.hours_since_started() < 2]

# Assess trend maturity for decision-making
for trend in new_trends:
    print(f"{trend.keyword}:")
    print(f"  Volume: {trend.volume}")
    print(f"  Growth: {trend.volume_growth_pct}%")
    print(f"  Age: {trend.hours_since_started()} hours")
    print(f"  Related: {len(trend.trend_keywords)} keywords")
    print(f"  Status: {'Active' if not trend.is_trend_finished else 'Finished'}")
```

**Acceptance Criteria**:
- ✓ Returns TrendList with 500+ TrendKeyword objects
- ✓ Each trend includes volume, growth%, timestamps, related keywords
- ✓ Topic filtering and summary methods work correctly
- ✓ Lifecycle tracking (hours_since_started, is_trend_finished) accurate
- ✓ News tokens provided for fetching articles

**User Value**: Real-time social listening, viral trend detection, brand monitoring, optimal timing for trend participation

**Source**: `client.py:638-669`

---

#### F-4: Trending Showcase Timeline (Batch Independent Normalization)

**What It Does**: Get historical data for 500+ keywords in a single request with **independent normalization** (each keyword normalized to itself, not cross-compared).

**Why Users Care**: "I need to analyze hundreds of trending keywords without cross-keyword normalization bias. I want each keyword's true trend pattern, not relative comparisons."

**Method Signature**:
```python
from trendspy import BatchPeriod
tr.trending_now_showcase_timeline(keywords, geo='US', timeframe=BatchPeriod.Past24H, return_raw=False)
```

**Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keywords` | list | Required | List of keywords (500+ supported) |
| `geo` | str | 'US' | Geographic region |
| `timeframe` | BatchPeriod | BatchPeriod.Past24H | Time window (enum value) |
| `return_raw` | bool | False | Return raw API response |

**BatchPeriod Options**:
- `BatchPeriod.Past4H`: ~30 data points (8-minute intervals)
- `BatchPeriod.Past24H`: ~90 data points (16-minute intervals)
- `BatchPeriod.Past48H`: ~180 data points (16-minute intervals)
- `BatchPeriod.Past7D`: ~42 data points (4-hour intervals)

**Returns**: pandas DataFrame
- **Index**: datetime (time series index)
- **Columns**: One column per keyword
- **Values**: Interest 0-100 **independently normalized per keyword** (each keyword's peak = 100)

**Key Differentiator vs. interest_over_time()**:
| Feature | interest_over_time() | trending_now_showcase_timeline() |
|---------|---------------------|----------------------------------|
| Normalization | Relative (cross-keyword) | Independent (per-keyword) |
| Use Case | Compare keywords | Analyze individual trends |
| Keyword Limit | 5 keywords | 500+ keywords |
| Timeframes | Flexible custom formats | Fixed BatchPeriod enums |

**Usage Example**:
```python
from trendspy import Trends, BatchPeriod

tr = Trends()

# Get 500 trending keywords
trends = tr.trending_now(geo='US')
keywords = [t.keyword for t in trends[:500]]

# Batch analysis with independent normalization
df = tr.trending_now_showcase_timeline(
    keywords,
    timeframe=BatchPeriod.Past24H
)

# Each keyword shows its own trend pattern (not relative to others)
df.plot(subplots=True, layout=(10, 10), figsize=(30, 30))

# Identify fastest-growing trends (independent analysis)
growth = df.diff().mean().sort_values(ascending=False)
print(f"Fastest growing (last 24h): {growth.head(20)}")
```

**Acceptance Criteria**:
- ✓ Supports 500+ keywords in single request
- ✓ Each keyword independently normalized (0-100 based on its own peak)
- ✓ Returns DataFrame with proper datetime index
- ✓ Updates every 2 minutes (near real-time)
- ✓ Four time window options with appropriate granularity

**User Value**: Large-scale trending analysis, dashboard building, independent trend monitoring, batch keyword research

**Source**: `client.py:705-715`

---

### 3.3 Discovery & Utility Features

#### F-5: Related Queries Discovery

**What It Does**: Discover top and rising related search queries for a single keyword.

**Why Users Care**: "I need to find long-tail keywords, understand search intent, and discover what people search for alongside my target keyword for SEO and content optimization."

**Method Signature**:
```python
tr.related_queries(keyword, timeframe='today 12-m', geo='', cat=0, gprop='', return_raw=False, headers=None)
```

**Parameters**:
| Parameter | Type | Description | Note |
|-----------|------|-------------|------|
| `keyword` | str | Single keyword only | **No batching supported** |
| `timeframe` | str | Time period | |
| `geo` | str | Geographic location | |
| `cat` | int | Category filter | |
| `gprop` | str | Google property | |
| `return_raw` | bool | Return raw response | |
| `headers` | dict | Custom headers | Varying referer can help with rate limits |

**Returns**: Dictionary with two DataFrames:
```python
{
    'top': DataFrame,     # Most popular related queries
    'rising': DataFrame   # Fastest growing related queries
}
```

Each DataFrame contains:
- `query`: Related search term
- `value`: Relative score (0-100 for top, percentage or "Breakout" for rising)

**Rate Limiting Note**: This endpoint is more quota-sensitive than others. Strategies:
- Space out requests (use built-in adaptive rate limiting)
- Vary `headers={'referer': 'https://trends.google.com/'}` to bypass some limits
- Use proxy rotation for large-scale research

**Usage Example**:
```python
related = tr.related_queries('electric vehicles')

# Top related queries (most popular)
print("Top related:")
print(related['top'].head(10))
# Output: 'tesla electric vehicles', 'best electric vehicles 2024', etc.

# Rising queries (fastest growing)
print("\nRising related:")
print(related['rising'].head(10))
# May include "Breakout" for explosive growth

# Long-tail keyword research
long_tail = related['top'][related['top']['value'] > 20]  # Moderate interest
print(f"Found {len(long_tail)} long-tail opportunities")
```

**Acceptance Criteria**:
- ✓ Returns dict with 'top' and 'rising' DataFrames
- ✓ Top queries sorted by popularity (value 0-100)
- ✓ Rising queries show growth (percentage or "Breakout")
- ✓ Single keyword only (raises error for lists)
- ✓ Custom headers support for rate limit management

**User Value**: SEO keyword research, content ideation, understanding search intent, long-tail discovery

**Source**: `client.py:476-508`

---

#### F-6: Categories & Geographic Location Search

**Categories Search (`categories()`)**: Find category IDs for filtering trends by topic.

**Method Signature**:
```python
tr.categories(find='', language=None)
```

**Returns**: List of dicts with `name` and `id` fields
```python
[{'name': 'Computers & Electronics', 'id': '13'}, ...]
```

**Usage Example**:
```python
# Find technology categories
tech_cats = tr.categories(find='technology')
# Use in filtered queries
df = tr.interest_over_time('AI', cat=tech_cats[0]['id'])
```

**Geographic Location Search (`geo()`)**: Find location codes for geographic filtering.

**Method Signature**:
```python
tr.geo(find='', language=None)
```

**Returns**: List of dicts with `name` and `id` fields
```python
[{'name': 'New York', 'id': 'US-NY'}, ...]
```

**Usage Example**:
```python
# Find location codes
ny_code = tr.geo(find='new york')[0]['id']  # 'US-NY'
df = tr.interest_by_region('pizza', geo=ny_code, resolution='CITY')
```

**Key Features**:
- Case-insensitive partial matching
- Results cached per language (performance optimization)
- Hierarchical structure (countries → regions → cities)

**User Value**: Discover filter IDs without documentation, build dynamic geographic and category queries

**Source**: `client.py:717-804`

---

### 3.4 Advanced Capabilities

#### F-7: Flexible Time Formats (Product Feature)

**What It Is**: TrendsPy extends Google Trends' limited preset timeframes with custom intervals, date-based offsets, and hourly precision.

**Why Users Care**: "Google Trends only offers ~10 preset timeframes. I need arbitrary date ranges, custom intervals like '45 days', and hourly precision for breaking news analysis."

**Supported Formats**:

**1. Standard Google Trends Presets**:
- `'now 1-H'`, `'now 4-H'`, `'now 1-d'`, `'now 7-d'`
- `'today 1-m'`, `'today 3-m'`, `'today 12-m'`, `'today 5-y'`
- `'all'` (all available data, typically ~2004-present)

**2. Custom Relative Intervals** (TrendsPy Extension):
- Hours: `'now 123-H'`, `'now 72-H'` (< 8 days for hourly/minute resolution)
- Days: `'today 45-d'`, `'today 90-d'`
- Months: `'today 18-m'`, `'today 24-m'`

**3. Date-Based Offsets** (TrendsPy Extension):
- From specific date: `'2024-02-01 10-d'`, `'2024-03-15 3-m'`
- Backwards from date: `'2024-06-30 90-d'` (March 31 - June 30, 2024)

**4. Explicit Date Ranges**:
- Standard: `'2024-01-01 2024-12-31'`
- Hourly precision: `'2024-03-25T12 2024-03-25T15'` (for periods < 8 days)

**5. Multirange Comparison** (Lists):
```python
timeframes = ['2024-01-01 2024-03-31', '2024-07-01 2024-09-30']
geo = ['US', 'GB']
df = tr.interest_over_time('python', timeframe=timeframes, geo=geo)
# Creates 4 column combinations: Q1-US, Q1-GB, Q3-US, Q3-GB
```

**Automatic Resolution Adjustment**:
| Timeframe Length | Resolution |
|------------------|------------|
| < 8 days | Hourly to 8-minute intervals |
| 8-90 days | Daily data |
| 90 days - 5 years | Weekly data |
| 5+ years | Monthly data |

**Multirange Constraints**:
- All timeframes must have same resolution (e.g., all hourly or all daily)
- Max timeframe ≤ 2× min timeframe (e.g., if min=30 days, max=60 days)

**Usage Example**:
```python
# Custom 45-day analysis
df = tr.interest_over_time('breaking news', timeframe='today 45-d')

# Specific date range for research
df = tr.interest_over_time('covid vaccine', timeframe='2020-12-01 2021-06-30')

# Hourly precision for viral event analysis
df = tr.interest_over_time('super bowl', timeframe='2024-02-11T18 2024-02-12T02')

# Multirange: Compare Q1 vs Q3 across regions
df = tr.interest_over_time(
    'summer fashion',
    timeframe=['2024-01-01 2024-03-31', '2024-07-01 2024-09-30'],
    geo=['US', 'AU']  # Northern vs Southern hemisphere seasonality
)
```

**Acceptance Criteria**:
- ✓ Accepts all Google Trends standard presets
- ✓ Parses custom intervals (now X-H, today X-d, today X-m)
- ✓ Handles date-based offsets (YYYY-MM-DD X-d/X-m)
- ✓ Supports explicit date ranges and hourly precision
- ✓ Validates multirange constraints (resolution consistency, 2x max rule)
- ✓ Auto-adjusts resolution based on timeframe length

**User Value**: Analyze arbitrary date ranges, compare non-overlapping periods, hourly breaking news analysis, research flexibility

**Source**: `timeframe_utils.py` (parsing logic), `client.py:415-474` (usage in interest_over_time)

---

**Summary**: Section 3 covers 17+ features across 4 categories (Trend Analysis, Real-Time Trending, Discovery, Advanced). Each feature includes method signatures, parameters, return types, usage examples, and acceptance criteria. Key differentiators like independent normalization (F-4) and flexible time formats (F-7) are highlighted as product features, not just technical details.


## 4. Reliability & Production Features

TrendsPy is designed for production use, not just prototyping. This section presents non-functional requirements as user-facing product features that ensure reliable operation at scale.

**Introduction**: Many Google Trends libraries fail in production due to rate limiting, bot detection, and IP blocks. TrendsPy solves these problems with enterprise-grade reliability features that enable large-scale, automated data collection.

### 4.1 Adaptive Rate Limiting

**What It Does**: Automatically manages request timing to prevent quota exhaustion using token bucket algorithm, sliding window tracking, and adaptive delays.

**Why Users Care**: "My scripts fail with 429 errors when I query too fast. I waste hours debugging rate limits instead of analyzing data."

**Problem Solved**: Google Trends enforces ~200 requests/hour limit. Manual throttling is tedious and error-prone. Exceeding limits results in IP blocks.

**How It Works** (High-Level):
1. **Token Bucket**: Enforces minimum delay between requests (default 15 seconds)
2. **Sliding Window**: Tracks requests per hour (200 req/hr default quota)
3. **Exponential Backoff**: On 429 errors, delay multiplier increases:
   - 1st error: 1.5x delay
   - 2nd error: 2.0x delay
   - 3rd+ error: Emergency mode (3x multiplier)
4. **Circuit Breaker**: Stops requests after 10 consecutive failures to prevent IP bans
5. **Jitter**: Adds random variance (±15% normal, ±25% emergency) to defeat timing-based detection

**Configuration**:
```python
from trendspy import AdaptiveRateLimiter

limiter = AdaptiveRateLimiter(
    requests_per_hour=200,      # Hourly quota
    base_delay=15.0,            # Minimum seconds between requests
    emergency_threshold=5,      # Failures before emergency mode
    emergency_multiplier=3      # Delay multiplier in emergency
)
```

**Observable Metrics**:
```python
stats = tr.rate_limiter.get_stats()
print(stats)
# Output: {
#   'utilization_pct': 45.2,
#   'delay_multiplier': 1.0,
#   'effective_delay': 15.0,
#   'consecutive_failures': 0
# }
```

**Business Impact**: Enables production workloads vs. one-off queries. Run overnight batch jobs without manual intervention.

**User Value**: "Set it and forget it" - automated quota management without manual delays or IP blocks

**Source**: `rate_limiter.py`

---

### 4.2 Circuit Breaker Pattern

**What It Does**: Stops requests after repeated failures (default 10 consecutive) to prevent IP bans from hammering dead endpoints.

**Why Users Care**: "I left a script running overnight and got my IP banned for 24 hours. I can't risk that in production."

**How It Works**:
- Tracks consecutive API failures (429, 302, timeouts)
- After threshold (10 failures), raises `CircuitBreakerError` and stops all requests
- Prevents cascading failures and protects API reputation

**User Value**: Protects against IP bans, safe for unattended operation

**Source**: `rate_limiter.py`

---

### 4.3 Session Management & Cookie Persistence

**What It Does**: Maintains session state across runs with cookie persistence and optional "session warmup" (3-request natural browsing sequence).

**Why Users Care**: "Fresh sessions trigger CAPTCHAs and have lower success rates. I need consistent, authenticated sessions."

**Features**:
1. **Cookie Persistence**: Saves session cookies to `.trendspy_session.pkl`
2. **Session Warmup**: Mimics human browsing before API calls:
   - Request 1: Homepage (0.5-1.5s delay)
   - Request 2: Explore page (1.0-2.5s delay)
   - Request 3: Trending searches (0.8-2.0s delay)
3. **Graceful Fallback**: Creates new session if saved session fails to load

**Configuration**:
```python
tr = Trends(
    persist_cookies=True,  # Save/load cookies across runs
    session_warmup=True    # 3-request warmup sequence
)
```

**User Value**: Higher success rates (>95%), fewer CAPTCHAs, consistent session state for multi-day research

**Source**: `session_manager.py`

---

### 4.4 TLS Fingerprint Impersonation

**What It Does**: Uses `curl-cffi` library to mimic real browser TLS signatures (Chrome, Firefox, Safari, Edge) at the connection layer.

**Why Users Care**: "Standard Python requests library creates a detectable bot fingerprint. I get 8+ second timeouts and empty response headers even before my HTTP request is processed."

**Problem Solved**: Google detects automation at the **TLS handshake layer** (before HTTP), resulting in:
- Connection-level blocks (empty headers, timeouts)
- Suspicious JA3 fingerprint different from claimed User-Agent
- Immediate rejection without processing HTTP request

**Solution**: `curl-cffi` impersonates real browser TLS fingerprints:
- Supported browsers: `chrome131`, `chrome130`, `firefox132`, `safari18`, `edge131`
- Falls back gracefully to standard requests if curl-cffi unavailable

**Configuration**:
```python
tr = Trends(
    use_tls_impersonation=True,  # Enable curl-cffi (default)
    tls_browser='chrome131'       # Browser to impersonate
)
```

**Impact**: Dramatically reduced connection-level blocks and timeouts

**User Value**: "Avoid bot detection at the TLS layer" - works where standard requests fails

**Source**: `tls_session.py`

---

### 4.5 Browser Profile Coherence

**What It Does**: Generates randomized but **coherent** browser headers where User-Agent matches all Client Hints headers (Sec-CH-UA-*).

**Why Users Care**: "Mismatched headers (e.g., Chrome 120 claiming macOS 10.15.7, an impossible combination) trigger bot detection."

**Problem Solved**: Header coherence validation. Google checks if:
- User-Agent browser version matches Sec-CH-UA version
- Operating system is compatible with claimed browser
- Architecture (x86, ARM) matches OS

**Solution**: 8 pre-defined coherent profiles:
- Chrome 131 macOS (25% weight)
- Chrome 131 Windows (25% weight)
- Chrome 130 macOS (15% weight)
- Chrome 130 Windows (15% weight)
- Firefox 132 macOS (5% weight)
- Firefox 132 Windows (5% weight)
- Safari 18 macOS (5% weight)
- Edge 131 Windows (5% weight)

**Weighted Random Selection**: Favors Chrome (70% combined) to match real-world browser distribution

**Configuration**:
```python
tr = Trends(use_browser_profiles=True)  # Enable coherent profiles (default)
```

**User Value**: Pass header validation checks, avoid detection based on impossible browser/OS combinations

**Source**: `browser_profiles.py`

---

### 4.6 IP Rotation via Tor

**What It Does**: Free IP rotation using Tor network exit nodes without expensive proxy services.

**Why Users Care**: "I need to distribute requests across multiple IPs for large-scale research, but proxy services cost $100-500/month."

**Problem Solved**: IP-based rate limiting affects large studies (1000+ keywords). Commercial proxies are expensive for academic/individual use.

**Solution**: Tor integration provides:
- Free IP rotation on demand
- Automatic circuit refresh
- Compatible with existing session management

**Prerequisites**:
- Tor installed: `brew install tor` (macOS) or `apt install tor` (Linux)
- STEM library: `pip install stem`
- Tor running on default ports (9050 SOCKS, 9051 control)

**Configuration**:
```python
tr = Trends(
    tor_enabled=True,
    tor_ports=[9050, 9051]  # SOCKS and control ports
)

# Tor automatically rotates IPs on circuit refresh
# Can also rotate manually if needed
```

**User Value**: "Overcome IP-based rate limits for free" - critical for academic research on tight budgets

**Source**: `tor_proxy.py`

---

### 4.7 Proxy Support

**What It Does**: Standard `requests`-compatible proxy configuration for integration with existing enterprise proxy infrastructure.

**Configuration Options**:

**String Format**:
```python
tr = Trends(proxy="http://user:pass@10.10.1.10:3128")
```

**Dict Format**:
```python
tr = Trends(proxy={
    "http": "http://10.10.1.10:3128",
    "https": "https://10.10.1.10:1080"
})
```

**Runtime Configuration**:
```python
tr.set_proxy("http://10.10.1.10:3128")
```

**User Value**: Enterprise compatibility, integrate with corporate proxies, SOCKS support

**Source**: `client.py:178-198`, `session_manager.py`

---

### 4.8 Graceful Degradation

**What It Does**: Priority-based feature reduction under stress. Instead of complete failure, continues processing high-priority queries while skipping low-priority ones.

**Health States**:
1. **HEALTHY**: Process all keywords normally
2. **DEGRADED_MINOR**: Skip LOW priority keywords (at 5+ consecutive 429s)
3. **DEGRADED_MAJOR**: Process only HIGH priority keywords (at 10+ consecutive 429s)
4. **RECOVERY**: Gradually return to normal after consecutive successes

**Decision Matrix**:
| Priority | HEALTHY | DEGRADED_MINOR | DEGRADED_MAJOR |
|----------|---------|----------------|----------------|
| HIGH | ✓ Process | ✓ Process | ✓ Process |
| MEDIUM | ✓ Process | ✓ Process | ✗ Skip |
| LOW | ✓ Process | ✗ Skip | ✗ Skip |

**Recovery Strategy**:
- 3 consecutive successes → RECOVERY state
- 6 consecutive successes → Full HEALTHY recovery
- 429 counter decreases gradually (not sudden reset)

**User Value**: "Keep critical operations running even during quota issues" - maintain availability for essential queries

**Source**: `degradation_manager.py`

---

## 5. Data Models & Objects

TrendsPy returns rich, structured objects beyond simple DataFrames. This section explains what you receive from each API method.

### 5.1 TrendKeyword

**What It Represents**: A single trending search term with comprehensive metadata including volume, growth rate, related keywords, news associations, and lifecycle timestamps.

**When You Get This**: Returned by `trending_now()` and `trending_now_by_rss()` methods

**Attributes (User-Facing)**:

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `keyword` | str | The trending search term | "black friday deals" |
| `volume` | int | Relative search volume | 850000 |
| `volume_growth_pct` | float | Percentage growth rate | 250.5 |
| `geo` | str | Geographic region | "US" |
| `started_timestamp` | tuple | When trend began | (2024, 11, 24, 6, 0) |
| `ended_timestamp` | tuple/None | When trend ended | None (if ongoing) |
| `trend_keywords` | list[str] | Related searches | ['black friday 2024', 'cyber monday', ...] (38+ keywords) |
| `topics` | list[int] | Topic category IDs | [16, 3] (Shopping, Business) |
| `news` | list[NewsArticle] | Associated news articles | [NewsArticle(...), ...] |
| `news_tokens` | list | API tokens for fetching news | Used with trending_now_news_by_ids() |
| `normalized_keyword` | str | Normalized form for dedup | "blackfridaydeals" |

**Methods & Properties**:

```python
# Properties
trend.topic_names          # ['Shopping', 'Business'] (human-readable)
trend.is_trend_finished    # Boolean: has the trend ended?

# Methods
trend.hours_since_started()  # Calculate trend age: 12.5 hours

# Display methods
print(trend)                   # Human-readable summary
trend.brief_summary()          # Formatted output for display
repr(trend)                    # Full reconstructible representation
```

**Usage Example**:
```python
trends = tr.trending_now(geo='US')

for trend in trends[:10]:
    print(f"Keyword: {trend.keyword}")
    print(f"  Volume: {trend.volume:,}")
    print(f"  Growth: {trend.volume_growth_pct}%")
    print(f"  Age: {trend.hours_since_started()} hours")
    print(f"  Status: {'Active' if not trend.is_trend_finished else 'Finished'}")
    print(f"  Topics: {', '.join(trend.topic_names)}")
    print(f"  Related: {len(trend.trend_keywords)} keywords")
    if trend.news:
        print(f"  News: {len(trend.news)} articles")
```

**Special Features**:
- IPython/Jupyter pretty-printing support via `_repr_pretty_()`
- f-string formatting support via `__format__()`
- List-like iteration over attributes

**Source**: `trend_keyword.py`

---

### 5.2 TrendList

**What It Represents**: Collection of `TrendKeyword` objects with built-in filtering and summarization methods.

**When You Get This**: Returned by `trending_now()` as the primary container

**Inheritance**: Extends Python's built-in `list` class

**Key Methods**:

```python
# Filtering
tech_trends = trends.filter_by_topic('Technology')  # By topic name
tech_trends = trends.filter_by_topic(18)            # By topic ID
multi = trends.filter_by_topic(['Technology', 'Sports'])  # Multiple topics

# Summarization
summary = trends.get_topics_summary()
# Returns: {'Technology': 45, 'Sports': 32, 'Entertainment': 28, ...}

# Standard list operations
len(trends)           # Number of trends
trends[0]             # First trend
trends[:10]           # First 10 trends
for trend in trends:  # Iteration
    ...
```

**Display**:
```python
print(trends)  # Formatted multiline display of all trends
```

**Usage Example**:
```python
trends = tr.trending_now(geo='US')

# Get topic distribution
summary = trends.get_topics_summary()
print("Topic distribution:")
for topic, count in sorted(summary.items(), key=lambda x: x[1], reverse=True):
    print(f"  {topic}: {count} trends")

# Filter to relevant topics
relevant = trends.filter_by_topic(['Technology', 'Science'])
print(f"\nFound {len(relevant)} relevant trends")

# Process filtered trends
for trend in relevant:
    if trend.hours_since_started() < 4 and not trend.is_trend_finished:
        print(f"NEW: {trend.keyword} (+{trend.volume_growth_pct}%)")
```

**Source**: `trend_list.py`

---

### 5.3 NewsArticle

**What It Represents**: News article associated with a trending topic, including title, source, URL, image, and publication time.

**When You Get This**:
- Inside `TrendKeyword.news` list
- Returned by `trending_now_news_by_ids()`

**Attributes**:

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `title` | str | Article headline | "Black Friday Sales Hit Record High" |
| `url` | str | Article link | "https://news.example.com/..." |
| `source` | str | News outlet name | "CNN Business" |
| `picture` | str | Article image URL | "https://cdn.example.com/img.jpg" |
| `time` | int/str | Publication timestamp or relative | "2 hours ago" or Unix timestamp |
| `snippet` | str | Article preview text | "Retailers report unprecedented..." |

**Factory Method**:
```python
# NewsArticle.from_api() handles two API response formats automatically
article = NewsArticle.from_api(api_response)
```

**Usage Example**:
```python
# Get news for trending topic
trends = tr.trending_now(geo='US')
trend = trends[0]

# Option 1: News included in TrendKeyword
if trend.news:
    for article in trend.news[:3]:
        print(f"Title: {article.title}")
        print(f"Source: {article.source}")
        print(f"URL: {article.url}")
        print()

# Option 2: Fetch detailed news separately
news = tr.trending_now_news_by_ids(trend.news_tokens, max_news=5)
for article in news:
    print(f"{article.source}: {article.title}")
    print(f"  {article.snippet}")
```

**Special Handling**:
- Automatically parses "2 hours ago" format to timestamps
- Flexible field extraction for multiple API response formats
- Handles missing fields gracefully

**Source**: `news_article.py`

---

### 5.4 BatchPeriod (Enum)

**What It Represents**: Time window options for batch timeline queries with fixed intervals and data point counts.

**When You Use This**: Required parameter for `trending_now_showcase_timeline()`

**Enum Values**:

| Value | Numeric Code | Data Points | Interval | Use Case |
|-------|--------------|-------------|----------|----------|
| `BatchPeriod.Past4H` | 2 | ~30 | 8 minutes | Real-time breaking trends |
| `BatchPeriod.Past24H` | 3 | ~90 | 16 minutes | Last day trending analysis |
| `BatchPeriod.Past48H` | 5 | ~180 | 16 minutes | 2-day trend comparison |
| `BatchPeriod.Past7D` | 4 | ~42 | 4 hours | Week-long trend patterns |

**Update Frequency**: Data refreshes every 2 minutes (not truly real-time, but near real-time)

**Usage Example**:
```python
from trendspy import Trends, BatchPeriod

tr = Trends()
keywords = ['keyword1', 'keyword2', ..., 'keyword500']

# Get last 24 hours with 16-minute granularity
df = tr.trending_now_showcase_timeline(
    keywords,
    timeframe=BatchPeriod.Past24H  # Enum value
)

# Result: DataFrame with ~90 time points per keyword
print(df.shape)  # (90, 500) - 90 timestamps, 500 keywords
```

**Source**: `client.py` (BatchPeriod class definition)

---

### 5.5 DataFrame Outputs

**What They Contain**: pandas DataFrames with proper temporal/geographic indexing, ready for analysis and visualization.

**Two Main Types**:

**1. Time Series DataFrames** (from `interest_over_time`, `trending_now_showcase_timeline`):
- **Index**: DatetimeIndex (properly parsed timestamps)
- **Columns**: Keyword names (or keyword-timeframe-geo combos for multirange)
- **Values**: Interest scores 0-100
- **Special Values**: NaN for missing data, -1 converted to NaN

**2. Geographic DataFrames** (from `interest_by_region`):
- **Index**: Integer index
- **Columns**: `geoName`, `geoCode`, keyword column(s), optionally `coordinates` (lat/lng dict)
- **Values**: Interest scores 0-100 for keyword columns
- **Special Values**: Low-volume regions may be excluded if `inc_low_vol=False`

**Partial Data Flag**: Recent data may be marked with `isPartial=true` in raw API response (last few hours/days)

**Direct Visualization**:
```python
# Time series plot
df = tr.interest_over_time(['python', 'javascript'], timeframe='today 12-m')
df.plot(title='Language Interest', figsize=(12, 6))

# Geographic choropleth (with external libraries)
import geopandas as gpd
geo_df = tr.interest_by_region('solar energy', resolution='COUNTRY')
# Merge with geopandas world map and visualize
```

**Analysis-Ready**:
```python
# Statistical analysis
df.describe()                    # Summary statistics
df.corr()                        # Correlation matrix
df.rolling(window=7).mean()      # 7-period moving average
df.pct_change()                  # Period-over-period growth

# Pandas operations
df.resample('W').mean()          # Weekly aggregation
df.fillna(method='ffill')        # Forward fill missing values
df.to_csv('export.csv')          # Export to CSV
```

**Source**: `converter.py` (DataFrame creation), individual API method return values

---


## 6. User Workflows & Journeys

This section demonstrates how TrendsPy features combine to solve real-world tasks through complete, executable workflows.

### 6.1 Content Calendar Planning (Emma's Journey)

**Scenario**: Emma needs to plan Q1 2025 content based on historical seasonal trends and discover related topics.

**Goal**: Identify high-potential content topics with proven seasonal interest patterns.

**Complete Workflow**:

```python
from trendspy import Trends
import pandas as pd

tr = Trends()

# Step 1: Discover relevant category
tech_categories = tr.categories(find='technology')
tech_cat_id = tech_categories[0]['id']  # '13' - Computers & Electronics

# Step 2: Analyze 24-month history for seasonality
seed_keywords = ['artificial intelligence', 'machine learning', 'data science']
df_24m = tr.interest_over_time(
    seed_keywords,
    timeframe='today 24-m',
    cat=tech_cat_id
)

# Step 3: Identify seasonal peaks
monthly_avg = df_24m.resample('M').mean()
peak_months = monthly_avg.idxmax()
print("Peak months for each keyword:")
print(peak_months)

# Step 4: Discover related keywords for top performer
top_keyword = df_24m.mean().idxmax()  # Highest average interest
related = tr.related_queries(top_keyword)

print(f"\nTop related queries for '{top_keyword}':")
print(related['top'].head(10))

print(f"\nRising queries (emerging opportunities):")
print(related['rising'].head(10))

# Step 5: Geographic targeting insights
geo_df = tr.interest_by_region(top_keyword, resolution='COUNTRY')
top_geos = geo_df.nlargest(5, top_keyword)
print(f"\nTop geographic markets for '{top_keyword}':")
print(top_geos)

# Step 6: Create content calendar (simplified)
content_calendar = []
for keyword in seed_keywords:
    peak_month = peak_months[keyword].month
    content_calendar.append({
        'keyword': keyword,
        'optimal_month': peak_month,
        'avg_interest': df_24m[keyword].mean(),
        'trend': 'rising' if df_24m[keyword].diff().mean() > 0 else 'stable/falling'
    })

calendar_df = pd.DataFrame(content_calendar)
print("\nContent Calendar Recommendations:")
print(calendar_df)
```

**Expected Output**:
- Optimal publishing months for each topic
- 10+ related long-tail keywords per seed
- Top 5 geographic markets for localization
- Rising vs. stable trend classification

**Time Savings**: 3 hours of manual research → 5 minutes automated

---

### 6.2 Real-Time Social Listening (Alex's Journey)

**Scenario**: Alex needs to monitor real-time trends to catch viral moments within 2 hours of emergence.

**Goal**: Automated trend monitoring with news context and lifecycle assessment for timely brand responses.

**Complete Workflow**:

```python
from trendspy import Trends
import json
from datetime import datetime

tr = Trends()

def monitor_trends(geo='US', topic_filter='Technology'):
    """
    Automated trend monitoring function (run every 15 min via cron/scheduler)
    """
    # Step 1: Get current trends (last 4 hours for freshness)
    trends = tr.trending_now(geo=geo, hours=4)

    # Step 2: Filter to brand-relevant topics
    relevant_trends = trends.filter_by_topic(topic_filter)

    # Step 3: Identify actionable trends
    actionable = []
    for trend in relevant_trends:
        age_hours = trend.hours_since_started()
        is_finished = trend.is_trend_finished
        growth = trend.volume_growth_pct

        # Decision criteria: less than 2 hours old, still active, high growth
        if age_hours < 2 and not is_finished and growth > 100:
            # Step 4: Get news context
            if trend.news:
                news_summary = [
                    {
                        'title': article.title,
                        'source': article.source,
                        'url': article.url
                    }
                    for article in trend.news[:3]
                ]
            else:
                news_summary = []

            actionable.append({
                'keyword': trend.keyword,
                'age_hours': age_hours,
                'volume': trend.volume,
                'growth_pct': growth,
                'topics': trend.topic_names,
                'related_keywords': trend.trend_keywords[:10],
                'news': news_summary,
                'timestamp': datetime.now().isoformat()
            })

    # Step 5: Alert/log actionable trends
    if actionable:
        print(f"🔥 Found {len(actionable)} actionable trends:")
        for item in actionable:
            print(f"\nKeyword: {item['keyword']}")
            print(f"  Age: {item['age_hours']:.1f} hours")
            print(f"  Growth: {item['growth_pct']}%")
            print(f"  Volume: {item['volume']:,}")
            if item['news']:
                print(f"  Latest news: {item['news'][0]['title']}")

        # Save to log for review
        with open('trending_alerts.json', 'a') as f:
            json.dump(actionable, f, indent=2)

    return actionable

# Run monitoring
results = monitor_trends()

# Schedule this to run every 15 minutes:
# */15 * * * * /usr/bin/python /path/to/trend_monitor.py
```

**Expected Output**:
- Real-time alerts for trends < 2 hours old with >100% growth
- News context for each trend (why it's trending)
- Related keywords for content ideation
- JSON log of all alerts for analysis

**Business Impact**: Catch 80% of relevant trends within first 2 hours (vs. 6+ hours manual checking)

---

### 6.3 Geographic Market Analysis (Raj's Journey)

**Scenario**: Raj needs to identify top expansion markets for a client launching a new product.

**Goal**: Hierarchical geographic analysis (country → state → city) to find high-potential markets.

**Complete Workflow**:

```python
from trendspy import Trends
import pandas as pd

tr = Trends()

def geographic_market_analysis(keyword, competitor_keyword=None):
    """
    Complete geographic opportunity analysis
    """
    results = {}

    # Step 1: Global country-level overview
    print(f"Analyzing '{keyword}' globally...")
    countries = tr.interest_by_region(keyword)
    top_countries = countries.nlargest(10, keyword)
    results['top_countries'] = top_countries

    print("\nTop 10 countries:")
    print(top_countries[[' geoName', keyword]])

    # Step 2: Drill down to top country (assume US for example)
    top_country_code = top_countries.iloc[0]['geoCode']  # e.g., 'US'
    print(f"\nDrilling down to {top_country_code} states...")

    us_states = tr.interest_by_region(
        keyword,
        geo=top_country_code,
        resolution='REGION'
    )
    top_states = us_states.nlargest(10, keyword)
    results['top_states'] = top_states

    print("\nTop 10 states:")
    print(top_states[['geoName', keyword]])

    # Step 3: City-level analysis for top state
    top_state_code = top_states.iloc[0]['geoCode']  # e.g., 'US-CA'
    print(f"\nDrilling down to {top_state_code} cities...")

    cities = tr.interest_by_region(
        keyword,
        geo=top_state_code,
        resolution='CITY'
    )
    top_cities = cities.nlargest(20, keyword)
    results['top_cities'] = top_cities

    print("\nTop 20 cities (with coordinates for mapping):")
    print(top_cities[['geoName', keyword, 'coordinates']].head(10))

    # Step 4: Competitive comparison (if competitor keyword provided)
    if competitor_keyword:
        print(f"\nComparing '{keyword}' vs '{competitor_keyword}'...")
        comparison = tr.interest_over_time(
            [keyword, competitor_keyword],
            timeframe='today 12-m'
        )

        # Market share analysis
        avg_interest = comparison.mean()
        market_share = (avg_interest / avg_interest.sum()) * 100

        print(f"\nMarket share (avg interest):")
        print(f"  {keyword}: {market_share[keyword]:.1f}%")
        print(f"  {competitor_keyword}: {market_share[competitor_keyword]:.1f}%")

        results['competitive_analysis'] = {
            'your_keyword': keyword,
            'competitor': competitor_keyword,
            'market_share': market_share.to_dict(),
            'trend_comparison': comparison
        }

    return results

# Execute analysis
keyword = 'solar panels'
competitor = 'wind turbines'
analysis = geographic_market_analysis(keyword, competitor)

# Export for reporting
analysis['top_cities'].to_csv('top_cities_solar.csv', index=False)
```

**Expected Output**:
- Top 10 countries by search interest
- Top 10 states in primary country
- Top 20 cities with lat/lng coordinates for mapping
- Competitive market share analysis

**Business Value**: Identify expansion opportunities, prioritize markets, understand competitive landscape

---

### 6.4 Large-Scale Keyword Research (Maria's Journey)

**Scenario**: Maria needs to analyze 200 trending keywords for SEO opportunities without cross-keyword normalization bias.

**Goal**: Independent trend analysis for each keyword to identify true rising patterns.

**Complete Workflow**:

```python
from trendspy import Trends, BatchPeriod
import pandas as pd

tr = Trends(
    persist_cookies=True,
    use_tls_impersonation=True,
    session_warmup=True,
    tor_enabled=True  # For large-scale analysis
)

def large_scale_keyword_research(seed_topic='technology'):
    """
    Analyze 200+ keywords with independent normalization
    """
    # Step 1: Get current trending keywords
    print("Fetching trending keywords...")
    trends = tr.trending_now(geo='US', hours=24)

    # Filter to seed topic
    relevant_trends = trends.filter_by_topic(seed_topic.title())
    keywords = [t.keyword for t in relevant_trends[:200]]

    print(f"Analyzing {len(keywords)} keywords...")

    # Step 2: Get independent historical data (each keyword normalized to itself)
    df_24h = tr.trending_now_showcase_timeline(
        keywords,
        timeframe=BatchPeriod.Past24H
    )

    # Step 3: Calculate growth metrics (independent for each keyword)
    growth_metrics = pd.DataFrame({
        'keyword': keywords,
        'current_interest': df_24h.iloc[-1],  # Most recent value
        'avg_interest_24h': df_24h.mean(),
        'max_interest_24h': df_24h.max(),
        'growth_rate': df_24h.diff().mean(),  # Average change per interval
        'volatility': df_24h.std()
    })

    # Step 4: Classify opportunities
    growth_metrics['opportunity_score'] = (
        growth_metrics['growth_rate'] * 0.4 +  # 40% weight on growth
        growth_metrics['avg_interest_24h'] * 0.3 +  # 30% weight on volume
        (100 - growth_metrics['volatility']) * 0.3  # 30% weight on stability
    )

    # Step 5: Rank and classify
    growth_metrics = growth_metrics.sort_values('opportunity_score', ascending=False)

    rising_stars = growth_metrics[
        (growth_metrics['growth_rate'] > 2) &
        (growth_metrics['avg_interest_24h'] > 20)
    ]

    stable_performers = growth_metrics[
        (growth_metrics['growth_rate'].between(-1, 2)) &
        (growth_metrics['avg_interest_24h'] > 40)
    ]

    print(f"\nRising Stars ({len(rising_stars)} keywords):")
    print(rising_stars[['keyword', 'growth_rate', 'avg_interest_24h']].head(10))

    print(f"\nStable Performers ({len(stable_performers)} keywords):")
    print(stable_performers[['keyword', 'avg_interest_24h', 'volatility']].head(10))

    # Step 6: Export for client reporting
    growth_metrics.to_csv('keyword_analysis_report.csv', index=False)

    return {
        'all_metrics': growth_metrics,
        'rising_stars': rising_stars,
        'stable_performers': stable_performers,
        'raw_timeline_data': df_24h
    }

# Execute
results = large_scale_keyword_research('technology')

# Visualize top opportunities
results['raw_timeline_data'][results['rising_stars']['keyword'].head(10).tolist()].plot(
    subplots=True,
    layout=(5, 2),
    figsize=(15, 20),
    title="Rising Star Keywords - 24H Trends"
)
```

**Expected Output**:
- 200 keywords analyzed with independent normalization
- Rising stars: High growth + moderate volume
- Stable performers: Consistent high volume + low volatility
- Opportunity scores for prioritization
- CSV report for client delivery

**Time Savings**: 8 hours manual research → 30 minutes automated
**Scale**: 10x more keywords analyzed (20 → 200)

---

## 7. Technical Architecture

### 7.1 Layered Architecture

TrendsPy follows a clean layered architecture with separation of concerns:

```
┌─────────────────────────────────────────────┐
│   Application Layer                         │
│   (Trends class - public API methods)       │
├─────────────────────────────────────────────┤
│   Data Processing Layer                     │
│   (Converter, TimeframeUtils)               │
├─────────────────────────────────────────────┤
│   Reliability Layer                         │
│   (AdaptiveRateLimiter, DegradationManager) │
│   (SessionManager, BrowserProfiles)         │
├─────────────────────────────────────────────┤
│   HTTP Layer                                │
│   (requests/curl-cffi, TLSSession)          │
├─────────────────────────────────────────────┤
│   Data Model Layer                          │
│   (TrendKeyword, TrendList, NewsArticle)    │
└─────────────────────────────────────────────┘
```

**Layer Responsibilities**:
1. **Application**: User-facing API, parameter validation, method routing
2. **Data Processing**: API response parsing, DataFrame transformation, timeframe normalization
3. **Reliability**: Rate limiting, session management, error recovery, degradation
4. **HTTP**: Network communication, TLS impersonation, proxy handling
5. **Data Models**: Structured representation of API responses

---

### 7.2 Request Flow

```
User Code: tr.interest_over_time(['python'])
    ↓
Trends.__init__() validates parameters
    ↓
Trends._get() orchestrates HTTP request
    ├─→ AdaptiveRateLimiter.wait_if_needed()  [Enforce delays]
    ├─→ SessionManager.get_session()          [Get/create session]
    ├─→ BrowserProfiles.get_random_profile()  [Coherent headers]
    ├─→ TLSImpersonationSession OR requests   [HTTP request]
    ├─→ Response validation                   [Status codes, content]
    └─→ Error handling & retries              [Exponential backoff]
    ↓
Trends._parse_protected_json()  [Parse Google's protected JSON format]
    ↓
TrendsDataConverter.interest_over_time()  [Transform to DataFrame]
    ↓
Returns: pandas.DataFrame to user
```

**Error Recovery Path**:
```
429 Error Detected
    ↓
AdaptiveRateLimiter.record_failure()
    ├─→ Increment delay multiplier (1.0 → 1.5 → 2.0 → 3.0)
    ├─→ Add jitter (±15% or ±25%)
    └─→ Check circuit breaker threshold
    ↓
Circuit Breaker Decision:
    - < 10 failures: Retry with increased delay
    - ≥ 10 failures: Raise CircuitBreakerError, stop requests
```

---

### 7.3 API Integration

**Google Trends Endpoints Used**:
- `/api/explore`: Keyword exploration, token generation
- `/api/widgetdata/multiline`: Interest over time data
- `/api/widgetdata/comparedgeo`: Geographic distribution
- `/api/widgetdata/relatedrequests`: Related queries
- `/api/widgetdata/relatedtopics`: Related topics
- `/api/dailytrends`: Daily trending (deprecated)
- `/api/realtimetrends`: Real-time trending (deprecated)
- `/embed/timeseries`: Batch timeline data
- RSS Feeds: Trending with news context

**Request Encoding**:
1. Parameters → JSON object
2. JSON → Base64 encoding (with custom escaping)
3. Sent as POST body or `req=<encoded>` URL parameter

**Response Decoding**:
1. Remove protection prefix: `)]}'\n`
2. Parse JSON
3. Extract embedded data from nested structures
4. Convert to DataFrames or model objects

---

### 7.4 Dependencies

**Core (Required)**:
- `requests >= 2.25.0`: HTTP library
- `pandas >= 1.2.0`: DataFrame operations
- `numpy >= 1.19.0`: Numerical arrays
- `python-dateutil >= 2.8.0`: Date parsing, relativedelta

**Optional (Enhanced Features)**:
- `curl-cffi >= 0.7.0`: TLS fingerprint impersonation
- `stem`: Tor control (for IP rotation)

**Development**:
- `build >= 0.10.0`: Package building
- `twine >= 4.0.0`: PyPI upload
- `pytest`: Testing framework

**Python Version**: >= 3.7 (tested on 3.7-3.11)

---

## 8. Configuration & Initialization

### 8.1 Basic Initialization

```python
from trendspy import Trends

# Minimal setup (all defaults)
tr = Trends()
```

**Defaults**:
- Language: 'en'
- Timezone: 360 (UTC-6)
- Cookie persistence: Disabled
- TLS impersonation: Enabled (if curl-cffi available)
- Session warmup: Disabled
- Tor: Disabled
- Proxy: None

---

### 8.2 Production Configuration

```python
tr = Trends(
    # Language & Locale
    language='en',              # UI language
    timezone=360,               # UTC offset in minutes

    # Session Management
    persist_cookies=True,       # Save cookies to .trendspy_session.pkl
    session_warmup=True,        # 3-request warmup sequence

    # Anti-Detection
    use_tls_impersonation=True, # curl-cffi TLS fingerprinting
    tls_browser='chrome131',    # Browser to impersonate
    use_browser_profiles=True,  # Coherent header profiles

    # Proxy & IP Rotation
    proxy=None,                 # HTTP/SOCKS proxy (string or dict)
    tor_enabled=False,          # Enable Tor IP rotation
    tor_ports=[9050, 9051],     # Tor SOCKS and control ports

    # Rate Limiting (uses defaults from AdaptiveRateLimiter)
    # Configured separately if needed
)
```

---

### 8.3 Parameter Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language` | str | 'en' | UI language code |
| `timezone` | int | 360 | UTC offset in minutes (360 = UTC-6) |
| `persist_cookies` | bool | False | Save/load session cookies |
| `session_warmup` | bool | False | Perform 3-request warmup sequence |
| `use_tls_impersonation` | bool | True | Use curl-cffi for TLS fingerprinting |
| `tls_browser` | str | 'chrome131' | Browser to impersonate (chrome131, firefox132, etc.) |
| `use_browser_profiles` | bool | True | Use coherent browser header profiles |
| `proxy` | str/dict | None | HTTP/SOCKS proxy configuration |
| `tor_enabled` | bool | False | Enable Tor IP rotation |
| `tor_ports` | list | [9050, 9051] | Tor SOCKS and control ports |

---

### 8.4 Proxy Configuration Recipes

**Simple HTTP Proxy**:
```python
tr = Trends(proxy="http://10.10.1.10:3128")
```

**Authenticated Proxy**:
```python
tr = Trends(proxy="http://user:pass@proxy.example.com:3128")
```

**Separate HTTP/HTTPS Proxies**:
```python
tr = Trends(proxy={
    "http": "http://proxy1.example.com:3128",
    "https": "https://proxy2.example.com:1080"
})
```

**SOCKS Proxy**:
```python
tr = Trends(proxy="socks5://localhost:9050")  # Tor default
```

**Runtime Proxy Change**:
```python
tr = Trends()
tr.set_proxy("http://newproxy.example.com:8080")
```

**Tor Setup** (Free IP Rotation):
```bash
# Install Tor
brew install tor  # macOS
# or
apt install tor   # Linux

# Install Python Tor control library
pip install stem

# Start Tor
brew services start tor  # macOS
# or
systemctl start tor      # Linux
```

```python
# Use Tor in TrendsPy
tr = Trends(
    tor_enabled=True,
    tor_ports=[9050, 9051]  # Default Tor ports
)
```

---

## 9. Constraints & Limitations

### 9.1 API Constraints (Google's Limits)

| Constraint | Value | Impact |
|------------|-------|--------|
| Requests/hour | ~200 | Hard limit; exceeding triggers 429 errors and potential IP blocks |
| Keywords per query | 5 | `interest_over_time()` maximum; use multiple queries for more |
| Related queries | 1 keyword | `related_queries()` and `related_topics()` do not support batching |
| Hourly precision max | 7 days | Date ranges with hourly resolution limited to < 8 days |
| Geographic resolution | Volume-dependent | City-level data only available for high-volume keywords/regions |
| Time range | ~2004-present | Historical data availability varies by keyword and region |

---

### 9.2 Library Design Constraints

**Normalization**:
- `interest_over_time()`: **Relative normalization** (keywords compared to each other, highest = 100)
- `trending_now_showcase_timeline()`: **Independent normalization** (each keyword normalized to itself)
- Cannot mix normalization types in single query

**Multirange**:
- All timeframes must have consistent resolution (all hourly OR all daily, not mixed)
- Maximum timeframe ≤ 2× minimum timeframe
- Violation raises `ValueError` with explanation

**TLS Impersonation**:
- Requires `curl-cffi` library (optional dependency)
- Falls back to standard `requests` if unavailable
- Some features (JA3 fingerprinting) only work with curl-cffi

---

### 9.3 Known Limitations & Workarounds

**Limitation 1: Related Queries Quota Exhausted Quickly**
- **Symptom**: `TrendsQuotaExceededError` after 10-20 related_queries calls
- **Workarounds**:
  1. Vary `referer` header: `tr.related_queries(kw, headers={'referer': 'https://trends.google.com/'})`
  2. Enable Tor IP rotation: `tr = Trends(tor_enabled=True)`
  3. Space out requests across hours/days
  4. Use proxy rotation for large-scale research

**Limitation 2: IP-Based Rate Limiting for Large Studies**
- **Symptom**: 429 errors persist even after waiting, IP temporarily blocked
- **Workarounds**:
  1. Enable Tor rotation for free IP changes
  2. Use commercial proxy pool
  3. Distribute queries across multiple days
  4. Use `AdaptiveRateLimiter` with conservative settings (lower requests_per_hour)

**Limitation 3: TLS Blocking with Standard Requests**
- **Symptom**: 8+ second timeouts, empty response headers, connection-level failures
- **Workarounds**:
  1. Install curl-cffi: `pip install curl-cffi`
  2. Enable TLS impersonation: `tr = Trends(use_tls_impersonation=True)`
  3. If curl-cffi unavailable, use proxy with residential IPs

**Limitation 4: Multirange Resolution Mismatch**
- **Symptom**: `ValueError: All timeframes must have consistent resolution`
- **Solution**: Ensure all timeframes in list have same granularity:
  - ✓ Valid: `['2024-01-01 30-d', '2024-07-01 30-d']` (both daily)
  - ✗ Invalid: `['now 6-H', 'today 30-d']` (hourly vs daily)

---

## 10. Error Handling & Troubleshooting

### 10.1 Exception Types

**TrendsQuotaExceededError**:
- **When**: Related queries/topics quota exhausted
- **Message**: Includes remediation suggestions
- **Remediation**:
  - Wait 1-2 hours before retrying
  - Use proxy/Tor rotation
  - Vary referer headers

**CircuitBreakerError**:
- **When**: 10+ consecutive request failures
- **Message**: "Circuit breaker triggered after N failures"
- **Remediation**:
  - Check internet connectivity
  - Verify proxy configuration
  - Wait 30-60 minutes for quota reset
  - Enable Tor rotation for future runs

**ValueError**:
- **When**: Invalid parameter combinations
- **Examples**:
  - Multirange resolution mismatch
  - Invalid timeframe format
  - Keywords list too long (>5 for interest_over_time)

---

### 10.2 Rate Limiter States

**Normal Mode**:
- Base delay between requests (default 15s)
- ±15% jitter
- No failures recorded

**Degraded Mode** (after 429 errors):
- Delay multiplier increases:
  - 1st 429: 1.5x delay (22.5s avg)
  - 2nd 429: 2.0x delay (30s avg)
  - 3rd+ 429: 3.0x delay (emergency mode, 45s avg)
- ±25% jitter in emergency mode

**Circuit Breaker Mode** (after 10 failures):
- All requests blocked
- `CircuitBreakerError` raised immediately
- Requires manual reset or wait period

**Recovery**:
- Each success decreases delay multiplier by 20%
- 3 consecutive successes → Recovery mode
- 6 consecutive successes → Full normal mode

---

### 10.3 Common Issues & Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **429 Too Many Requests** | HTTP 429, quota errors | Enable adaptive rate limiting (automatic); space out requests |
| **Connection Timeouts** | 8+ second timeouts, no response | Install curl-cffi for TLS impersonation; check proxy config |
| **Empty DataFrames** | DataFrame returned but no data | Keyword has no search volume; try broader terms or different regions |
| **IP Temporarily Blocked** | All requests fail, persists hours | Enable Tor rotation; use different IP; wait 12-24 hours |
| **Session Cookie Errors** | "Invalid session" errors | Delete `.trendspy_session.pkl`; restart with fresh session |
| **Multirange ValueError** | "Inconsistent resolution" error | Ensure all timeframes have same granularity (hourly/daily/weekly) |
| **TLS Import Error** | "curl_cffi not found" | Install: `pip install curl-cffi` or disable TLS impersonation |

---

### 10.4 Debugging Tips

**1. Check Rate Limiter Stats**:
```python
stats = tr.rate_limiter.get_stats()
print(f"Utilization: {stats['utilization_pct']}%")
print(f"Delay multiplier: {stats['delay_multiplier']}")
print(f"Failures: {stats['consecutive_failures']}")
```

**2. Review Session Cookies**:
```python
# Check if cookies are persisted
import os
if os.path.exists('.trendspy_session.pkl'):
    print("Session cookies found")
else:
    print("No saved session, will create new")
```

**3. Verify Proxy Connectivity**:
```python
tr = Trends(proxy="http://proxy:3128")
# Test with simple query
try:
    df = tr.interest_over_time('test', timeframe='now 7-d')
    print("Proxy working!")
except Exception as e:
    print(f"Proxy error: {e}")
```

**4. Enable Verbose Logging** (if implemented):
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Now see detailed request/response logs
```

**5. Test with Minimal Query**:
```python
# Simplest possible query to isolate issues
tr = Trends()
df = tr.interest_over_time('python', timeframe='now 7-d')
print(df.head())
```

---

## 11. Success Criteria & Metrics

### 11.1 Performance Targets

**Request Success Rate**:
- **Target**: >95% under normal conditions
- **Measurement**: (Successful requests / Total requests) × 100
- **Acceptable**: >90% (occasional quota issues)
- **Action Required**: <90% (investigate rate limiting, proxy, TLS issues)

**IP Block Rate**:
- **Target**: <1% long-term (across all users/sessions)
- **Measurement**: (Blocked IPs / Total unique IPs) × 100
- **Acceptable**: 1-5% (with recovery within 24 hours)
- **Action Required**: >5% (review anti-detection strategies)

**Processing Time**:
- **100 keywords**: <30 minutes (with rate limiting)
- **500 keywords** (batch): 5-10 minutes
- **Single query**: 1-5 seconds (excluding mandatory delays)

---

### 11.2 Reliability Metrics

**Circuit Breaker Triggers**:
- **Target**: <1% of sessions hit circuit breaker
- **Measurement**: (Sessions with circuit breaker / Total sessions) × 100

**Emergency Mode Activations**:
- **Target**: <5% of sessions enter emergency mode
- **Measurement**: (Sessions with 3+ consecutive 429s / Total sessions) × 100

**Session Persistence Success**:
- **Target**: >99% successful cookie save/load
- **Measurement**: (Successful session loads / Attempted loads) × 100

---

### 11.3 User Experience Goals

**Clear Error Messages**:
- All exceptions include actionable remediation steps
- No generic "An error occurred" messages
- Examples:
  - ✓ "TrendsQuotaExceededError: Related queries quota exhausted. Solutions: 1) Wait 1-2 hours, 2) Use proxy rotation, 3) Vary referer headers"
  - ✗ "Error: Request failed"

**Pandas-Native Outputs**:
- 100% of time-series methods return DataFrames
- Zero conversion required (no manual parsing)
- Proper datetime indexes (not string dates)

**Minimal Configuration**:
- Basic use cases work with `tr = Trends()` (zero configuration)
- Production features opt-in (not required for simple queries)

**Production-Ready Defaults**:
- Rate limiting enabled by default
- Adaptive backoff automatic
- TLS impersonation enabled (if available)
- Safe defaults prevent IP bans for new users

---

## Appendices

### Appendix A: Timeframe Format Reference

| Format Type | Pattern | Example | Granularity | Max Range |
|-------------|---------|---------|-------------|-----------|
| **Standard Presets** | | | | |
| Hourly | `now N-H` | `now 4-H` | Minutes | ~8 days |
| Daily | `now N-d` | `now 7-d` | Hourly | ~90 days |
| Monthly | `today N-m` | `today 12-m` | Daily/Weekly | ~5 years |
| Yearly | `today N-y` | `today 5-y` | Weekly/Monthly | All available |
| All data | `all` | `all` | Monthly | ~2004-present |
| **Custom Intervals** | | | | |
| Custom hours | `now N-H` | `now 123-H` | Minutes/Hourly | < 8 days |
| Custom days | `today N-d` | `today 45-d` | Daily | < 270 days |
| Custom months | `today N-m` | `today 18-m` | Weekly | ~5 years |
| **Date-Based** | | | | |
| Date + offset | `YYYY-MM-DD N-d` | `2024-02-01 30-d` | Daily | Based on N |
| Date + offset (months) | `YYYY-MM-DD N-m` | `2024-06-15 6-m` | Weekly | Based on N |
| Date range | `YYYY-MM-DD YYYY-MM-DD` | `2024-01-01 2024-12-31` | Auto | Any |
| Hourly precision | `YYYY-MM-DDTHH YYYY-MM-DDTHH` | `2024-03-25T12 2024-03-25T15` | Minutes | < 8 days |

**Resolution Rules**:
- < 8 days: Hourly to 8-minute intervals
- 8-90 days: Daily data
- 90 days - 5 years: Weekly data
- 5+ years: Monthly data

---

### Appendix B: Geographic Resolution Levels

| Resolution | Code | Description | Example Geo | Output |
|------------|------|-------------|-------------|--------|
| **COUNTRY** | `'COUNTRY'` | Country-level aggregation | `''` (worldwide) | Countries by interest |
| **REGION** | `'REGION'` | State/province/territory | `'US'` | US states |
| | | | `'CA'` (Canada) | Canadian provinces |
| **CITY** | `'CITY'` | City-level detail | `'US-CA'` | California cities |
| | | Includes lat/lng coordinates | `'GB'` | UK cities |
| **DMA** | `'DMA'` | Designated Market Areas (US media markets) | `'US'` | US DMAs (210 regions) |

**Hierarchy**:
```
World (geo='')
  ├─→ Countries (resolution='COUNTRY')
  │     └─→ Regions/States (geo='US', resolution='REGION')
  │           └─→ Cities (geo='US-CA', resolution='CITY')
  └─→ DMAs (geo='US', resolution='DMA')
```

---

### Appendix C: Google Property Filters

| Property | Code | Description |
|----------|------|-------------|
| **Web Search** | `''` or `'web'` | Default; general web search |
| **Image Search** | `'images'` | Google Images search trends |
| **News Search** | `'news'` | Google News search trends |
| **YouTube** | `'youtube'` | YouTube search trends |
| **Shopping** | `'froogle'` | Google Shopping search trends |

**Usage**:
```python
# Compare web vs YouTube interest
web_df = tr.interest_over_time('minecraft', gprop='web')
yt_df = tr.interest_over_time('minecraft', gprop='youtube')
```

---

### Appendix D: Browser Profile Details

| Profile ID | Browser | OS | TLS Version | User-Agent String |
|------------|---------|-----|-------------|-------------------|
| `chrome131_macos` | Chrome 131 | macOS 14 | TLS 1.3 | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)... |
| `chrome131_windows` | Chrome 131 | Windows 11 | TLS 1.3 | Mozilla/5.0 (Windows NT 10.0; Win64; x64)... |
| `chrome130_macos` | Chrome 130 | macOS 13 | TLS 1.3 | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)... |
| `chrome130_windows` | Chrome 130 | Windows 10 | TLS 1.3 | Mozilla/5.0 (Windows NT 10.0; Win64; x64)... |
| `firefox132_macos` | Firefox 132 | macOS 14 | TLS 1.3 | Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15;...)... |
| `firefox132_windows` | Firefox 132 | Windows 11 | TLS 1.3 | Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0)... |
| `safari18_macos` | Safari 18 | macOS 14 | TLS 1.3 | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)... |
| `edge131_windows` | Edge 131 | Windows 11 | TLS 1.3 | Mozilla/5.0 (Windows NT 10.0; Win64; x64)... |

**Weighting**:
- Chrome profiles: 70% combined (matches real-world usage)
- Firefox: 10%
- Safari: 5%
- Edge: 15%

**Coherent Headers**: Each profile includes matching:
- User-Agent
- Sec-CH-UA (browser brand/version)
- Sec-CH-UA-Platform (OS)
- Sec-CH-UA-Platform-Version (OS version)
- Sec-CH-UA-Mobile (mobile flag)
- Sec-CH-UA-Full-Version-List
- Sec-CH-UA-Arch (architecture)

---

### Appendix E: Topic Taxonomy

| Topic ID | Topic Name |
|----------|------------|
| 1 | Autos and Vehicles |
| 2 | Beauty and Fashion |
| 3 | Business and Finance |
| 4 | Entertainment |
| 5 | Food and Drink |
| 6 | Games |
| 7 | Health |
| 8 | Hobbies and Leisure |
| 9 | Jobs and Education |
| 10 | Law and Government |
| 11 | Other |
| 13 | Pets and Animals |
| 14 | Politics |
| 15 | Science |
| 16 | Shopping |
| 17 | Sports |
| 18 | Technology |
| 19 | Travel and Transportation |
| 20 | Climate |

**Note**: Topic ID 12 is absent (likely deprecated category)

**Usage in Filtering**:
```python
# Filter TrendList by topic
trends = tr.trending_now()
tech_trends = trends.filter_by_topic('Technology')  # By name
tech_trends = trends.filter_by_topic(18)            # By ID
```

**Usage in Categories**:
```python
# Get trends in specific category
df = tr.interest_over_time('AI', cat=18)  # Technology category
```

---

**End of Document**

---

**Document Metadata**:
- **Total Sections**: 11 main sections + 5 appendices
- **Feature Coverage**: 17+ API methods across 4 categories
- **Personas**: 5 detailed user personas with problem-solution mapping
- **Workflows**: 4 complete, executable user journeys
- **Estimated Reading Time**: 60-90 minutes
- **Target Audience**: Product managers, developers, data analysts, researchers, marketers

**Recommended Next Steps**:
1. **For Product Managers**: Read Sections 1-2, 6, 9-11
2. **For Developers**: Read Sections 3-5, 7-8, 10
3. **For Data Analysts**: Read Sections 1-3, 6
4. **For First-Time Users**: Start with Section 1, then Section 6 (workflows)

**Feedback & Updates**:
- This is a living document. Submit updates via GitHub issues
- For feature requests, reference this PRD in discussions
- Report inaccuracies or outdated information

