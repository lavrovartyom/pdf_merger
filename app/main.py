import streamlit as st
from merger import merge_pdfs


def reset_state():
    """Сброс состояния и обновление страницы."""
    st.session_state.files = []
    st.session_state.result = None
    st.session_state.uploader_key += 1
    st.rerun()


def process_merge():
    """Запуск объединения PDF и отображение прогресса."""
    files = st.session_state.files
    total = len(files)
    progress = st.progress(0, text="Склеиваем файлы...")

    for i, _ in enumerate(files, start=1):
        progress.progress(i / total, text=f"Добавлено {i}/{total}")
    st.session_state.result = merge_pdfs(files)
    progress.progress(1.0, text="✅ Готово!")


st.set_page_config(page_title="PDF Merger", page_icon="📄", layout="centered")

st.session_state.setdefault("uploader_key", 0)
st.session_state.setdefault("files", [])
st.session_state.setdefault("result", None)

st.title("📄 Склейка PDF-файлов")
st.caption("Загрузи несколько PDF и получи один объединённый документ")

uploaded = st.file_uploader(
    "Выбери или перетащи файлы (до 200 МБ каждый)",
    type=["pdf"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}",
)
if uploaded:
    st.session_state.files = uploaded

if not st.session_state.files:
    st.info("Загрузи хотя бы один PDF, чтобы начать работу.")
    st.stop()

st.divider()
st.subheader("Действия")

merge_col, clear_col = st.columns([3, 1])

with merge_col:
    if st.button("🚀 Объединить файлы", use_container_width=True):
        process_merge()

with clear_col:
    if st.button("🧹 Очистить", use_container_width=True, type="primary"):
        reset_state()

if st.session_state.result:
    st.divider()
    st.download_button(
        "📥 Скачать объединённый PDF",
        st.session_state.result,
        file_name="merged.pdf",
        use_container_width=True,
    )

st.divider()
st.markdown(
    """
    <div style="text-align:center; opacity:0.6; font-size:0.9em;">
      Сделано на Python 3.13 + Streamlit + UV<br>
    </div>
    """,
    unsafe_allow_html=True,
)
