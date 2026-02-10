import streamlit as st
import pandas as pd
import io
import requests
import base64

# Set page settings
st.set_page_config(
    page_title="Land Record Search System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False


# Fixed values
# Update to XLSX export URL to support multiple sheets
DATA_URL = "https://docs.google.com/spreadsheets/d/1lpzFNKk0thSQqS8GQxzwiuLr8T9abM7M/export?format=xlsx"

# Dictionary for languages
TRANSLATIONS = {
    'NP': {
        'header_title': "भू-उपयोग क्षेत्र वर्गीकरण खोज प्रणाली",
        'sidebar_title': "फिल्टरहरू र नियन्त्रणहरू",
        'refresh_button': "डाटा रिफ्रेस गर्नुहोस्",
        'loading_msg': "तथ्याङ्क लोड हुँदैछ...",
        'connection_error': "तथ्याङ्क लोड गर्न सकिएन। कृपया इन्टरनेट जडान जाँच गर्नुहोस् वा पुनः प्रयास गर्नुहोस्।",
        'total_results': "जम्मा नतिजा",
        'kit_number': "कित्ता नं.",
        'vdc': "साविक गा.",
        'ward': "वडा नं.",
        'sheet_no': "सिट नं.",
        'land_use': "भूउपयोग क्षेत्र",
        'select_placeholder': "टाईप गर्नुहोस् या छान्नुहोस्",
        'search_placeholder': "यहाँ टाईप गर्नुहोस्...",
        'missing_cols_msg': "केही columns फेला परेनन्",
        'available_cols_msg': "उपलब्ध columns",
        'select_sheet': "साविक गा.वि.स. चयन गर्नुहोस् (Select a VDC)"
    },
    'EN': {
        'header_title': "Land Use Classification Search System",
        'sidebar_title': "Filters & Controls",
        'refresh_button': "Refresh Data",
        'loading_msg': "Loading Data...",
        'connection_error': "Could not load data. Please check internet connection or try again.",
        'total_results': "Total Results",
        'kit_number': "Plot/Kitta No.",
        'vdc': "VDC",
        'ward': "Ward No.",
        'sheet_no': "Sheet No.",
        'land_use': "Land Use",
        'select_placeholder': "Type or Select",
        'search_placeholder': "Type here to search...",
        'missing_cols_msg': "Some columns missing",
        'available_cols_msg': "Available Columns",
        'select_sheet': "Select Sheet"
    }
}

# This function gets data
@st.cache_data(ttl=600, show_spinner=False)
def load_all_sheets():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status()
        # Read the Excel file into a dictionary of DataFrames
        # We read without header first to detect the correct header row
        xls = pd.read_excel(io.BytesIO(response.content), sheet_name=None, header=None)
        return xls
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def find_header_row(df):
    """
    Search first 10 rows to find a row that looks like a header (contains at least 2 keywords).
    """
    keywords = ['कित्ता', 'साविक', 'वडा', 'सिट', 'भूउपयोग', 'सि.नं.', 'Plot', 'Ward', 'Sheet', 'VDC']
    for i in range(min(10, len(df))):
        row_values = df.iloc[i].astype(str).tolist()
        match_count = sum(1 for val in row_values if any(k.lower() in val.lower() for k in keywords))
        if match_count >= 2:
            return i
    return 0

def identify_columns(df):
    """
    Heuristically identify required columns from the dataframe.
    """
    cols = df.columns.tolist()
    mapping = {
        'vdc': None,
        'ward': None,
        'sheet_no': None,
        'plot': None,
        'land_use': None
    }
    
    # Heuristic rules (keywords)
    keywords = {
        'vdc': ['साविक गा', 'साविक', 'गा.वि.स', 'VDC', 'Municipality', 'Gapa', 'Napa'],
        'ward': ['वडा', 'वडा नं', 'Ward', 'Ward No'],
        'sheet_no': ['सिट नं', 'सिट', 'Sheet', 'Sheet No'],
        'plot': ['कित्ता', 'कित्ता नं', 'Plot', 'Kitta', 'Kitta No'],
        'land_use': ['भूउपयोग क्षेत्र', 'भूउपयोग', 'Land Use', 'Classification']
    }
    
    for key, patterns in keywords.items():
        for col in cols:
            col_str = str(col).strip()
            if any(p.lower() in col_str.lower() for p in patterns):
                mapping[key] = col
                break
    
    return mapping

# Helper to encode image for robust HTML display
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return None

def main():
    # Button to switch language
    # Start with Nepali language
    lang_choice = st.sidebar.radio("भाषा (Language)", options=["नेपाली", "English"], horizontal=True)
    lang_code = 'NP' if lang_choice == "नेपाली" else 'EN'
    t = TRANSLATIONS[lang_code]

    # Dynamic animation name to force re-triggering on language change
    anim_name = f"textFadeIn_{lang_code}"
    
    # Define theme colors based on state
    if st.session_state.dark_mode:
        bg_color = "#0E1117"
        sidebar_bg = "#262730"
        text_color = "#FAFAFA"
        input_bg = "#2C2F36"
        card_bg = "#1E1E1E"
    else:
        bg_color = "#FFFFFF"
        sidebar_bg = "#F0F2F6"
        text_color = "#31333F"
        input_bg = "#FFFFFF"
        card_bg = "#FFFFFF"

    # Custom CSS for UI Animations & Theme Toggle
    st.markdown(f"""
    <style>
        /* Theme Colors */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
            animation: fadeIn 0.8s ease-in-out;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            transition: all 0.3s ease;
        }}
        
        /* Text colors - comprehensive coverage */
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, a {{
            color: {text_color} !important;
        }}
        
        /* Ensure markdown text is visible */
        .stMarkdown, .stMarkdown p, .stMarkdown span {{
            color: {text_color} !important;
        }}
        
        /* Input fields - background and text */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            transition: background-color 0.3s ease;
            border-color: {text_color}40 !important;
        }}
        
        /* Dropdown menu items */
        div[data-baseweb="select"] ul {{
            background-color: {input_bg} !important;
        }}
        
        div[data-baseweb="select"] li {{
            background-color: {input_bg} !important;
            color: {text_color} !important;
            opacity: 1 !important;
        }}
        
        div[data-baseweb="select"] li span {{
            color: {text_color} !important;
            opacity: 1 !important;
        }}
        
        div[data-baseweb="select"] li:hover {{
            background-color: {text_color}20 !important;
        }}
        
        /* Selected option in dropdown */
        div[data-baseweb="select"] [aria-selected="true"] {{
            background-color: #4CAF50 !important;
            color: #FFFFFF !important;
        }}
        
        /* Currently displayed value in dropdown input */
        div[data-baseweb="select"] input {{
            color: {text_color} !important;
        }}
        
        /* Input placeholder text */
        input::placeholder, textarea::placeholder {{
            color: {text_color}60 !important;
        }}
        
        /* DataFrame/Table text visibility */
        div[data-testid="stDataFrame"] {{
            color: {text_color} !important;
            background-color: {bg_color} !important;
        }}
        
        div[data-testid="stDataFrame"] table {{
            color: {text_color} !important;
            background-color: {bg_color} !important;
        }}
        
        div[data-testid="stDataFrame"] th,
        div[data-testid="stDataFrame"] td {{
            color: {text_color} !important;
            background-color: {bg_color} !important;
        }}
        
        /* Force table container backgrounds */
        div[data-testid="stDataFrame"] > div {{
            background-color: {bg_color} !important;
        }}
        
        /* Table header row */
        div[data-testid="stDataFrame"] thead {{
            background-color: {bg_color} !important;
        }}
        
        div[data-testid="stDataFrame"] thead th {{
            background-color: {bg_color} !important;
            color: {text_color} !important;
        }}
        
        /* Table body */
        div[data-testid="stDataFrame"] tbody {{
            background-color: {bg_color} !important;
        }}
        
        div[data-testid="stDataFrame"] tbody tr {{
            background-color: {bg_color} !important;
        }}
        
        /* Warning and info boxes */
        .stAlert {{
            background-color: {card_bg} !important;
            color: {text_color} !important;
        }}
        
        /* Radio button labels */
        div[role="radiogroup"] label {{
            color: {text_color} !important;
        }}
        
        /* Ensure button text is always visible */
        button {{
            color: white !important;
        }}
        
        /* Tooltip text - make it darker in light mode */
        div[data-baseweb="tooltip"] {{
            color: #000000 !important;
            opacity: 1 !important;
        }}
        
        div[data-baseweb="tooltip"] * {{
            color: #000000 !important;
            opacity: 1 !important;
        }}
        
        /* Sidebar text elements */
        section[data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}
        
        /* Toggle Switch Container - Top Right */
        .theme-toggle-container {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999999;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        /* Toggle Switch */
        .theme-switch {{
            position: relative;
            display: inline-block;
            width: 60px;
            height: 30px;
        }}
        
        .theme-switch input {{
            opacity: 0;
            width: 0;
            height: 0;
        }}
        
        .slider {{
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            transition: 0.3s;
            border-radius: 30px;
        }}
        
        .slider:before {{
            position: absolute;
            content: "";
            height: 22px;
            width: 22px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            transition: 0.3s;
            border-radius: 50%;
        }}
        
        input:checked + .slider {{
            background-color: #2196F3;
        }}
        
        input:checked + .slider:before {{
            transform: translateX(30px);
        }}
        
        /* Icons in toggle */
        .slider:after {{
            content: '☀️';
            position: absolute;
            left: 8px;
            top: 4px;
            font-size: 16px;
        }}
        
        input:checked + .slider:after {{
            content: '🌙';
            left: auto;
            right: 8px;
        }}
        
        /* Style the theme toggle button */
        button[key="theme_toggle"] {{
            position: fixed !important;
            top: 10px !important;
            right: 10px !important;
            z-index: 999999 !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            border-radius: 50px !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 24px !important;
            cursor: pointer !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }}
        
        button[key="theme_toggle"]:hover {{
            transform: scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.3) !important;
        }}

        /* Smooth Transitions for Buttons */
        div.stButton > button {{
            transition: all 0.3s ease !important;
            border-radius: 8px !important;
        }}
        div.stButton > button:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        /* Dropdown & Input Animation */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
        }}
        div[data-baseweb="select"]:hover,
        div[data-baseweb="input"]:hover {{
            transform: translateY(-1px);
        }}

        /* Dropdown Menu Items (Popovers) */
        li[data-baseweb="menu-item"], div[data-baseweb="menu-item"] {{
            transition: background-color 0.2s ease !important;
        }}

        /* DataFrame/Table styling - Subtler, Faster Animation for "Reflow" feel */
        div[data-testid="stDataFrame"] {{
            transition: opacity 0.3s ease;
            animation: slideUp 0.4s ease-out;
        }}
        @keyframes slideUp {{
            0% {{ transform: translateY(10px); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}

        /* Metric/Card hover effects */
        div[data-testid="metric-container"] {{
            transition: transform 0.2s ease;
        }}
        div[data-testid="metric-container"]:hover {{
            transform: translateY(-2px);
        }}

        /* Smooth Text Transitions for Language Change */
        /* We change the animation name based on language to FORCE it to replay */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stButton button, div[data-baseweb="select"] div, span {{
            animation: {anim_name} 0.6s ease-in-out;
        }}

        @keyframes {anim_name} {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}

        /* Smooth transition for the whole sidebar */
        section[data-testid="stSidebar"] > div {{
             transition: all 0.5s ease-in-out;
        }}

        /* Header Image Styling */
        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}
        .block-container {{
            padding-top: 1rem !important;
        }}
        /* Header Image Styling - Final Centering Attempt */
        .header-wrapper {{
            text-align: center !important;
            width: 100% !important;
            margin-top: -4.5rem !important;
            margin-bottom: 0.5rem !important;
            display: block !important;
        }}
        
        /* Force the Streamlit image container to be inline-block so it centers via text-align */
        .header-wrapper [data-testid="stImage"] {{
            display: inline-block !important;
            margin: 0 auto !important;
        }}

        .header-wrapper img {{
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            max-height: 160px !important;
            width: auto !important;
            object-fit: contain;
        }}

        /* Adjust main title margin and centering */
        .main-title {{
            margin-top: 0.5rem !important;
            text-align: center;
            width: 100%;
        }}
        
        .header-container-final {{
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            margin-top: -1.5rem !important; /* Moved down from -4.5rem */
            margin-bottom: 0.5rem !important;
        }}
        
        .header-img-final {{
            width: 500px !important;
            max-height: 160px !important;
            object-fit: contain;
            border-radius: 0 !important; /* Removed rounded corners */
            box-shadow: none !important; /* Removed shadow */
        }}
    </style>
""", unsafe_allow_html=True)


    # Display Header Image using direct HTML for perfect centering
    header_base64 = get_image_base64("static/header.jpeg")
    if header_base64:
        st.markdown(
            f'''
            <div class="header-container-final">
                <img src="data:image/jpeg;base64,{header_base64}" class="header-img-final">
            </div>
            ''',
            unsafe_allow_html=True
        )
    else:
        # Fallback if file not found
        st.image("static/header.jpeg", width=500)

    # Theme Toggle Button - Top Right Corner
    col1, col2 = st.columns([6, 1])
    with col2:
        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(theme_icon, key="theme_toggle", help="Toggle Dark/Light Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown(f'<h1 class="main-title">{t["header_title"]}</h1>', unsafe_allow_html=True)

    # Get the data now
    with st.spinner(t['loading_msg']):
        all_sheets = load_all_sheets()

    if all_sheets:
        # Side menu for options
        st.sidebar.title(t['sidebar_title'])
        
        # Sheet Selection
        # Skip the first sheet (Cover Page)
        sheet_names = list(all_sheets.keys())[1:] if len(all_sheets) > 1 else list(all_sheets.keys())
        selected_sheet_name = st.sidebar.selectbox(
            t['select_sheet'],
            sheet_names,
            index=0 if len(sheet_names) == 1 else None,
            placeholder=t['select_placeholder']
        )

        # Button to get new data
        if st.sidebar.button(t['refresh_button'], type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        st.sidebar.divider()

        if selected_sheet_name:
            df = all_sheets[selected_sheet_name].copy()
            
            # Find the correct header row
            header_row_idx = find_header_row(df)
            
            # Re-assign data and headers
            new_header = df.iloc[header_row_idx]
            df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
            df.columns = new_header
            
            # Fix column names, remove spaces
            df.columns = df.columns.astype(str).str.strip()
            
            # Delete bad columns starting with Unnamed or nan
            df = df.loc[:, ~(df.columns.str.contains('^Unnamed') | (df.columns == 'nan'))]
            
            # Dynamically identify columns
            col_mapping = identify_columns(df)
            col_vdc = col_mapping['vdc']
            col_ward = col_mapping['ward']
            col_sheet = col_mapping['sheet_no']
            col_plot = col_mapping['plot']
            col_land_use = col_mapping['land_use']
            
            available_columns = df.columns.tolist()

            # Make filters work
            filtered_df = df.copy()

            # 1. Filter for Ward
            if col_ward:
                ward_options = sorted(df[col_ward].dropna().astype(str).unique().tolist())
                selected_ward = st.sidebar.selectbox(
                    t['ward'], 
                    ward_options, 
                    index=None, 
                    placeholder=t['select_placeholder']
                )
                if selected_ward:
                    filtered_df = filtered_df[filtered_df[col_ward].astype(str) == selected_ward]
            
            # 2. Filter for Sheet No (depends on Ward)
            if col_sheet:
                sheet_options = sorted(filtered_df[col_sheet].dropna().astype(str).unique().tolist())
                selected_sheet = st.sidebar.selectbox(
                    t['sheet_no'], 
                    sheet_options, 
                    index=None, 
                    placeholder=t['select_placeholder']
                )
                if selected_sheet:
                    filtered_df = filtered_df[filtered_df[col_sheet].astype(str) == selected_sheet]
            
            # 3. Filter for Plot (Text Input)
            if col_plot:
                search_plot = st.sidebar.text_input(
                    t['kit_number'],
                    placeholder=t['search_placeholder']
                )
                if search_plot:
                    filtered_df = filtered_df[filtered_df[col_plot].astype(str).str.contains(search_plot, case=False, na=False)]
            
            # Put important columns first
            found_cols = [c for c in [col_plot, col_ward, col_sheet] if c]
            other_cols = [c for c in filtered_df.columns if c not in found_cols]
            final_cols = found_cols + other_cols
            filtered_df = filtered_df[final_cols]

            # Show the table
            st.write(f"जम्मा नतिजा (Total Results): {len(filtered_df)}")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=520)
            
            # Help fix if columns missing
            missing_cols = []
            if not col_ward: missing_cols.append(t['ward'])
            if not col_sheet: missing_cols.append(t['sheet_no'])
            if not col_plot: missing_cols.append(t['kit_number'])
            if not col_land_use: missing_cols.append(t['land_use'])

            if missing_cols:
                st.warning(f"केही स्तम्भहरू फेला परेनन् (Some columns missing): {', '.join(missing_cols)}")
                st.info(f"उपलब्ध स्तम्भहरू (Available Columns): {', '.join(available_columns)}")
        else:
            st.info("कृपया डेटा हेर्नको लागि एउटा साविक गा.वि.स. चयन गर्नुहोस्। (Please select a VDC to view data.)")

if __name__ == "__main__":
    main()
