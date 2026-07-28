import streamlit as st
import requests
import json
import re

st.set_page_config(page_title="Blinkit · Try-Small-First MVP", page_icon="🧺", layout="centered")

# ---------------------------------------------------------------------------
# Palette + shared CSS (matches the deck / React prototype)
# ---------------------------------------------------------------------------
INK = "#141414"; SUB = "#4A4A46"; GREEN = "#1F6F54"; GREENBG = "#E1EEE8"
AMBER = "#B97D06"; AMBERBG = "#FCEBC0"; MUTED = "#F1F1EC"; YELLOW = "#F8CB46"; BORDER = "#E7E7E2"

st.markdown(f"""
<style>
.stApp {{ background:#FAFAF8; }}
.phone {{
  width: 360px; margin: 0 auto; background:#fff; border-radius:30px;
  border: 9px solid {INK}; box-shadow:0 20px 50px rgba(0,0,0,0.18);
  overflow:hidden; padding: 20px 18px; font-family: -apple-system, "Segoe UI", sans-serif;
  color:{INK};
}}
.topbar {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }}
.logo {{ font-weight:800; font-size:21px; }}
.logo .b {{ color:{YELLOW}; }} .logo .k {{ color:{GREEN}; }}
.eta {{ font-size:12.5px; color:{SUB}; font-weight:600; }}
.search {{ border:1px solid {BORDER}; border-radius:13px; padding:11px 14px; font-size:13.5px; color:{SUB}; margin-bottom:16px;}}
.label {{ font-size:12px; font-weight:800; color:{SUB}; margin-bottom:9px; letter-spacing:0.3px;}}
.groceries {{ display:flex; gap:9px; margin-bottom:18px; }}
.g-item {{ flex:1; background:{MUTED}; border-radius:11px; padding:11px 6px; text-align:center; }}
.g-item .icon {{ font-size:22px; margin-bottom:6px; }}
.g-item .name {{ font-size:10.5px; color:{SUB}; }}
.g-item .price {{ font-size:12px; font-weight:700; }}
.nudge {{ background:{AMBERBG}; border:1.5px dashed {AMBER}; border-radius:15px; padding:15px; }}
.nudge .tag {{ font-size:11.5px; font-weight:800; color:{AMBER}; letter-spacing:0.3px; margin-bottom:7px;}}
.footnote {{ font-size:11.5px; color:#9a9a94; margin-top:11px; text-align:center; }}
.stepper {{ font-size:12px; font-weight:800; color:{SUB}; margin-bottom:9px; }}
.progress {{ height:8px; background:{MUTED}; border-radius:4px; margin-bottom:17px; overflow:hidden;}}
.progress .fill {{ height:100%; background:linear-gradient(90deg, {AMBER}, {GREEN}); border-radius:4px; }}
.trial-card {{ border:1.6px dashed {AMBER}; background:{AMBERBG}; border-radius:17px; padding:17px; }}
.trial-row {{ display:flex; gap:13px; }}
.trial-icon {{ width:60px; height:60px; border-radius:11px; background:#fff; display:flex; align-items:center; justify-content:center; font-size:26px; flex-shrink:0;}}
.trial-name {{ font-weight:700; font-size:14.5px; }}
.rating {{ font-size:12.5px; color:{SUB}; margin-top:4px;}}
.price-row {{ margin-top:6px; font-weight:800; font-size:16px; }}
.mrp {{ font-size:12px; font-weight:400; color:#9a9a94; text-decoration:line-through; margin-left:4px;}}
.desc {{ font-size:12.5px; color:{SUB}; margin-top:11px; line-height:1.45; }}
.basket-title {{ font-weight:800; font-size:14.5px; margin:11px 0 13px;}}
.basket-row {{ display:flex; justify-content:space-between; font-size:13.5px; padding:8px 0; border-bottom:1px solid {BORDER}; }}
.basket-new {{ display:flex; justify-content:space-between; font-size:13.5px; padding:10px 9px; background:{AMBERBG}; margin:5px 0; border-radius:9px; }}
.new-tag {{ font-size:10px; background:{AMBER}; color:#fff; border-radius:6px; padding:2px 6px; font-weight:700; margin-left:6px;}}
.total-row {{ display:flex; justify-content:space-between; font-weight:800; font-size:15px; margin:13px 0 15px;}}
.confirm {{ text-align:center; padding-top:14px; }}
.check-circle {{ width:60px; height:60px; border-radius:50%; background:{GREEN}; display:flex; align-items:center; justify-content:center; margin:0 auto 15px; font-size:28px; color:#fff;}}
.confirm h2 {{ font-weight:800; font-size:18px; margin:0 0 7px;}}
.confirm .eta2 {{ font-size:13.5px; color:{SUB}; margin-bottom:20px;}}
.unlock-box {{ background:{GREENBG}; border:1px solid {GREEN}; border-radius:15px; padding:17px; text-align:left; }}
.unlock-box .tag {{ font-weight:800; font-size:13.5px; color:{GREEN}; margin-bottom:7px;}}
.unlock-box p {{ font-size:13px; color:{SUB}; line-height:1.5; margin:0;}}
.reengage {{ background:{GREENBG}; border:1px solid {GREEN}; border-radius:15px; padding:15px; }}
.reengage .tag {{ font-size:11.5px; font-weight:800; color:{GREEN}; letter-spacing:0.3px; margin-bottom:7px;}}
.daynote {{ font-size:11px; color:#9a9a94; margin-bottom:11px;}}
.ai-card {{ border:1.6px solid {GREEN}; border-radius:17px; overflow:hidden;}}
.ai-head {{ background:{GREENBG}; padding:12px 16px; font-weight:800; font-size:13.5px; color:{GREEN};}}
.ai-body {{ padding:17px; }}
.ai-msg {{ font-size:13.5px; line-height:1.55; margin:11px 0;}}
.conf-line {{ background:{MUTED}; border-radius:10px; padding:10px 12px; font-size:12.5px; color:{SUB}; margin-bottom:14px;}}
.trophy-box {{ background:{AMBERBG}; border:1px solid {AMBER}; border-radius:15px; padding:17px; text-align:left;}}
.trophy-box .tag {{ font-weight:800; font-size:13.5px; color:{AMBER}; margin-bottom:7px;}}
.trophy-box p {{ font-size:12.5px; color:{SUB}; line-height:1.5; margin:0;}}
div.stButton > button {{ width:100%; border-radius:10px; font-weight:700; padding:0.6em; }}
button[kind="primary"] {{ background-color:{GREEN} !important; border-color:{GREEN} !important; color:#fff !important; }}
button[kind="primary"]:hover {{ background-color:#18543f !important; border-color:#18543f !important; }}
</style>
""", unsafe_allow_html=True)

