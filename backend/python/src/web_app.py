import streamlit as st
import logic
import os

st.set_page_config(layout="wide", page_title="類似画像検索")
st.title("🔍 類似画像スキャン")

# セッション状態の初期化
if 'folder_path' not in st.session_state:
    st.session_state['folder_path'] = ""

with st.sidebar:
    st.header("設定")
    # 入力値をセッションに保存
    folder_input = st.text_input("スキャンするフォルダのパス", value=st.session_state['folder_path'])
    threshold = st.slider("類似度のしきい値", 0, 30, 8)

    col1, col2 = st.columns(2)
    with col1:
        scan_clicked = st.button("新規スキャン")
    with col2:
        # フォルダが入力されている時だけ再検索ボタンを出す
        rescan_clicked = st.button("🔄 再検索")

# 実行条件の判定
if (scan_clicked or rescan_clicked) and folder_input:
    if os.path.isdir(folder_input):
        st.session_state['folder_path'] = folder_input # パスを記憶

        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(current, total, filename):
            progress_bar.progress(current / total)
            status_text.text(f"スキャン中: {current}/{total}")

        # スキャン実行
        results = logic.find_duplicates(folder_input, threshold, progress_callback=update_progress)

        progress_bar.empty()
        status_text.empty()
        st.session_state['results'] = results
    else:
        st.error("フォルダパスが正しくありません。")

# 結果表示エリア
if 'results' in st.session_state and st.session_state['results']:
    st.write(f"### {len(st.session_state['results'])} 組の類似画像が見つかりました")

    for i, (a, b) in enumerate(st.session_state['results']):
        with st.container():
            col1, col2 = st.columns(2)

            # 画像ペアの表示
            for idx, img_path in enumerate([a, b]):
                with (col1 if idx == 0 else col2):
                    st.image(img_path, use_column_width=True)
                    st.caption(f"Path: {img_path}")

                    # ボタン配置用のサブカラム
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(f"🗑 削除", key=f"del_{img_path}_{i}"):
                            if logic.delete_file(img_path):
                                st.warning(f"削除しました: {os.path.basename(img_path)}")
                                # 実際は再描画が必要だが、まずは簡易的に
                    with btn_col2:
                        if st.button(f"📁 フォルダを開く", key=f"open_{img_path}_{i}"):
                            logic.open_folder_at_path(img_path)
            st.divider()
