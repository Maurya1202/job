import streamlit as st
import requests, re, time
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(
    page_title="DataJobs India",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 40%, #06b6d4 100%);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px;
    color: white; position: relative; overflow: hidden;
}
.hero::after {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px; background: rgba(255,255,255,0.06); border-radius: 50%;
}
.hero h1 { font-size: 26px; font-weight: 800; margin: 0 0 4px; letter-spacing: -0.5px; }
.hero p  { font-size: 13px; opacity: 0.85; margin: 0; }
.hero .chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.chip {
    background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px; padding: 3px 11px; font-size: 11px; font-weight: 500; color: white;
}

.stats-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 20px; }
.stat-card {
    background: white; border-radius: 14px; padding: 16px;
    border: 1px solid #f0f0f0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: transform 0.2s, box-shadow 0.2s; text-align: center;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
.stat-icon  { font-size: 22px; margin-bottom: 4px; }
.stat-value { font-size: 28px; font-weight: 800; color: #1e1b4b; line-height: 1; }
.stat-label { font-size: 11px; color: #9ca3af; font-weight: 500; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }

.job-card {
    background: white; border-radius: 14px; padding: 18px 22px; margin-bottom: 12px;
    border: 1px solid #f0f0f0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    position: relative; overflow: hidden;
}
.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(99,102,241,0.12);
    border-color: #c7d2fe;
}
.job-card::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px; border-radius: 4px 0 0 4px;
}

.card-naukri::before      { background: linear-gradient(180deg, #f97316, #fb923c); }
.card-linkedin::before    { background: linear-gradient(180deg, #0077b5, #0ea5e9); }
.card-indeed::before      { background: linear-gradient(180deg, #2557a7, #3b82f6); }
.card-internshala::before { background: linear-gradient(180deg, #11a9b5, #06b6d4); }
.card-shine::before       { background: linear-gradient(180deg, #7c3aed, #8b5cf6); }
.card-foundit::before     { background: linear-gradient(180deg, #dc2626, #ef4444); }
.card-timesjobs::before   { background: linear-gradient(180deg, #d97706, #f59e0b); }
.card-glassdoor::before   { background: linear-gradient(180deg, #0caa41, #34d058); }
.card-wellfound::before   { background: linear-gradient(180deg, #f43f5e, #fb7185); }
.card-instahyre::before   { background: linear-gradient(180deg, #7c3aed, #a78bfa); }
.card-hirist::before      { background: linear-gradient(180deg, #0891b2, #22d3ee); }
.card-monster::before     { background: linear-gradient(180deg, #7f1d1d, #ef4444); }
.card-cutshort::before    { background: linear-gradient(180deg, #ea580c, #fb923c); }
.card-default::before     { background: linear-gradient(180deg, #6366f1, #8b5cf6); }

.job-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
.job-title  { font-size: 15px; font-weight: 700; color: #1e1b4b; margin-bottom: 2px; line-height: 1.3; }
.job-company { font-size: 13px; color: #6b7280; font-weight: 500; }

.apply-btn {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white !important; padding: 7px 16px; border-radius: 8px;
    font-size: 12px; font-weight: 600; text-decoration: none;
    white-space: nowrap; transition: opacity 0.2s, transform 0.15s; display: inline-block;
}
.apply-btn:hover { opacity: 0.9; transform: scale(1.03); }

.badges { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0 6px; }
.badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }

.badge-portal-naukri      { background: #fff7ed; color: #c2410c; }
.badge-portal-linkedin    { background: #eff6ff; color: #1d4ed8; }
.badge-portal-indeed      { background: #eef2ff; color: #3730a3; }
.badge-portal-internshala { background: #ecfeff; color: #0e7490; }
.badge-portal-shine       { background: #f5f3ff; color: #6d28d9; }
.badge-portal-foundit     { background: #fef2f2; color: #b91c1c; }
.badge-portal-timesjobs   { background: #fffbeb; color: #b45309; }
.badge-portal-glassdoor   { background: #f0fdf4; color: #166534; }
.badge-portal-wellfound   { background: #fff1f2; color: #be123c; }
.badge-portal-instahyre   { background: #f5f3ff; color: #5b21b6; }
.badge-portal-hirist      { background: #ecfeff; color: #0e7490; }
.badge-portal-monster     { background: #fef2f2; color: #991b1b; }
.badge-portal-cutshort    { background: #fff7ed; color: #c2410c; }
.badge-portal-default     { background: #f0fdf4; color: #15803d; }

.badge-loc   { background: #f0fdf4; color: #166534; }
.badge-exp   { background: #eff6ff; color: #1e40af; }
.badge-mode  { background: #fdf4ff; color: #7e22ce; }
.badge-sal   { background: #fff7ed; color: #9a3412; }
.badge-days  { background: #f1f5f9; color: #334155; }

.skills-row { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
.skill {
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px;
    padding: 2px 8px; font-size: 11px; color: #475569; font-weight: 500;
}
.snippet { font-size: 12px; color: #6b7280; line-height: 1.6; margin-top: 8px; }

.portal-section { display: flex; align-items: center; gap: 10px; margin: 24px 0 12px; }
.portal-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
.portal-title { font-size: 13px; font-weight: 700; color: #374151; text-transform: uppercase; letter-spacing: 0.8px; }
.portal-count { background: #f3f4f6; color: #6b7280; border-radius: 20px; padding: 2px 9px; font-size: 11px; font-weight: 600; }

.empty { text-align: center; padding: 48px 24px; background: white; border-radius: 14px; border: 1px dashed #e0e0e0; }
.empty-icon  { font-size: 52px; margin-bottom: 12px; }
.empty-title { font-size: 16px; font-weight: 600; color: #374151; margin-bottom: 6px; }
.empty-sub   { font-size: 13px; color: #9ca3af; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%) !important;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stSelectbox > div,
section[data-testid="stSidebar"] .stCheckbox { filter: brightness(1.1); }

.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4) !important; border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════
ROLES = [
    # Data & Analytics
    "Data Analyst",
    "Data Scientist",
    "Data Engineer",
    "BI Analyst",
    "Business Analyst",
    # Developer
    "Python Developer",
    "SQL Developer",
    "Power BI Developer",
    # Machine Learning / AI
    "ML Engineer",
    "AI Engineer",
    "NLP Engineer",
    # Specialised
    "ETL Developer",
    "Database Administrator",
    "Analytics Engineer",
    "Tableau Developer",
]

CITIES = [
    "Mumbai", "Bangalore", "Delhi NCR", "Hyderabad", "Pune",
    "Chennai", "Noida", "Gurgaon", "Kolkata", "Ahmedabad",
    "Jaipur", "Kochi", "Chandigarh", "Remote",
]

EXP = ["Fresher (0–1 year)", "1–3 years", "3–5 years", "5+ years"]

# Days filter options  →  (label, DuckDuckGo timelimit code)
DAYS_OPTIONS = {
    "Last 1 day":   "d",
    "Last 3 days":  "d3",   # will be handled manually
    "Last 7 days":  "w",
    "Last 14 days": "w2",   # will be handled manually
    "Last 30 days": "m",
    "All time":     None,
}

WORK_MODES = ["Any", "Remote", "Hybrid", "On-site / Office"]

PORTAL_COLORS = {
    # Original 7
    "Naukri":      "#f97316",
    "LinkedIn":    "#0077b5",
    "Indeed":      "#2557a7",
    "Internshala": "#11a9b5",
    "Shine":       "#7c3aed",
    "Foundit":     "#dc2626",
    "TimesJobs":   "#d97706",
    # New 6
    "Glassdoor":   "#0caa41",
    "Wellfound":   "#f43f5e",
    "Instahyre":   "#7c3aed",
    "Hirist":      "#0891b2",
    "Monster":     "#7f1d1d",
    "Cutshort":    "#ea580c",
}

PORTAL_QUERIES = {
    # Scoped to actual job-listing URL paths to avoid social posts / articles
    "Naukri":      'site:naukri.com/job-listings "{role}" {location}',
    "LinkedIn":    'site:linkedin.com/jobs/view "{role}" {location} India',
    "Indeed":      'site:indeed.co.in/viewjob "{role}" {location}',
    "Internshala": 'site:internshala.com/job/detail "{role}" {location}',
    "Shine":       'site:shine.com/job-search "{role}" {location}',
    "Foundit":     'site:foundit.in/job "{role}" {location}',
    "TimesJobs":   'site:timesjobs.com/job-detail "{role}" {location}',
    "Glassdoor":   'site:glassdoor.co.in/job-listing "{role}" {location}',
    "Wellfound":   'site:wellfound.com/jobs "{role}" India',
    "Instahyre":   'site:instahyre.com/job "{role}" {location}',
    "Hirist":      'site:hirist.tech/j "{role}" {location}',
    "Monster":     'site:monsterindia.com/job "{role}" {location}',
    "Cutshort":    'site:cutshort.io/jobs "{role}" {location}',
}

# URL must contain at least one of these substrings to be accepted as a real job listing
PORTAL_URL_ALLOWLIST = {
    "Naukri":      ["naukri.com/job-listings", "naukri.com/jobs/"],
    "LinkedIn":    ["linkedin.com/jobs/view"],
    "Indeed":      ["indeed.co.in/viewjob", "indeed.co.in/jobs/"],
    "Internshala": ["internshala.com/job/", "internshala.com/jobs/"],
    "Shine":       ["shine.com/job-search", "shine.com/jobs/"],
    "Foundit":     ["foundit.in/job/", "foundit.in/jobs/"],
    "TimesJobs":   ["timesjobs.com/job-detail", "timesjobs.com/jobs/"],
    "Glassdoor":   ["glassdoor.co.in/job-listing", "glassdoor.co.in/Jobs/"],
    "Wellfound":   ["wellfound.com/jobs/", "wellfound.com/job/"],
    "Instahyre":   ["instahyre.com/job/", "instahyre.com/jobs/"],
    "Hirist":      ["hirist.tech/j/", "hirist.tech/jobs/"],
    "Monster":     ["monsterindia.com/job/", "monsterindia.com/srp/"],
    "Cutshort":    ["cutshort.io/jobs/", "cutshort.io/job/"],
}

# URL fragments that always indicate non-job content — block regardless of portal
GLOBAL_URL_BLOCKLIST = [
    "/posts/", "/post/", "/pulse/", "/article/", "/articles/",
    "/blog/", "/blogs/", "/news/", "/in/",         # linkedin profiles
    "/company/", "/school/", "/groups/",            # linkedin non-job pages
    "quora.com", "reddit.com", "youtube.com",
    "twitter.com", "facebook.com", "instagram.com",
    "wikipedia.org", "wiki/", "forum", ".pdf",
]

WORK_MODE_KEYWORDS = {
    "Remote":           ["remote", "work from home", "wfh"],
    "Hybrid":           ["hybrid"],
    "On-site / Office": ["on-site", "onsite", "office", "in-office"],
}

SKILLS_MAP = {
    "Data Analyst":         ["SQL", "Power BI", "Excel", "Python", "Tableau", "Data Visualization"],
    "Data Scientist":       ["Python", "ML", "SQL", "Pandas", "Scikit-learn", "Statistics"],
    "Data Engineer":        ["Python", "SQL", "PySpark", "AWS", "Airflow", "ETL", "Hadoop"],
    "Python Developer":     ["Python", "Django", "Flask", "REST API", "SQL", "Git"],
    "Power BI Developer":   ["Power BI", "DAX", "SQL", "Excel", "Data Modeling", "Azure"],
    "SQL Developer":        ["SQL", "MySQL", "PostgreSQL", "Stored Procedures", "ETL", "Oracle"],
    "BI Analyst":           ["Power BI", "Tableau", "SQL", "Excel", "Looker", "Data Visualization"],
    "ML Engineer":          ["Python", "TensorFlow", "PyTorch", "MLOps", "Docker", "Kubernetes"],
    "AI Engineer":          ["Python", "LLM", "OpenAI", "LangChain", "PyTorch", "NLP"],
    "NLP Engineer":         ["Python", "NLP", "BERT", "Transformers", "SpaCy", "Text Mining"],
    "Business Analyst":     ["SQL", "Excel", "Power BI", "Tableau", "Requirement Gathering", "JIRA"],
    "ETL Developer":        ["ETL", "SQL", "Informatica", "SSIS", "Talend", "Python"],
    "Database Administrator":["SQL", "Oracle", "MySQL", "PostgreSQL", "Performance Tuning", "Backup"],
    "Analytics Engineer":   ["dbt", "SQL", "Python", "Snowflake", "BigQuery", "Looker"],
    "Tableau Developer":    ["Tableau", "SQL", "Data Visualization", "Python", "ETL", "Dashboards"],
}

# Map UI date keys → Serper tbs (Google date range) parameters
_SERPER_DATE_MAP = {
    "d":  "qdr:d",
    "d3": "qdr:d3",
    "w":  "qdr:w",
    "w2": "qdr:w2",
    "m":  "qdr:m",
    None: None,
}

# ══════════════════════════════════════════════════════════════════
#  SERPER SEARCH  (works on Streamlit Cloud — no IP blocking)
#  Get free API key at https://serper.dev  (2,500 free searches/month)
#  Add to Streamlit secrets:  SERPER_API_KEY = "your_key_here"
# ══════════════════════════════════════════════════════════════════
def serper_search(query: str, tbs: str | None, num: int = 10) -> list[dict]:
    """Call Serper.dev Google Search API. Returns list of {title, href, body}."""
    # Key priority: session_state (sidebar input) → st.secrets
    api_key = (
        st.session_state.get("serper_api_key", "")
        or (st.secrets.get("SERPER_API_KEY", "") if hasattr(st, "secrets") else "")
    )
    if not api_key:
        return []   # warning already shown in sidebar

    payload = {"q": query, "num": num, "gl": "in", "hl": "en"}
    if tbs:
        payload["tbs"] = tbs

    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )
        if resp.status_code == 401:
            st.error("❌ Serper API key is invalid. Please check your key in the sidebar.")
            return []
        if resp.status_code == 429:
            st.warning("⚠️ Serper rate limit hit — you've used your free quota. Check serper.dev.")
            return []
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title", ""),
                "href":  item.get("link", "#"),
                "body":  item.get("snippet", ""),
            })
        return results
    except requests.exceptions.Timeout:
        st.warning("⚠️ Serper request timed out. Try again.")
        return []
    except Exception:
        return []

# ══════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════
def detect_portal(url: str) -> str:
    u = url.lower()
    portal_map = {
        "naukri":      "Naukri",
        "linkedin":    "LinkedIn",
        "indeed":      "Indeed",
        "internshala": "Internshala",
        "shine.com":   "Shine",
        "foundit":     "Foundit",
        "timesjobs":   "TimesJobs",
        "glassdoor":   "Glassdoor",
        "wellfound":   "Wellfound",
        "instahyre":   "Instahyre",
        "hirist":      "Hirist",
        "monsterindia":"Monster",
        "cutshort":    "Cutshort",
    }
    for key, name in portal_map.items():
        if key in u:
            return name
    return "Web"

def extract_salary(text: str) -> str:
    pats = [
        r'(?:₹|INR|Rs\.?)\s*\d[\d,.]*\s*[-–to]+\s*(?:₹|INR|Rs\.?)?\s*\d[\d,.]*\s*(?:LPA|lakh|L|lac|CTC)?',
        r'\d+[\d.]*\s*[-–]\s*\d+[\d.]*\s*(?:LPA|lakh|L|CTC)',
        r'\d+\s*(?:LPA|lakh|L|lac)\s*(?:to|-)\s*\d+\s*(?:LPA|lakh|L)',
    ]
    for p in pats:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return ""

def extract_company(title: str, body: str) -> str:
    text = title + " " + body[:300]
    patterns = [
        r'at\s+([A-Z][A-Za-z0-9 &.,\-]+?)(?:\s*[-|•,]|\s+in\s|\s+for\s)',
        r'[-–|]\s*([A-Z][A-Za-z0-9 &.,\-]{3,40})\s*[-|]',
        r'([A-Z][A-Za-z0-9 &.,\-]{3,35})\s+(?:is hiring|hiring now|jobs)',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            name = m.group(1).strip().rstrip(".,- ")
            if 3 < len(name) < 45 and name.lower() not in (
                "the","this","our","their","view","apply","latest"
            ):
                return name
    return "—"

def clean_title(raw: str) -> str:
    for noise in [
        "| Naukri.com","| LinkedIn","| Indeed India","| Internshala",
        "- Naukri.com","- LinkedIn","- Shine","- Foundit","- TimesJobs",
        "| Glassdoor","- Glassdoor","| Wellfound","- Wellfound",
        "| Instahyre","- Instahyre","| Hirist","- Hirist",
        "| Monster India","- Monster India","| Cutshort","- Cutshort",
        "Apply Now","Job Details","View Job","Hiring","Job Opening",
        "| Job","| Career",
    ]:
        raw = raw.replace(noise, "")
    return raw.strip()[:90]

def exp_key(exp_label: str) -> str:
    if "Fresher" in exp_label: return "fresher"
    if "1"       in exp_label: return "1-3"
    if "3"       in exp_label: return "3-5"
    return "5plus"

def detect_work_mode(text: str) -> str:
    """Detect work mode from job title + snippet text."""
    t = text.lower()
    if any(k in t for k in ["remote","work from home","wfh"]):
        return "Remote"
    if "hybrid" in t:
        return "Hybrid"
    return "On-site"

def search_one_portal(
    portal: str, role: str, location: str, exp: str,
    days_key: str, work_mode: str
) -> tuple[str, list]:
    results = []
    try:
        tmpl  = PORTAL_QUERIES.get(portal, 'site:{portal} "{role}" jobs {location} India')
        query = tmpl.format(role=role, location=location, portal=portal.lower()+".com")

        # Experience modifier
        exp_k = exp_key(exp)
        if exp_k == "fresher":
            query += " fresher entry level"
        elif exp_k == "1-3":
            query += " 1 2 3 years experience"
        elif exp_k == "3-5":
            query += " 3 4 5 years senior"
        elif exp_k == "5plus":
            query += " senior lead 5+ years"

        # Work mode in query
        if work_mode == "Remote":
            query += " remote OR \"work from home\" OR WFH"
        elif work_mode == "Hybrid":
            query += " hybrid"
        elif work_mode == "On-site / Office":
            query += " onsite OR \"in office\""

        # Days → Serper tbs date filter
        tbs = _SERPER_DATE_MAP.get(days_key)

        # Primary search using Serper (works on Streamlit Cloud)
        raw = serper_search(query, tbs, num=10)

        # Fallback: broader root-domain query if strict path returns nothing
        if not raw:
            fallback_q = f'site:{portal.lower()}.com "{role}" {location} jobs'
            time.sleep(0.5)
            raw = serper_search(fallback_q, tbs, num=10)

        for r in raw:
            title = clean_title(r.get("title", ""))
            body  = r.get("body", "")
            url   = r.get("href", "#")

            if not title or not url:
                continue

            url_lower = url.lower()

            # 1. Block known non-job URLs globally
            if any(bad in url_lower for bad in GLOBAL_URL_BLOCKLIST):
                continue

            # 2. For this portal, URL must match at least one known job-listing path
            allowed_paths = PORTAL_URL_ALLOWLIST.get(portal, [])
            if allowed_paths and not any(p.lower() in url_lower for p in allowed_paths):
                continue

            combined_text = title + " " + body
            mode = detect_work_mode(combined_text)

            results.append({
                "title":     title,
                "company":   extract_company(title, body),
                "location":  location,
                "salary":    extract_salary(body),
                "exp_raw":   exp,
                "portal":    portal,          # ← use the searched portal directly
                "url":       url,
                "skills":    SKILLS_MAP.get(role, ["SQL", "Python"]),
                "snippet":   body[:170].strip(),
                "role":      role,
                "work_mode": mode,
            })
    except Exception:
        pass
    return portal, results

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
for key, default in {
    "all_jobs":         {},
    "searched":         False,
    "failed_portals":   [],
    "filter_portal":    "All",
    "filter_salary":    False,
    "filter_mode":      "Any",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 💼 Search Filters")
    st.markdown("---")

    # ── API KEY ── enter here if not set in Streamlit secrets
    _secret_key = st.secrets.get("SERPER_API_KEY", "") if hasattr(st, "secrets") else ""
    if _secret_key:
        st.success("✅ Serper API key loaded from secrets")
        api_key_input = _secret_key
    else:
        st.warning("⚠️ No API key in secrets")
        api_key_input = st.text_input(
            "🔑 Serper API Key",
            type="password",
            placeholder="Paste key from serper.dev",
            help="Get free key at https://serper.dev (2500 searches/month free)"
        )

    if api_key_input:
        st.session_state["serper_api_key"] = api_key_input
        # Test button
        if st.button("🧪 Test API Key"):
            try:
                r = requests.post(
                    "https://google.serper.dev/search",
                    headers={"X-API-KEY": api_key_input, "Content-Type": "application/json"},
                    json={"q": "data analyst jobs India", "num": 1},
                    timeout=8,
                )
                if r.status_code == 200 and r.json().get("organic"):
                    st.success("✅ API key works! Ready to search.")
                elif r.status_code == 401:
                    st.error("❌ Invalid API key — check serper.dev")
                else:
                    st.error(f"❌ Error {r.status_code}: {r.text[:120]}")
            except Exception as e:
                st.error(f"❌ Connection failed: {e}")
    else:
        st.session_state["serper_api_key"] = ""
        st.info("Get a free API key at [serper.dev](https://serper.dev)")

    st.markdown("---")

    role       = st.selectbox("🎯 Role",       ROLES)
    location   = st.selectbox("📍 City",       CITIES)
    experience = st.selectbox("🎓 Experience", EXP)

    # ── NEW: Days filter ──
    days_label = st.selectbox(
        "📅 Posted Within",
        list(DAYS_OPTIONS.keys()),
        index=4,   # default = Last 30 days
        help="Filter jobs by how recently they were posted"
    )
    days_key = DAYS_OPTIONS[days_label]

    # ── NEW: Work mode filter ──
    work_mode = st.selectbox(
        "🏠 Work Mode",
        WORK_MODES,
        help="Remote / Hybrid / On-site"
    )

    st.markdown("### 🌐 Portals")
    portal_flags = {}
    for p, color in PORTAL_COLORS.items():
        portal_flags[p] = st.checkbox(
            p, value=p in ("Naukri", "LinkedIn", "Indeed", "Internshala")
        )

    st.markdown("---")
    go = st.button("🔍 Search Jobs", use_container_width=True, type="primary")

    # Post-search result filters
    if st.session_state.searched:
        st.markdown("### 🎛 Filter Results")
        all_flat = [j for jobs in st.session_state.all_jobs.values() for j in jobs]

        portals_found = ["All"] + sorted(set(j["portal"] for j in all_flat))
        st.session_state.filter_portal = st.selectbox("By Portal", portals_found, key="fp")

        modes_found = ["Any"] + sorted(set(j.get("work_mode","") for j in all_flat if j.get("work_mode","")))
        st.session_state.filter_mode = st.selectbox("By Work Mode", modes_found, key="fm")

        st.session_state.filter_salary = st.checkbox("💰 Show salary only", key="fs")

# ══════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>🔍 DataJobs India</h1>
  <p>Live job search across 13 portals · Powered by Serper.dev · Always Free</p>
  <div class="chips">
    <span class="chip">Naukri</span>
    <span class="chip">LinkedIn</span>
    <span class="chip">Indeed</span>
    <span class="chip">Internshala</span>
    <span class="chip">Shine</span>
    <span class="chip">Foundit</span>
    <span class="chip">TimesJobs</span>
    <span class="chip">Glassdoor</span>
    <span class="chip">Wellfound</span>
    <span class="chip">Instahyre</span>
    <span class="chip">Hirist</span>
    <span class="chip">Monster</span>
    <span class="chip">Cutshort</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  SEARCH
# ══════════════════════════════════════════════════════════════════
if go:
    if not st.session_state.get("serper_api_key", ""):
        st.error("❌ Please enter your Serper API key in the sidebar before searching. Get one free at https://serper.dev")
        st.stop()
    selected = [p for p, v in portal_flags.items() if v]
    if not selected:
        st.warning("Select at least one portal.")
        st.stop()

    st.session_state.all_jobs    = {}
    st.session_state.failed_portals = []
    st.session_state.searched    = False

    prog_bar = st.progress(0, text="⚡ Starting parallel search...")
    status   = st.empty()
    done     = [0]
    total_p  = len(selected)

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {
            ex.submit(
                search_one_portal, p, role, location, experience, days_key, work_mode
            ): p
            for p in selected
        }
        for fut in as_completed(futures):
            portal_name, jobs = fut.result()
            if jobs:
                st.session_state.all_jobs[portal_name] = jobs
            else:
                st.session_state.failed_portals.append(portal_name)
            done[0] += 1
            pct = done[0] / total_p
            prog_bar.progress(pct, text=f"✅ {done[0]}/{total_p} portals searched...")

    prog_bar.progress(1.0, text="🎉 Search complete!")
    time.sleep(0.4)
    prog_bar.empty()
    status.empty()
    # Show portals that returned no results
    failed = st.session_state.get("failed_portals", [])
    if failed:
        st.warning(f"⚠️ No results from: **{', '.join(failed)}** — DuckDuckGo may be rate-limiting these. Try again in a few seconds.")
    st.session_state.searched = True
    st.rerun()

# ══════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════
if st.session_state.searched:
    all_flat = [j for jobs in st.session_state.all_jobs.values() for j in jobs]

    # Apply result filters
    filtered = all_flat
    if st.session_state.get("filter_portal", "All") != "All":
        filtered = [j for j in filtered if j["portal"] == st.session_state.filter_portal]
    if st.session_state.get("filter_mode", "Any") not in ("Any", ""):
        filtered = [j for j in filtered if j.get("work_mode","") == st.session_state.filter_mode]
    if st.session_state.get("filter_salary", False):
        filtered = [j for j in filtered if j.get("salary", "")]

    total     = len(filtered)
    companies = len(set(j["company"] for j in filtered if j["company"] != "—"))
    portals_n = len(set(j["portal"] for j in filtered))
    remote_n  = sum(1 for j in filtered if j.get("work_mode","") == "Remote")
    sal_n     = sum(1 for j in filtered if j.get("salary",""))

    if total == 0:
        st.markdown("""
        <div class="empty">
          <div class="empty-icon">🔎</div>
          <div class="empty-title">No results found</div>
          <div class="empty-sub">DuckDuckGo may be rate-limiting, or no jobs match your filters.
          Try a wider date range or different work mode, then search again.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Stats row
        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-card">
            <div class="stat-icon">📋</div>
            <div class="stat-value">{total}</div>
            <div class="stat-label">Jobs Found</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏢</div>
            <div class="stat-value">{companies}</div>
            <div class="stat-label">Companies</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🏠</div>
            <div class="stat-value">{remote_n}</div>
            <div class="stat-label">Remote Jobs</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-value">{sal_n}</div>
            <div class="stat-label">With Salary</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Group by portal
        by_portal: dict[str, list] = {}
        for j in filtered:
            by_portal.setdefault(j["portal"], []).append(j)

        for portal, jobs in by_portal.items():
            color = PORTAL_COLORS.get(portal, "#6366f1")
            st.markdown(f"""
            <div class="portal-section">
              <div class="portal-dot" style="background:{color};"></div>
              <div class="portal-title">{portal}</div>
              <div class="portal-count">{len(jobs)} jobs</div>
            </div>
            """, unsafe_allow_html=True)

            for job in jobs:
                portal_cls = f"card-{portal.lower()}" if portal.lower() in {k.lower() for k in PORTAL_COLORS} else "card-default"
                badge_cls  = f"badge-portal-{portal.lower()}" if portal.lower() in {k.lower() for k in PORTAL_COLORS} else "badge-portal-default"
                sal_badge  = f'<span class="badge badge-sal">💰 {job["salary"]}</span>' if job.get("salary") else ""
                mode_val   = job.get("work_mode","")
                mode_icon  = {"Remote":"🏠","Hybrid":"🔀","On-site":"🏢"}.get(mode_val, "📌")
                mode_badge = f'<span class="badge badge-mode">{mode_icon} {mode_val}</span>' if mode_val else ""
                skills_html = "".join(f'<span class="skill">{s}</span>' for s in job["skills"][:6])
                snippet     = f'<div class="snippet">{job["snippet"]}</div>' if job.get("snippet") else ""
                url         = job["url"] if job["url"].startswith("http") else "#"

                st.markdown(f"""
                <div class="job-card {portal_cls}">
                  <div class="job-header">
                    <div style="flex:1;">
                      <div class="job-title">{job['title']}</div>
                      <div class="job-company">{job['company']}</div>
                    </div>
                    <a href="{url}" target="_blank" class="apply-btn">Apply ↗</a>
                  </div>
                  <div class="badges">
                    <span class="badge {badge_cls}">{portal}</span>
                    <span class="badge badge-loc">📍 {job['location']}</span>
                    <span class="badge badge-exp">🎓 {job['exp_raw'].split('(')[0].strip()}</span>
                    {mode_badge}
                    {sal_badge}
                  </div>
                  <div class="skills-row">{skills_html}</div>
                  {snippet}
                </div>
                """, unsafe_allow_html=True)

        # CSV download
        st.markdown("<br>", unsafe_allow_html=True)
        lines = ["Title,Company,Location,Work Mode,Salary,Portal,URL"]
        for j in filtered:
            lines.append(
                f'"{j["title"]}","{j["company"]}","{j["location"]}",'
                f'"{j.get("work_mode","")}","{j.get("salary","")}","{j["portal"]}","{j["url"]}"'
            )
        st.download_button(
            "⬇️ Download Jobs as CSV",
            data="\n".join(lines),
            file_name="datajobs_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

elif not st.session_state.searched:
    st.markdown("""
    <div class="empty">
      <div class="empty-icon">🎯</div>
      <div class="empty-title">Ready to Find Jobs</div>
      <div class="empty-sub">Select role, city, experience, date range & work mode in the sidebar — then click Search Jobs</div>
    </div>
    """, unsafe_allow_html=True)