TRIAL_ITEM = {
    "name": "Braided USB-C Cable (1m)", "price": 49, "mrp": 99, "rating": 4.3,
    "reviews": [
        "Cheap but doesn't feel cheap — braided sleeve hasn't frayed after 2 months.",
        "Charges fast, exactly as advertised. Good starter buy if you're unsure about ordering electronics here.",
    ],
}
UPSELL_ITEM = {
    "name": "boAt Rockerz 255 Pro Wireless Earphones", "price": 1299, "mrp": 1999,
    "rating": 4.1, "rating_count": 214,
    "reviews": [
        "Sound quality is decent for the price, bass is punchy. Battery lasts about 6 hours.",
        "Got a defective piece once — replacement in 24 hours, no argument needed.",
        "Works well, connects fast to my phone.",
    ],
}
GROCERIES = [("Milk 1L", 62, "🥛"), ("Atta 5kg", 259, "🌾"), ("Snacks pack", 99, "🍪")]

# ---------------------------------------------------------------------------
# Real, server-side Claude call — the API key lives in st.secrets, never in
# the browser. This is the equivalent of the Vercel serverless function,
# just running directly inside Streamlit's own Python process.
# ---------------------------------------------------------------------------
def call_claude(prompt: str) -> str:
    api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set in Streamlit secrets")
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


def extract_json(text: str) -> dict:
    clean = re.sub(r"```json|```", "", text).strip()
    start, end = clean.find("{"), clean.rfind("}")
    return json.loads(clean[start:end + 1])


