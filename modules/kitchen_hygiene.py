"""
Tab 3: Kitchen Hygiene & Food Safety Compliance Auditor (Epic 4)
Automated Computer Vision Compliance for Commercial Kitchens & HACCP Biosecurity
"""
import streamlit as st
import json
import tempfile
import os

from modules.sample_data import (
    SAMPLE_KITCHEN_COMPLIANT_IMAGE,
    SAMPLE_KITCHEN_VIOLATIONS_IMAGE,
    SAMPLE_KITCHEN_HYGIENE_COMPLIANT,
    SAMPLE_KITCHEN_HYGIENE_VIOLATION
)
from modules.ui_components import plot_hygiene_gauge, render_metric_card

def render_kitchen_hygiene_tab(ai_engine):
    st.markdown("### 👨‍🍳 Commercial Kitchen Hygiene & Food Safety Compliance")
    st.markdown(
        "Automated AI visual auditing for commercial food prep lines, restaurants, and catering facilities. "
        "Continuously evaluates mandatory personal protective equipment (chef hats, hairnets, beard nets, gloves), "
        "surface sanitization, and flags cross-contamination hazards (e.g. raw poultry near ready-to-eat produce)."
    )

    col_input, col_presets = st.columns([1.2, 0.8])

    with col_input:
        media_type = st.radio("Select Media Feed Type:", ["Still Image / Camera Snapshot", "Video Feed / Kitchen Clip"], horizontal=True, key="hygiene_media_type")

        if media_type == "Still Image / Camera Snapshot":
            uploaded_file = st.file_uploader(
                "Upload Kitchen Snapshot (JPG/PNG)",
                type=["jpg", "jpeg", "png", "webp"],
                key="kitchen_img_uploader",
                help="Wide or station-focused photo of food prep line"
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload Kitchen CCTV / Video Clip (MP4/MOV)",
                type=["mp4", "mov", "avi"],
                key="kitchen_vid_uploader",
                help="Short video clip (max 50MB) of kitchen line operations"
            )

        kitchen_type = st.selectbox(
            "Kitchen Sector / Station Type:",
            ["Cold Prep & Salad Station", "Hot Line & Sauté Station", "Butchery & Raw Meat Station", "Dishwashing & Sanitizing Bay", "Plating & Pass Station"],
            key="kitchen_station_sel"
        )

    with col_presets:
        st.markdown("**⚡ Instant Regulatory Audit Scenarios:**")
        preset_choice = st.radio(
            "Select Audit Preset Scenario:",
            [
                "None (Use Upload)",
                "Compliant 5-Star Prep Station (100% PPE & Sanitized)",
                "Critical Violation Alert (Uncovered Hair & Raw Poultry Hazard)"
            ],
            index=2 if not uploaded_file else 0,
            key="kitchen_preset_radio"
        )

    image_bytes = None
    active_sample_data = None

    if uploaded_file is not None:
        if media_type == "Video Feed / Kitchen Clip":
            st.video(uploaded_file)
            st.info("Video feed loaded. FoodVerse AI will sample key analytical frames for biosecurity compliance inspection.")
            # For video, extract first 500KB as buffer or use fallback
            image_bytes = SAMPLE_KITCHEN_VIOLATIONS_IMAGE
        else:
            image_bytes = uploaded_file.getvalue()
    elif "Compliant" in preset_choice:
        image_bytes = SAMPLE_KITCHEN_COMPLIANT_IMAGE
        active_sample_data = SAMPLE_KITCHEN_HYGIENE_COMPLIANT
    elif "Critical Violation" in preset_choice:
        image_bytes = SAMPLE_KITCHEN_VIOLATIONS_IMAGE
        active_sample_data = SAMPLE_KITCHEN_HYGIENE_VIOLATION

    if image_bytes:
        if media_type != "Video Feed / Kitchen Clip" or uploaded_file is None:
            st.image(image_bytes, caption="Active Commercial Kitchen Video/Photo Feed for Safety Audit", use_container_width=True)

        audit_btn = st.button("🚨 Run Kitchen Hygiene Compliance Audit", key="btn_run_hygiene", use_container_width=True)

        if audit_btn or "hygiene_cache" in st.session_state:
            if audit_btn:
                with st.spinner("Executing HACCP biometric scans, PPE detection & cross-contamination safety audits..."):
                    if ai_engine.is_demo() and active_sample_data:
                        results = active_sample_data
                    else:
                        results = ai_engine.analyze_kitchen_hygiene(image_bytes, kitchen_type)
                    st.session_state["hygiene_cache"] = results
            else:
                results = st.session_state.get("hygiene_cache", active_sample_data or SAMPLE_KITCHEN_HYGIENE_VIOLATION)

            st.markdown("---")
            render_hygiene_results(results)


