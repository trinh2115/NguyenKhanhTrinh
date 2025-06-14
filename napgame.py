import streamlit as st
import json
import hashlib

# Định nghĩa file lưu trữ dữ liệu người dùng
USER_DATA_FILE = 'users.json'

# Hàm tải và lưu dữ liệu người dùng
def load_users():
    try:
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

# Hàm đăng ký
def register():
    with st.form('register_form'):
        st.subheader('Đăng Ký')
        username = st.text_input('Tên người dùng')
        password = st.text_input('Mật khẩu', type='password')
        confirm_password = st.text_input('Xác nhận mật khẩu', type='password')
        submit = st.form_submit_button('Đăng Ký')
        if submit:
            if password != confirm_password:
                st.error('Mật khẩu không khớp')
            else:
                users = load_users()
                if username in users:
                    st.error('Tên người dùng đã tồn tại')
                else:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    users[username] = hashed_password
                    save_users(users)
                    st.success('Đăng ký thành công. Vui lòng đăng nhập.')

# Hàm đăng nhập
def login():
    with st.form('login_form'):
        st.subheader('Đăng Nhập')
        username = st.text_input('Tên người dùng')
        password = st.text_input('Mật khẩu', type='password')
        submit = st.form_submit_button('Đăng Nhập')
        if submit:
            users = load_users()
            if username in users:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if users[username] == hashed_password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()  # Chuyển ngay sang trang nạp tiền
                else:
                    st.error('Mật khẩu không đúng')
            else:
                st.error('Tên người dùng không tồn tại')

# Hàm nạp tiền
def top_up():
    st.subheader(f'Chào mừng, {st.session_state.username}')
    game = st.selectbox('Chọn Game', ['Liên Quân', 'PUBG'])
    amount = st.number_input('Số tiền', min_value=1, step=1)
    if st.button('Nạp Tiền'):
        st.success(f'Nạp {amount} cho {game} thành công!')
    if st.button('Đăng Xuất'):
        st.session_state.logged_in = False
        st.session_state.username = ''
        st.rerun()

# Logic chính của ứng dụng
st.title('Trang Web Nạp Game')

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'username' not in st.session_state:
    st.session_state.username = ''

if not st.session_state.logged_in:
    choice = st.radio('Chọn', ['Đăng Nhập', 'Đăng Ký'])
    if choice == 'Đăng Nhập':
        login()
    else:
        register()
else:
    top_up()