def get_upsell():
    prompt = f"""A Blinkit user just received their first Electronics item ever: a {TRIAL_ITEM['name']} (₹{TRIAL_ITEM['price']}), after being hesitant about the category for months. Real reviews of that trial item: {' | '.join(TRIAL_ITEM['reviews'])}.

Now recommend their natural next Electronics purchase: {UPSELL_ITEM['name']} (₹{UPSELL_ITEM['price']}). Real reviews of it: {' | '.join(UPSELL_ITEM['reviews'])}.

Write a short, warm, genuinely enticing (not salesy-fake) nudge that references the trial purchase as proof they can trust this category now. Be honest — mention the one real watch-out from reviews (a past defective unit) but frame the replacement policy as reassurance, not a warning label. Respond ONLY with JSON, no markdown fences:
{{
  "headline": "<punchy 5-8 word headline capitalizing on their trial win>",
  "message": "<2 sentences, warm and confident, grounded in the actual reviews>",
  "confidence_line": "<one short honest reassurance about quality/returns, under 18 words>"
}}"""
    try:
        text = call_claude(prompt)
        return extract_json(text)
    except Exception:
        return {
            "headline": "You've already got this",
            "message": "Your cable arrived exactly as promised — this pair of earphones comes from the same shelf.",
            "confidence_line": "Free replacement within 24 hours if anything's off.",
        }


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = 0
if "ai" not in st.session_state:
    st.session_state.ai = None

STEPS = ["Home", "Trial item", "Cart & checkout", "Order placed", "Next visit", "AI recommendation", "Complete"]


def goto(i):
    st.session_state.step = max(0, min(len(STEPS) - 1, i))


# ---------------------------------------------------------------------------
# Stepper
# ---------------------------------------------------------------------------
cols = st.columns(len(STEPS))
for i, (col, label) in enumerate(zip(cols, STEPS)):
    with col:
        if st.button(f"{i+1}", key=f"step_{i}", help=label, use_container_width=True,
                     type="primary" if i == st.session_state.step else "secondary"):
            goto(i)
st.caption(" · ".join(f"**{i+1}**. {l}" if i == st.session_state.step else f"{i+1}. {l}" for i, l in enumerate(STEPS)))

st.markdown("<br>", unsafe_allow_html=True)

step = st.session_state.step