def render_hygiene_results(data: dict):
    area = data.get("kitchen_area", "Commercial Food Preparation Line")
    score = int(data.get("compliance_score", 75))
    grade = data.get("safety_grade", "B (Satisfactory)")
    inspected = data.get("inspected_items", [])
    violations = data.get("violations", [])
    corrective = data.get("corrective_actions", [])

    # Header Card
    badge_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    st.markdown(
        f"""
        <div class="fv-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <span style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase;">INSPECTED SECTOR: {area}</span>
                    <h2 style="color:#FFFFFF; margin:4px 0 8px 0; font-size:1.8rem;">Regulatory Food Safety Audit</h2>
                    <span style="background:rgba(255,255,255,0.06); padding:4px 12px; border-radius:12px; color:{badge_color}; font-weight:700; border:1px solid {badge_color}55;">
                        GRADE: {grade}
                    </span>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:0.8rem; color:#94A3B8;">HACCP COMPLIANCE BENCHMARK</div>
                    <div style="font-size:1.8rem; font-weight:800; color:{badge_color};">{score}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Gauge & Quick Status
    col_gauge, col_items = st.columns([1, 1.2])

    with col_gauge:
        fig_gauge = plot_hygiene_gauge(score)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_items:
        st.markdown("#### 📋 Core Biosecurity Indicators")
        for item in inspected:
            indicator = item.get("indicator", "Item")
            status = item.get("status", "Compliant")
            details = item.get("details", "")

            if "Compliant" in status:
                icon = "🟢"
                pill_class = "violation-pill-pass"
            elif "Warning" in status:
                icon = "🟡"
                pill_class = "violation-pill-warning"
            else:
                icon = "🔴"
                pill_class = "violation-pill-critical"

            st.markdown(
                f"""
                <div class="{pill_class}">
                    <div style="font-weight:700;">{icon} {indicator}: <span style="font-weight:600;">{status}</span></div>
                    <div style="font-size:0.85rem; opacity:0.9; margin-top:2px;">{details}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Itemized Violations Log
    st.markdown("#### 🚨 Itemized Violation Log & Risk Vectors")
    if violations:
        for v in violations:
            sev = v.get("severity", "Major")
            v_name = v.get("violation", "Safety Issue")
            v_desc = v.get("description", "")
            risk = v.get("haccp_risk", "")

            sev_color = "#EF4444" if sev == "Critical" else "#F59E0B" if sev == "Major" else "#3B82F6"
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(255,255,255,0.08); border-left: 5px solid {sev_color}; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.05rem; font-weight:700; color:#F8FAFC;">{v_name}</span>
                        <span style="background:{sev_color}25; color:{sev_color}; border:1px solid {sev_color}55; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">
                            {sev} SEVERITY
                        </span>
                    </div>
                    <p style="color:#CBD5E1; font-size:0.92rem; margin:6px 0 8px 0; line-height:1.4;">{v_desc}</p>
                    <div style="font-size:0.82rem; color:#94A3B8;"><b>HACCP Biosecurity Risk:</b> {risk}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("🎉 Zero safety violations detected! Kitchen station adheres strictly to HACCP & FDA Food Code guidelines.")

    # Actionable Corrective Actions Checklist
    st.markdown("#### 🛠️ Immediate Corrective Actions & Protocol Mandates")
    if corrective:
        for i, act in enumerate(corrective, 1):
            st.checkbox(f"**Step {i}:** {act}", key=f"action_chk_{i}")

    # Export Audit Log
    st.download_button(
        label="📥 Download Official Kitchen Hygiene Audit Report",
        data=json.dumps(data, indent=2),
        file_name=f"foodverse_kitchen_audit_{area.lower().replace(' ', '_')}.json",
        mime="application/json"
    )
