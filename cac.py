import streamlit as st
import json
from pathlib import Path

st.set_page_config(layout="wide", page_title="Design Thinking Toolbox")

ICON_MAP = {
    "problem_statement": "📝", "design_principles": "📐", "interview_for_empathy": "🎤",
    "explorative_interview": "🔍", "ask_5x_why": "❓", "5w_h": "📝", "jobs_to_be_done": "⚒️",
    "extreme_lead_users": "🚀", "stakeholder_map": "👥", "emotional_response_cards": "🎴",
    "empathy_map": "🧩", "persona": "👤", "customer_journey": "🛤️", "aeiou": "📊",
    "analysis_question_builder": "❔", "peers_observing_peers": "👀", "trend_analysis": "📈",
    "how_might_we": "💡", "storytelling": "📖", "context_mapping": "🗺️", "define_success": "🏆",
    "vision_cone": "🔭", "critical_items_diagram": "⚠️",
    "brainstorming": "🤯", "2x2_matrix": "➗", "dot_voting": "🔘", "brainwriting": "✍️",
    "special_brainstorming": "💭", "analogies_benchmarking": "🔗", "nabc": "📦", "blue_ocean": "🌊",
}

# ---------- LOAD DATA (SAFE VERSION) ----------
def load_tool_data():
    path = Path(__file__).parent / "tool_data.json"
    if not path.exists():
        st.error("❌ Không tìm thấy file tool_data.json trong repo.")
        st.stop()
    with open(path, encoding="utf-8") as f:
        return json.load(f)

tool_data = load_tool_data()

# ---------- STATE ----------
if "selected_tool" not in st.session_state:
    st.session_state.selected_tool = None

# ---------- HEADER ----------
st.title("Design Thinking Toolbox 🧰")
st.caption("Thư viện công cụ & trợ lý gợi ý cho sinh viên | Prototype")

detail_col, workspace_col = st.columns([2, 3])

# ---------- WORKSPACE ----------
with workspace_col:
    phases = {
        "Understand": [],
        "Observe": [],
        "Point of view": [],
        "Ideate": [],
        "Prototype": [],
        "Test": []
    }

    for tool_id, tool_info in tool_data.items():
        phase = tool_info.get("phase", "")
        if phase in phases:
            phases[phase].append(tool_id)

    zones = {
        "Difficult Zone — Understanding the problem": {
            "note": "Vấn đề còn 'u tối': cần thấu hiểu, quan sát và xác định góc nhìn trước khi bước sang sáng tạo.",
            "phases": ["Understand", "Observe", "Point of view"]
        },
        "Creative Zone — From ideas to light": {
            "note": "Vùng sáng tạo: mở rộng giải pháp, hiện thực hóa mẫu thử, kiểm thử có cấu trúc.",
            "phases": ["Ideate", "Prototype", "Test"]
        }
    }

    for zone_title, zone_content in zones.items():
        st.header(zone_title)
        st.write(zone_content["note"])

        cols = st.columns(len(zone_content["phases"]))
        for i, phase in enumerate(zone_content["phases"]):
            with cols[i]:
                st.subheader(phase)
                for tool_id in phases.get(phase, []):
                    tool = tool_data[tool_id]
                    icon = ICON_MAP.get(tool_id, "❓")
                    if st.button(f"{icon} {tool['title']}", key=tool_id, use_container_width=True):
                        st.session_state.selected_tool = tool_id

# ---------- DETAIL ----------
with detail_col:
    st.header("Tool Detail")
    selected_id = st.session_state.selected_tool

    if selected_id and selected_id in tool_data:
        data = tool_data[selected_id]

        if st.button("❌ Clear Selection", use_container_width=True):
            st.session_state.selected_tool = None
            st.experimental_rerun()

        st.subheader(data.get("title", "N/A"))
        st.caption(f"Phase: {data.get('phase', '')}")

        with st.container(border=True):
            if data.get("short"):
                st.markdown(f"**{data['short']}**")
            if data.get("definition"):
                st.markdown(data["definition"])

            if data.get("howto"):
                st.markdown("**Quy trình**")
                for i, step in enumerate(data["howto"], 1):
                    st.markdown(f"{i}. {step}")

            if data.get("tips"):
                st.markdown("**Tips**")
                for tip in data["tips"]:
                    st.markdown(f"- {tip}")

            if data.get("example"):
                st.markdown(f"**Ví dụ:** *{data['example']}*")
    else:
        st.info("👈 Chọn một công cụ từ danh sách bên phải để xem chi tiết.")

# ---------- RECOMMENDER ----------
st.divider()
st.header("🤖 Tool Recommendation System")

col1, col2, col3 = st.columns(3)

with col1:
    selected_phase = st.selectbox("🎯 Chọn Phase", ["Understand", "Observe", "Point of view", "Ideate", "Prototype", "Test"])
with col2:
    selected_time = st.selectbox("⏱️ Chọn Thời gian", ["short", "medium", "long"])
with col3:
    selected_size_group = st.selectbox("👥 Chọn Nhóm size", ["small (2-5)", "medium (6-10)", "large (10+)"])

if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
    results = []
    for tool_id, tool in tool_data.items():
        if (
            tool.get("phase") == selected_phase and
            tool.get("time") == selected_time and
            tool.get("size_group") == selected_size_group
        ):
            results.append(tool_id)

    if results:
        st.success(f"🎉 Tìm thấy {len(results)} công cụ phù hợp:")
        for tool_id in results:
            tool = tool_data[tool_id]
            icon = ICON_MAP.get(tool_id, "❓")
            with st.expander(f"{icon} {tool['title']}"):
                st.markdown(f"**Phase:** {tool['phase']} | **Time:** {tool['time']} | **Size:** {tool['size_group']}")
                st.markdown(f"**Mô tả:** {tool['short']}")
                if st.button(f"📋 Xem chi tiết {tool['title']}", key=f"rec_{tool_id}"):
                    st.session_state.selected_tool = tool_id
                    st.experimental_rerun()
    else:
        st.warning("⚠️ Không có công cụ phù hợp với lựa chọn của bạn.")

