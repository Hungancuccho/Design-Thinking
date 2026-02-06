import streamlit as st
import json
from pathlib import Path

# --- CẤU HÌNH VÀ DỮ LIỆU ---

st.set_page_config(layout="wide", page_title="Design Thinking Toolbox")

# Ánh xạ tool_id với icon tương ứng
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

# Cấu trúc layout của các công cụ
TOOL_LAYOUT = {
    "Difficult Zone — Understanding the problem": {
        "note": "Vấn đề còn “u tối”: cần thấu hiểu, quan sát và xác định góc nhìn (Point of View) trước khi bước sang sáng tạo.",
        "columns": {
            "Understand": ["problem_statement", "design_principles", "interview_for_empathy"],
            "Observe": ["empathy_map"],
            "Point of view": ["how_might_we"]
        }
    },
    "Creative Zone — From ideas to light": {
        "note": "Vùng sáng tạo: mở rộng giải pháp, hiện thực hóa mẫu thử, kiểm thử có cấu trúc và đúc kết để mở rộng quy mô.",
        "columns": {
            "Ideate": ["brainstorming"],
            "Prototype": [],
            "Test": []
        }
    }
}

# --- HÀM TẢI DỮ LIỆU ---

@st.cache
def load_tool_data(filepath: str) -> dict:
    """Tải dữ liệu công cụ từ file JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Lỗi: Không tìm thấy file `{filepath}`. Hãy chắc chắn bạn đã tạo file này.")
        return {}
    except json.JSONDecodeError:
        st.error(f"Lỗi: File `{filepath}` có định dạng JSON không hợp lệ.")
        return {}

# --- KHỞI TẠO STATE ---

if 'selected_tool' not in st.session_state:
    st.session_state.selected_tool = None

# --- GIAO DIỆN APP ---

# Tải dữ liệu
tool_data = load_tool_data('tool_data.json')
if not tool_data:
    st.stop() # Dừng app nếu không tải được dữ liệu

# Header
st.title("Design Thinking Toolbox 🧰")
st.caption("Thư viện công cụ & trợ lý gợi ý cho sinh viên | Prototype")

# Chia layout chính
detail_col, workspace_col = st.columns([2, 3]) # Tỉ lệ 40% - 60%

# --- CỘT BÊN PHẢI (WORKSPACE) ---
with workspace_col:
    # Tự động phân loại tools theo phase
    phases = {
        "Understand": [],
        "Observe": [],
        "Point of view": [],
        "Ideate": [],
        "Prototype": [],
        "Test": []
    }
    
    # Phân loại tools theo phase
    for tool_id, tool_info in tool_data.items():
        phase = tool_info.get('phase', '')
        if phase in phases:
            phases[phase].append(tool_id)
    
    # Hiển thị các zone
    zones = {
        "Difficult Zone — Understanding the problem": {
            "note": "Vấn đề còn 'u tối': cần thấu hiểu, quan sát và xác định góc nhìn (Point of View) trước khi bước sang sáng tạo.",
            "phases": ["Understand", "Observe", "Point of view"]
        },
        "Creative Zone — From ideas to light": {
            "note": "Vùng sáng tạo: mở rộng giải pháp, hiện thực hóa mẫu thử, kiểm thử có cấu trúc và đúc kết để mở rộng quy mô.",
            "phases": ["Ideate", "Prototype", "Test"]
        }
    }
    
    for zone_title, zone_content in zones.items():
        st.header(zone_title)
        st.write(zone_content['note'])
        
        # Tạo các cột con cho từng phase
        zone_phases = zone_content['phases']
        sub_cols = st.columns(len(zone_phases))
        
        for i, phase in enumerate(zone_phases):
            with sub_cols[i]:
                st.subheader(phase)
                tool_ids = phases.get(phase, [])
                for tool_id in tool_ids:
                    if tool_id in tool_data:
                        tool_info = tool_data[tool_id]
                        icon = ICON_MAP.get(tool_id, "❓")
                        # Nút bấm để chọn công cụ
                        if st.button(f"{icon} {tool_info['title']}", key=tool_id, use_container_width=True):
                            st.session_state.selected_tool = tool_id

# --- CỘT BÊN TRÁI (DETAIL) ---
with detail_col:
    st.header("Tool Detail")

    selected_id = st.session_state.selected_tool
    
    if selected_id and selected_id in tool_data:
        data = tool_data[selected_id]
        
        # Hiển thị nút Clear
        if st.button("❌ Clear Selection", use_container_width=True):
            st.session_state.selected_tool = None
            st.rerun() # Chạy lại app để cập nhật giao diện ngay lập tức

        # Hiển thị thông tin chi tiết
        st.subheader(data.get('title', 'N/A'))
        st.caption(f"Phase: {data.get('phase', '')}")

        with st.container(border=True):
            if data.get('short'):
                st.markdown(f"**{data['short']}**")
            if data.get('definition'):
                st.markdown(data['definition'])
            
            if data.get('howto'):
                st.markdown("**Quy trình**")
                for i, step in enumerate(data['howto'], 1):
                    st.markdown(f"{i}. {step}")
            
            if data.get('tips'):
                st.markdown("**Tips**")
                for tip in data['tips']:
                    st.markdown(f"- {tip}")

            if data.get('example'):
                st.markdown(f"**Ví dụ:** *{data['example']}*")
    else:
        st.info("👈 Chọn một công cụ từ danh sách bên phải để xem chi tiết.")

# --- RECOMMENDATION SYSTEM ---
st.divider()
st.header("🤖 Tool Recommendation System")

# Dropdowns cho phase, time, và size group
col1, col2, col3 = st.columns(3)

with col1:
    phase_options = ['Understand', 'Observe', 'Point of view', 'Ideate', 'Prototype', 'Test']
    selected_phase = st.selectbox("🎯 Chọn Phase", phase_options)

with col2:
    time_options = ['short', 'medium', 'long']
    selected_time = st.selectbox("⏱️ Chọn Thời gian", time_options)

with col3:
    size_group_options = ['small (2-5)', 'medium (6-10)', 'large (10+)']
    selected_size_group = st.selectbox("👥 Chọn Nhóm size", size_group_options)

# Nút Get Recommendations
if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
    # Lọc công cụ theo lựa chọn
    filtered_tools = []
    for tool_id, tool_info in tool_data.items():
        if (tool_info.get('phase') == selected_phase and
            tool_info.get('time') == selected_time and
            tool_info.get('size_group') == selected_size_group):
            filtered_tools.append(tool_id)

    # Hiển thị các công cụ lọc được
    if filtered_tools:
        st.success(f"🎉 Tìm thấy {len(filtered_tools)} công cụ phù hợp:")
        for tool_id in filtered_tools:
            tool_info = tool_data[tool_id]
            icon = ICON_MAP.get(tool_id, "❓")
            
            with st.expander(f"{icon} {tool_info['title']}", expanded=False):
                st.markdown(f"**Phase:** {tool_info['phase']} | **Time:** {tool_info['time']} | **Size:** {tool_info['size_group']}")
                st.markdown(f"**Mô tả:** {tool_info['short']}")
                if st.button(f"📋 Xem chi tiết {tool_info['title']}", key=f"rec_{tool_id}"):
                    st.session_state.selected_tool = tool_id
                    st.rerun()
    else:
        st.warning("⚠️ Không có công cụ phù hợp với lựa chọn của bạn. Hãy thử thay đổi tiêu chí.")
