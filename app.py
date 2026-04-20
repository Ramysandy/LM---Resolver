"""Noon Last-Mile Resolver: AI Office Prototype - Main Streamlit Application."""

import streamlit as st
import asyncio
from typing import List
from config import (
    GROQ_API_KEY, SYSTEM_METRICS, SAMPLE_ADDRESSES, 
    SYSTEM_METRICS_AR, SAMPLE_ADDRESSES_AR, TRANSLATIONS
)
from groq_client import GroqAddressResolver, StressTestRunner
from address_resolver import AddressResolutionPipeline
from ui_components import (
    render_noon_branding,
    render_logo_placeholder,
    render_sidebar_metrics,
    render_delivery_card,
    render_warning_banner,
    render_pipeline_stages,
)


# Helper function to get translations
def t(key: str) -> str:
    """Get translated text. Falls back to English if key not found."""
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, {}).get(key, key)


# Page configuration
st.set_page_config(
    page_title="Noon Last-Mile Resolver",
    page_icon="N",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply Noon branding
render_noon_branding()

# Initialize session state
if "language" not in st.session_state:
    st.session_state.language = "en"
if "groq_resolver" not in st.session_state:
    st.session_state.groq_resolver = None
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None
if "stress_test_results" not in st.session_state:
    st.session_state.stress_test_results = None
if "address_input" not in st.session_state:
    st.session_state.address_input = ""


# ==============================================================================
# SIDEBAR: Language Toggle, Logo, Title, Metrics, API Configuration
# ==============================================================================
with st.sidebar:
    # Language Toggle Button (Top Right Corner Style)
    col_lang1, col_lang2, col_lang3 = st.columns([1, 1, 1.5])
    with col_lang3:
        if st.button(t("language_toggle"), use_container_width=True, key="lang_toggle"):
            st.session_state.language = "ar" if st.session_state.language == "en" else "en"
            st.rerun()
    
    st.markdown("---")
    
    render_logo_placeholder()
    
    st.markdown(f"## {t('sidebar_title')}")
    st.markdown("---")
    
    # System Metrics
    st.markdown(f"### {t('sidebar_metrics')}")
    
    current_metrics = SYSTEM_METRICS_AR if st.session_state.language == "ar" else SYSTEM_METRICS
    render_sidebar_metrics(current_metrics, st.session_state.language)


# ==============================================================================
# INITIALIZE GROQ RESOLVER (Background)
# ==============================================================================
# Auto-initialize from .env API key if not already done
if st.session_state.groq_resolver is None and GROQ_API_KEY:
    try:
        st.session_state.groq_resolver = GroqAddressResolver(api_key=GROQ_API_KEY)
        st.session_state.pipeline = AddressResolutionPipeline(st.session_state.groq_resolver)
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {str(e)}")


# ==============================================================================
# MAIN CONTENT
# ==============================================================================
col_title, col_info = st.columns([10, 1])

with col_title:
    st.title(t("main_title"))

with col_info:
    with st.popover("?", use_container_width=False):
        st.markdown(f"**Yellow Friday Challenge**")
        st.markdown(t("main_problem"))
        st.markdown("---")
        st.markdown(f"**Our AI Solution**")
        st.markdown(t("main_solution"))

st.markdown(f"### {t('main_subtitle')}")

# Display problem and solution context
with st.expander("📌 Yellow Friday Challenge & AI Solution", expanded=False):
    col_problem, col_solution = st.columns(2)
    
    with col_problem:
        st.markdown("**The Problem:**")
        st.markdown(t("main_problem"))
    
    with col_solution:
        st.markdown("**Our AI Solution:**")
        st.markdown(t("main_solution"))

st.markdown("---")

# Check if Groq is configured
if not st.session_state.groq_resolver:
    st.info(
        t("info_banner"),

    )
    st.stop()

# ==============================================================================
# INPUT SECTION
# ==============================================================================
col_input_title, col_input_info = st.columns([10, 1])

with col_input_title:
    st.markdown(f"## {t('input_section')}")

with col_input_info:
    with st.popover("?", use_container_width=False):
        st.markdown("**How to Use:**")
        st.markdown("Enter your delivery instructions exactly as provided by the customer.")
        st.markdown("Our AI will extract:")
        st.markdown("• Landmarks (pharmacies, banks, malls)")
        st.markdown("• Building and floor numbers")
        st.markdown("• Neighborhoods and locations")
        st.markdown("• GPS coordinates")
        st.divider()
        st.markdown("**Pro Tip:** The more details you provide, the more accurate our AI can be.")

# Create columns for input and quick actions
col_input, col_buttons = st.columns([3, 1], gap="medium")

with col_input:
    delivery_address = st.text_area(
        t("input_label"),
        value=st.session_state.address_input,
        placeholder=t("input_placeholder"),
        height=120,
        key="address_input",
    )

with col_buttons:
    st.markdown(f"### {t('quick_inject')}")
    
    # Get appropriate addresses based on language
    addresses = SAMPLE_ADDRESSES_AR if st.session_state.language == "ar" else SAMPLE_ADDRESSES
    address_keys = list(addresses.keys())
    
    # Define callback functions
    def select_address_0():
        addresses = SAMPLE_ADDRESSES_AR if st.session_state.language == "ar" else SAMPLE_ADDRESSES
        st.session_state.address_input = addresses[list(addresses.keys())[0]]
    
    def select_address_1():
        addresses = SAMPLE_ADDRESSES_AR if st.session_state.language == "ar" else SAMPLE_ADDRESSES
        st.session_state.address_input = addresses[list(addresses.keys())[1]]
    
    st.button(address_keys[0], use_container_width=True, on_click=select_address_0)
    st.button(address_keys[1], use_container_width=True, on_click=select_address_1)

# ==============================================================================
# RESOLVER ACTION BUTTON
# ==============================================================================
col_run, col_stress_test = st.columns(2)

with col_run:
    run_resolver = st.button(
        t("run_resolver"),
        use_container_width=True,
        type="primary",
        help=t("run_resolver_help"),
    )

with col_stress_test:
    enable_stress_test = st.checkbox(
        t("stress_test_toggle"),
        help=t("stress_test_help"),
    )

# ==============================================================================
# PROCESSING AND RESULTS
# ==============================================================================
if run_resolver and delivery_address:
    with st.status(t("processing_status"), expanded=True) as status:
        # Run the pipeline
        try:
            resolved_data, stages_data, total_time = (
                st.session_state.pipeline.process_address(delivery_address)
            )
            
            status.update(
                label=f"{t('processing_complete')} ({total_time:.1f}ms)",
                state="complete",
            )
            
            # Store results in session
            st.session_state.resolved_data = resolved_data
            st.session_state.stages_data = stages_data
            st.session_state.total_time = total_time
            
        except Exception as e:
            status.update(label=t("processing_error"), state="error")
            st.error(f"{t('processing_error_msg')}{str(e)}")
            st.stop()

# Display results if available
if "resolved_data" in st.session_state:
    st.markdown("---")
    
    # Warning banner based on risk score
    risk_score = st.session_state.resolved_data.get("risk_score", 0.5)
    render_warning_banner(risk_score, st.session_state.language)
    
    # Pipeline stages visualization
    render_pipeline_stages(st.session_state.stages_data, st.session_state.language)
    
    st.markdown("---")
    
    # Delivery card output
    st.markdown(f"## {t('output_section')}")
    render_delivery_card(st.session_state.resolved_data, st.session_state.total_time, st.session_state.language)

# ==============================================================================
# YELLOW FRIDAY STRESS TEST
# ==============================================================================
if enable_stress_test:
    st.markdown("---")
    st.markdown(f"## {t('stress_test_title')}")
    
    if st.button(t("stress_test_runbtn"), type="primary", use_container_width=True):
        with st.status(t("stress_test_running")) as status:
            try:
                # Create sample addresses for stress test
                addresses_base = SAMPLE_ADDRESSES_AR if st.session_state.language == "ar" else SAMPLE_ADDRESSES
                test_addresses = [
                    addresses_base.get(list(addresses_base.keys())[0]),
                    addresses_base.get(list(addresses_base.keys())[1]),
                    "Marina Dubai, near the promenade, building B, floor 15",
                    "King Road, Jeddah, close to the market, green building",
                    "Abu Dhabi, downtown, near the government building",
                    "Sharjah, Al Montaza area, behind the mall",
                    "Dammam, Corniche road, near the fountain",
                    "Riyadh, Olaya district, opposite the shopping center",
                    "Dubai, Bay Area, near the water front",
                    "Jeddah, Historical district, close to the port",
                ]
                
                # Run async stress test
                runner = StressTestRunner(st.session_state.groq_resolver, num_requests=10)
                
                # Use asyncio to run concurrent requests
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                results = loop.run_until_complete(
                    runner.run_concurrent_requests(test_addresses)
                )
                
                st.session_state.stress_test_results = results
                
                status.update(label=t("stress_test_complete"), state="complete")
                
            except Exception as e:
                status.update(label=t("stress_test_failed"), state="error")
                st.error(f"{t('stress_test_error')}{str(e)}")
    
    # Display stress test results if available
    if st.session_state.stress_test_results:
        results = st.session_state.stress_test_results
        
        st.markdown(t("stress_test_results"))
        
        # Metrics cards
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(t("stress_test_total"), results["num_requests"])
        
        with col2:
            st.metric(
                t("stress_test_time"),
                f"{results['total_time_ms']:.1f}",
            )
        
        with col3:
            st.metric(
                t("stress_test_avg"),
                f"{results['avg_inference_ms']:.1f}",
            )
        
        with col4:
            st.metric(t("stress_test_max"), f"{results['max_inference_ms']:.1f}")
        
        with col5:
            st.metric(
                t("stress_test_throughput"),
                f"{results['requests_per_second']:.2f}",
            )
        
        # Detailed results
        st.markdown(t("stress_test_detailed"))
        
        for idx, result in enumerate(results["results"], 1):
            with st.expander(f"{t('stress_test_request')}{idx}: {result.get('neighborhood', 'Unknown')}"):
                import json as _json
                st.code(_json.dumps(result, indent=2, ensure_ascii=False), language="json")


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown(
    f"""
<div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>
    {t('footer')}
</div>
""",
    unsafe_allow_html=True,
)
