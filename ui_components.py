"""UI Components for Noon Last-Mile Resolver."""

import streamlit as st
from typing import Dict, Any, List
from config import NOON_COLORS, TRANSLATIONS


def t(key: str, language: str = "en") -> str:
    """Get translated text."""
    return TRANSLATIONS.get(language, {}).get(key, key)


def render_noon_branding() -> None:
    """Render custom Noon branding CSS with professional styling."""
    css = f"""
    <style>
    :root {{
        --noon-bg: {NOON_COLORS['background']};
        --noon-yellow: {NOON_COLORS['primary_yellow']};
        --noon-text: {NOON_COLORS['text']};
        --noon-red: {NOON_COLORS['accent_red']};
        --noon-green: {NOON_COLORS['accent_green']};
    }}
    
    body, .main {{
        background-color: {NOON_COLORS['background']} !important;
        color: {NOON_COLORS['text']} !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }}
    
    /* Typography */
    h1, h2, h3 {{
        font-weight: 600;
        letter-spacing: -0.3px;
        color: {NOON_COLORS['text']};
        margin-bottom: 1rem;
    }}
    
    h1 {{ font-size: 32px; font-weight: 700; }}
    h2 {{ font-size: 24px; font-weight: 600; }}
    h3 {{ font-size: 18px; font-weight: 600; }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {{
        background-color: transparent;
        border: none;
        border-bottom: 3px solid #f0f0f0;
        color: {NOON_COLORS['text']};
        font-weight: 500;
        font-size: 14px;
        padding: 12px 16px !important;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .stTabs [data-baseweb="tab-list"] button:hover {{
        border-bottom-color: {NOON_COLORS['primary_yellow']};
        background-color: #f9f9f9;
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        border-bottom-color: {NOON_COLORS['primary_yellow']};
        color: {NOON_COLORS['text']};
        font-weight: 600;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {NOON_COLORS['primary_yellow']};
        color: {NOON_COLORS['text']};
        font-weight: 600;
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-size: 14px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
    }}
    
    .stButton > button:hover {{
        background-color: #FFC700;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(255, 224, 0, 0.2);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border: 1px solid #e0e0e0 !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        padding: 12px !important;
        transition: all 0.2s ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {NOON_COLORS['primary_yellow']} !important;
        box-shadow: 0 0 0 3px rgba(255, 224, 0, 0.1) !important;
    }}
    
    /* Cards */
    .delivery-card {{
        background-color: {NOON_COLORS['background']};
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }}
    
    .delivery-card:hover {{
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }}
    
    /* Warning card */
    .warning-card {{
        background-color: #FEF3E0;
        border-left: 4px solid #FF8C42;
        border-radius: 6px;
        padding: 16px;
        margin: 16px 0;
        font-size: 14px;
        line-height: 1.5;
    }}
    
    .warning-card strong {{
        color: #D84315;
        font-weight: 600;
    }}
    
    /* Success card */
    .success-card {{
        background-color: #E8F5E9;
        border-left: 4px solid #4CAF50;
        border-radius: 6px;
        padding: 16px;
        margin: 16px 0;
        font-size: 14px;
        line-height: 1.5;
    }}
    
    .success-card strong {{
        color: #2E7D32;
        font-weight: 600;
    }}
    
    /* Info/Moderate card */
    .info-card {{
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
        border-radius: 6px;
        padding: 16px;
        margin: 16px 0;
        font-size: 14px;
        line-height: 1.5;
    }}
    
    .info-card strong {{
        color: #1565C0;
        font-weight: 600;
    }}
    
    /* Metric box */
    .metric-box {{
        background-color: #F5F5F5;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        transition: all 0.2s ease;
    }}
    
    .metric-box:hover {{
        background-color: #FAFAFA;
        border-color: {NOON_COLORS['primary_yellow']};
        box-shadow: 0 2px 4px rgba(255, 224, 0, 0.1);
    }}
    
    /* Driver view */
    .driver-view {{
        background-color: #F9F9F9;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 20px;
        font-size: 13px;
        line-height: 1.6;
        font-family: 'Courier New', monospace;
    }}
    
    /* Latency badge */
    .latency-badge {{
        background-color: {NOON_COLORS['primary_yellow']};
        color: {NOON_COLORS['text']};
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(255, 224, 0, 0.2);
    }}
    
    /* Sidebar */
    .stSidebar {{
        background-color: {NOON_COLORS['background']};
    }}
    
    [data-testid="stSidebar"] {{
        box-shadow: 1px 0 4px rgba(0, 0, 0, 0.04);
    }}
    
    /* Status container */
    .stStatus {{
        background-color: #F5F5F5;
        border-radius: 8px;
    }}
    
    /* Horizontal divider */
    hr {{
        border: none;
        border-top: 1px solid #E0E0E0;
        margin: 24px 0;
    }}
    
    /* Expandable sections */
    .streamlit-expanderHeader {{
        background-color: #F5F5F5;
        border-radius: 6px;
        font-weight: 500;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: #EEEEEE;
    }}
    
    /* JSON viewer */
    .stJson {{
        background-color: #F5F5F5;
        border-radius: 6px;
        padding: 12px !important;
    }}
    
    /* Alerts and messages */
    .stAlert {{
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 14px;
    }}
    
    /* Driver Card - Premium Styling */
    .driver-card {{
        background: linear-gradient(135deg, #FAFAFA 0%, #F5F5F5 100%);
        border: 1px solid #E8E8E8;
        border-radius: 12px;
        padding: 24px;
        font-size: 14px;
        line-height: 1.8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        transition: all 0.3s ease;
    }}
    
    .driver-card:hover {{
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }}
    
    .driver-section {{
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid #E0E0E0;
    }}
    
    .driver-section:last-child {{
        border-bottom: none;
        margin-bottom: 0;
    }}
    
    .driver-label {{
        font-weight: 700;
        color: #333;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        color: #FFE000;
    }}
    
    .driver-value {{
        color: #000;
        font-weight: 500;
        word-break: break-word;
    }}
    
    .driver-value.landmarks {{
        line-height: 1.6;
        margin-top: 8px;
    }}
    
    .driver-value.coordinates {{
        font-family: 'Courier New', monospace;
        background-color: #F0F0F0;
        padding: 8px 12px;
        border-radius: 6px;
        color: #D84315;
        font-weight: 600;
    }}
    
    /* Navigation Button - Premium CTA */
    .navigation-button {{
        display: inline-block;
        background: linear-gradient(135deg, #FFE000 0%, #FFC700 100%);
        color: #000;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 14px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        box-shadow: 0 4px 12px rgba(255, 224, 0, 0.3);
        cursor: pointer;
        display: block;
        text-align: center;
        margin-top: 16px;
    }}
    
    .navigation-button:hover {{
        background: linear-gradient(135deg, #FFC700 0%, #FFB700 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 224, 0, 0.4);
        text-decoration: none;
        color: #000;
    }}
    
    .navigation-button:active {{
        transform: translateY(0);
    }}
    
    /* Info Icon */
    .info-icon {{
        display: inline-block;
        width: 18px;
        height: 18px;
        background-color: #FFE000;
        color: #000;
        border-radius: 50%;
        text-align: center;
        line-height: 18px;
        font-weight: bold;
        font-size: 12px;
        cursor: help;
        margin-left: 8px;
        transition: all 0.2s ease;
    }}
    
    .info-icon:hover {{
        background-color: #FFC700;
        transform: scale(1.1);
    }}
    
    /* Pipeline Stage Animation */
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes slideUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes fadeIn {{
        from {{
            opacity: 0;
        }}
        to {{
            opacity: 1;
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
        }}
        50% {{
            opacity: 0.7;
        }}
    }}
    
    .animate-slide-up {{
        animation: slideUp 0.6s ease-out;
    }}
    
    .animate-fade-in {{
        animation: fadeIn 0.5s ease-out forwards;
        opacity: 0;
    }}
    
    .pipeline-stage {{
        animation: slideIn 0.5s ease-out forwards;
    }}
    
    .pipeline-stage:nth-child(1) {{
        animation-delay: 0s;
    }}
    
    .pipeline-stage:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    
    .pipeline-stage:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    
    /* Stage card styling */
    .stExpander {{
        background-color: #F5F5F5;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
    }}
    
    /* Pulse animation for status indicators */
    .status-pulse {{
        animation: pulse 2s ease-in-out infinite;
    }}
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_logo_placeholder() -> None:
    """Render Noon logo placeholder in sidebar."""
    st.markdown(
        """
    <div style="text-align: center; margin: 20px 0;">
        <div style="
            background: linear-gradient(135deg, #FFE000 0%, #FFC000 100%);
            width: 80px;
            height: 80px;
            margin: 0 auto;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 36px;
            color: #000;
            box-shadow: 0 4px 8px rgba(255, 224, 0, 0.3);
        ">
            N
        </div>
        <p style="margin-top: 10px; font-weight: 700; font-size: 14px;">NOON</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_sidebar_metrics(metrics: Dict[str, str], language: str = "en") -> None:
    """Render system metrics in sidebar."""
    
    for metric_name, metric_value in metrics.items():
        st.sidebar.markdown(
            f"""
        <div class="metric-box">
            <div style="font-size: 11px; color: #666;">{metric_name}</div>
            <div style="font-size: 14px; color: #000; margin-top: 4px;">{metric_value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def _clean_for_display(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove empty string and empty list fields for clean JSON display."""
    out = {}
    for k, v in data.items():
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        if isinstance(v, list) and len(v) == 0:
            continue
        out[k] = v
    return out


def render_delivery_card(
    resolved_data: Dict[str, Any], inference_time_ms: float, language: str = "en"
) -> None:
    """Render delivery card output with simple text display and Google Maps navigation."""
    import json
    
    # Generate Google Maps link
    lat = resolved_data['geo_coordinates']['latitude']
    lon = resolved_data['geo_coordinates']['longitude']
    google_maps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}&travelmode=driving"
    
    col_left, col_right = st.columns(2, gap="medium")
    
    with col_left:
        st.markdown(f"#### {t('output_payload', language)}")
        display_data = _clean_for_display(resolved_data)
        st.code(json.dumps(display_data, indent=2, ensure_ascii=False), language="json")
    
    with col_right:
        st.markdown(f"#### {t('output_driver', language)}")
        
        # Helper function to display field
        def show_field(label: str, value: str):
            """Show field only if it has content."""
            if value and str(value).strip():
                st.write(f"**{label}:** {value}")
        
        # Display as clean text info
        neighborhood = resolved_data.get('neighborhood', '').strip()
        building = resolved_data.get('building', '').strip()
        floor_unit = resolved_data.get('floor_unit', '').strip()
        instructions = resolved_data.get('instructions', '').strip()
        landmarks = resolved_data.get('landmarks', [])
        
        if neighborhood:
            st.write(f"**Location:** {neighborhood}")
        if building:
            st.write(f"**Building:** {building}")
        if floor_unit:
            st.write(f"**Floor/Unit:** {floor_unit}")
        
        if landmarks:
            st.write("**Key Landmarks:**")
            for landmark in landmarks:
                if landmark and str(landmark).strip():
                    st.write(f"  • {landmark}")
        
        if instructions:
            st.write(f"**Delivery Instructions:** {instructions}")
        
        st.write(f"**GPS Coordinates:** {lat}, {lon}")
        
        # Navigation button
        st.markdown(f"[🗺️ Navigate on Google Maps]({google_maps_url})")
    
    # Footer with latency and info
    col_footer1, col_footer2, col_footer3 = st.columns([1, 2, 1])
    with col_footer2:
        st.markdown(
            f"<div style='text-align: center;'><span class='latency-badge'>{t('output_latency', language)}{inference_time_ms:.1f}{t('output_ms', language)}</span></div>",
            unsafe_allow_html=True,
        )


def render_warning_banner(risk_score: float, language: str = "en") -> None:
    """Render risk warning if needed."""
    if risk_score > 0.7:
        st.markdown(
            f"""
        <div class="warning-card">
            <strong>{t('warning_high', language)}</strong><br/>
            {t('risk_score', language)}<strong>{risk_score:.2%}</strong><br/>
            {t('requires_call', language)}
        </div>
        """,
            unsafe_allow_html=True,
        )
    elif risk_score > 0.4:
        st.markdown(
            f"""
        <div class="info-card">
            <strong>{t('warning_moderate', language)}</strong><br/>
            {t('risk_score', language)}<strong>{risk_score:.2%}</strong><br/>
            {t('moderate_ambiguity', language)}
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div class="success-card">
            <strong>{t('success_clear', language)}</strong><br/>
            {t('risk_score', language)}<strong>{risk_score:.2%}</strong><br/>
            {t('high_confidence', language)}
        </div>
        """,
            unsafe_allow_html=True,
        )


def render_pipeline_stages(stages: List[Dict[str, Any]], language: str = "en") -> None:
    """Render animated 3-stage pipeline visualization with info buttons."""
    st.markdown(f"### {t('pipeline_title', language)}")
    
    # Timeline visualization
    st.markdown("""
    <style>
    .pipeline-timeline {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 30px 0;
        position: relative;
    }
    
    .pipeline-timeline::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 5%;
        right: 5%;
        height: 2px;
        background: linear-gradient(90deg, #FFE000 0%, #FFE000 100%);
        z-index: 0;
    }
    
    .pipeline-dot {
        width: 40px;
        height: 40px;
        background: #FFE000;
        border: 3px solid #FFC700;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #000;
        z-index: 1;
        position: relative;
        box-shadow: 0 4px 12px rgba(255, 224, 0, 0.3);
    }
    
    .pipeline-label {
        font-weight: 700;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 12px;
        color: #FFE000;
    }
    
    .pipeline-stages-container {
        display: flex;
        gap: 20px;
        margin-top: 30px;
    }
    </style>
    
    <div class="pipeline-timeline">
        <div style="flex: 1; text-align: center;">
            <div class="pipeline-dot">1</div>
            <div class="pipeline-label">Entity Extraction</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div class="pipeline-dot">2</div>
            <div class="pipeline-label">Risk Assessment</div>
        </div>
        <div style="flex: 1; text-align: center;">
            <div class="pipeline-dot">3</div>
            <div class="pipeline-label">Geo-Mapping</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stage details with info buttons
    stage_configs = [
        {
            "key": "stage1",
            "title_key": "stage1_title",
            "desc_key": "stage1_desc",
            "info_key": "info_entity_extraction",
            "index": 0,
        },
        {
            "key": "stage2",
            "title_key": "stage2_title",
            "desc_key": "stage2_desc",
            "info_key": "info_risk_assessment",
            "index": 1,
        },
        {
            "key": "stage3",
            "title_key": "stage3_title",
            "desc_key": "stage3_desc",
            "info_key": "info_geo_mapping",
            "index": 2,
        },
    ]
    
    for config in stage_configs:
        stage = stages[config["index"]]
        col1, col2 = st.columns([10, 1])
        
        with col1:
            st.markdown(f"**{t(config['title_key'], language)}**")
        
        with col2:
            with st.popover("?", use_container_width=False):
                st.markdown(t(config['info_key'], language))
        
        with st.expander(t(config['desc_key'], language), expanded=True):
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.metric(
                    "Processing Time",
                    f"{stage['result']['inference_time_ms']:.2f}ms",
                )
            
            with col_b:
                if config["index"] == 1:  # Stage 2
                    st.metric(
                        t('stage2_risk', language),
                        f"{stage['result']['risk_score']:.2%}",
                        delta=t('stage2_high_risk', language) if stage['result']['requires_call'] else t('stage2_normal', language),
                    )
                else:
                    st.metric("Status", "Complete")
            
            # Stage-specific details
            if config["index"] == 0:
                st.markdown("**Extracted Entities:**")
                import json as _json
                entities_clean = _clean_for_display(stage['result']['entities'])
                st.code(_json.dumps(entities_clean, indent=2, ensure_ascii=False), language="json")
            
            elif config["index"] == 1:
                risk_score = stage['result']['risk_score']
                if risk_score > 0.7:
                    st.error("🚨 HIGH RISK - Customer verification REQUIRED. Address ambiguity detected.")
                elif risk_score > 0.4:
                    st.warning("⚠️ MODERATE RISK - Customer verification RECOMMENDED. Address has some ambiguity.")
                else:
                    st.success("✓ LOW RISK - Address is clear. Delivery can proceed directly.")
            
            elif config["index"] == 2:
                st.markdown("**Generated Coordinates:**")
                import json as _json
                st.code(_json.dumps(stage['result']['coordinates'], indent=2, ensure_ascii=False), language="json")