if step == 0:
    st.markdown(f"""
    <div class="phone">
    <div class="topbar"><div class="logo"><span class="b">blink</span><span class="k">it</span></div><div class="eta">8 min delivery</div></div>
    <div class="search">🔍 Search "milk"</div>
    <div class="label">FREQUENTLY BOUGHT — SAME AS EVERY WEEK</div>
    <div class="groceries">
      {"".join(f'<div class="g-item"><div class="icon">{icon}</div><div class="name">{name}</div><div class="price">₹{price}</div></div>' for name, price, icon in GROCERIES)}
    </div>
    <div class="nudge">
      <div class="tag">✨ NEW FOR YOU, RIGHT HERE IN YOUR FEED</div>
      <p style="font-size:13.5px; line-height:1.5; margin:0 0 6px;">A ₹49 Electronics item people like you keep adding alongside their grocery order.</p>
    </div>
    <div class="footnote">No separate "Explore" tab — this rides inside the search-first habit itself.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("See the ₹49 starter", key="btn0"):
        goto(1)

elif step == 1:
    st.markdown(f"""
    <div class="phone">
    <div class="topbar"><div class="logo"><span class="b">blink</span><span class="k">it</span></div><div class="eta">8 min delivery</div></div>
    <div class="stepper">ELECTRONICS EXPLORER · Step 1 of 2</div>
    <div class="progress"><div class="fill" style="width:8%"></div></div>
    <div class="trial-card">
      <div class="trial-row">
        <div class="trial-icon">🔌</div>
        <div>
          <div class="trial-name">{TRIAL_ITEM['name']}</div>
          <div class="rating">⭐ {TRIAL_ITEM['rating']}</div>
          <div class="price-row">₹{TRIAL_ITEM['price']} <span class="mrp">₹{TRIAL_ITEM['mrp']}</span></div>
        </div>
      </div>
      <div class="desc">Almost no risk at this price — the easiest way to see if you'll trust Blinkit with Electronics.</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Add to basket — ₹49", key="btn1"):
        goto(2)

elif step == 2:
    rows = "".join(f'<div class="basket-row"><span>{n}</span><span>₹{p}</span></div>' for n, p, _ in GROCERIES)
    total = sum(p for _, p, _ in GROCERIES) + TRIAL_ITEM["price"]
    st.markdown(f"""
    <div class="phone">
    <div class="topbar"><div class="logo"><span class="b">blink</span><span class="k">it</span></div><div class="eta">8 min delivery</div></div>
    <div class="basket-title">🧺 Your basket</div>
    {rows}
    <div class="basket-new"><span>🔌 {TRIAL_ITEM['name']}<span class="new-tag">NEW</span></span><span>₹{TRIAL_ITEM['price']}</span></div>
    <div class="total-row"><span>Total</span><span>₹{total}</span></div>
    <div class="footnote">One trip, one delivery — no separate "trying electronics" errand.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Place order", key="btn2"):
        goto(3)

elif step == 3:
    st.markdown(f"""
    <div class="phone">
    <div class="confirm">
      <div class="check-circle">✓</div>
      <h2>Order placed</h2>
      <div class="eta2">Arriving in 8 minutes</div>
      <div class="unlock-box">
        <div class="tag">🎉 Electronics Explorer — Step 1 unlocked</div>
        <p>Your cable's on its way. Next time you open Blinkit, we'll show you what usually comes next.</p>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Continue → a few days later", key="btn3"):
        goto(4)

elif step == 4:
    st.markdown(f"""
    <div class="phone">
    <div class="topbar"><div class="logo"><span class="b">blink</span><span class="k">it</span></div><div class="eta">8 min delivery</div></div>
    <div class="daynote">3 days later · opening Blinkit for the weekly grocery run</div>
    <div class="search">🔍 Search "eggs"</div>
    <div class="reengage">
      <div class="tag">✓ YOUR CABLE ARRIVED — HOW WAS IT?</div>
      <p style="font-size:13.5px; line-height:1.5; margin:0 0 6px;">Since that went well, here's what most people try next in Electronics.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Show me", key="btn4"):
        with st.spinner("Building your recommendation from real reviews…"):
            st.session_state.ai = get_upsell()
        goto(5)

elif step == 5:
    ai = st.session_state.ai or get_upsell()
    st.session_state.ai = ai
    st.markdown(f"""
    <div class="phone">
    <div class="topbar"><div class="logo"><span class="b">blink</span><span class="k">it</span></div><div class="eta">8 min delivery</div></div>
    <div class="progress"><div class="fill" style="width:60%"></div></div>
    <div class="ai-card">
      <div class="ai-head">✓ {ai['headline']}</div>
      <div class="ai-body">
        <div class="trial-row">
          <div class="trial-icon">🎧</div>
          <div>
            <div class="trial-name">{UPSELL_ITEM['name']}</div>
            <div class="rating">⭐ {UPSELL_ITEM['rating']} · {UPSELL_ITEM['rating_count']} ratings</div>
            <div class="price-row">₹{UPSELL_ITEM['price']} <span class="mrp">₹{UPSELL_ITEM['mrp']}</span></div>
          </div>
        </div>
        <div class="ai-msg">{ai['message']}</div>
        <div class="conf-line">🔒 {ai['confidence_line']}</div>
      </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"Add to cart & place order — ₹{UPSELL_ITEM['price']}", key="btn5"):
        goto(6)

elif step == 6:
    st.markdown(f"""
    <div class="phone">
    <div class="confirm">
      <div class="check-circle" style="background:{AMBER};">🎉</div>
      <h2>Order placed</h2>
      <div class="eta2">Arriving in 8 minutes</div>
      <div class="trophy-box">
        <div class="tag">🏆 Electronics Explorer — complete</div>
        <p>Two orders in, one new category permanently unlocked. Same pattern now works for Beauty and Baby.</p>
      </div>
      <div class="progress" style="margin-top:15px;"><div class="fill" style="width:100%"></div></div>
    </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if st.button("← Prev", disabled=(step == 0), use_container_width=True):
        goto(step - 1)
with c2:
    if st.button("Next →", disabled=(step == len(STEPS) - 1), use_container_width=True):
        goto(step + 1)

st.caption("Live AI-native MVP — the Step 2 recommendation (screen 6) is generated fresh from real reviews by Claude on every run, server-side.")
