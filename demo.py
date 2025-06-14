import streamlit as st
import json

# Cấu hình trang
st.set_page_config(page_title="Anime Watcher", layout="wide")

# Tải dữ liệu anime từ file JSON
try:
    with open("anime_data.json") as f:
        anime_list = json.load(f)
except FileNotFoundError:
    st.error("Không tìm thấy file dữ liệu anime. Vui lòng tạo file 'anime_data.json' với dữ liệu cần thiết.")
    st.stop()

# Thanh bên (sidebar)
st.sidebar.header("Anime Watcher")
search_term = st.sidebar.text_input("Tìm kiếm anime")

# Lọc danh sách anime dựa trên từ khóa tìm kiếm
filtered_anime = [anime for anime in anime_list if search_term.lower() in anime["title"].lower()]

if filtered_anime:
    # Hiển thị hộp chọn với các tiêu đề đã lọc
    selected_title = st.sidebar.selectbox("Chọn một anime", [anime["title"] for anime in filtered_anime])
    # Tìm dữ liệu của anime được chọn
    selected_data = next(anime for anime in filtered_anime if anime["title"] == selected_title)
    
    # Khu vực chính
    st.title(selected_data["title"])
    st.write(selected_data["description"])
    # Nhúng video YouTube
    st.components.v1.html(
        f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{selected_data["video_id"]}" frameborder="0" allowfullscreen></iframe>',
        width=560, height=315
    )
else:
    st.write("Không tìm thấy anime nào phù hợp với từ khóa tìm kiếm.")
