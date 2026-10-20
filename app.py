
import streamlit as st

# ページの設定（ワイドレイアウト）
st.set_page_config(
    page_title="議会リアルタイム文字起こし＆答弁支援システム",
    layout="wide",
    initial_sidebar_state="expanded"
)

# スタイルの調整（ハイライトや見やすさの向上）
st.markdown("""
<style>
    .highlight-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 4px;
    }
    .qa-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    .no-match {
        color: #dc3545;
        font-weight: bold;
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# タイトル
st.title("🏛️ 議場リアルタイム文字起こし ＆ 答弁支援ダッシュボード")
st.caption("※想定QAデータベース（PDF等）の厳格な情報のみに基づいて答弁案を提示します。")

# 画面を左右に分割（左：リアルタイム文字起こし、右：答弁支援・QA照合）
col_left, col_right = st.columns([1, 1], gap="medium")

# --- 左側：リアルタイム文字起こしログ ---
with col_left:
    st.subheader("🗣️ リアルタイム文字起こし（議場音声）")
    
    # 接続・ステータス表示
    st.success("🟢 録音・文字起こしエンジン稼働中（接続安定）")
    
    # 文字起こしログを表示するエリア
    log_container = st.container(height=500)
    
    with log_container:
        st.markdown("**[11:02:15] 議長（山田議員）：** 次に、一般質問を許可します。佐藤議員の登壇を求めます。")
        st.markdown("**[11:02:45] 佐藤議員：** 子育て世帯の定住促進について、現在の市内共通クーポン券の利用実績と、次年度の拡充予定について当局の見解を伺います。")
        
        # ハイライト対象の質問
        st.markdown("""
        <div class="highlight-box">
        <b>[11:03:10] 佐藤議員（質問中）：</b><br>
        特に、子育て世帯への経済支援として、第2子以降の給付金上乗せや、保育料の完全無償化の対象拡大について、財源も含めてすぐにでも踏み込むべきと考えますが、市長の決裁はいかがですか？
        </div>
        """, unsafe_allow_html=True)

# --- 右側：データベースに基づく答弁支援 ---
with col_right:
    st.subheader("📋 答弁支援・想定QAデータベース照合")
    
    # 検索中・判定中のステータス
    st.info("🔍 直近の質問文から想定QAデータベースを検索中...")
    
    # タブ切り替え
    tab1, tab2 = st.tabs(["🎯 該当する想定QAと答弁案", "📚 データベース管理"])
    
    with tab1:
        st.markdown("#### 【ヒットした想定QA (一致度: 92%)】")
        st.markdown("""
        <div class="qa-card">
            <b>登録QA番号:</b> QA-2026-089<br>
            <b>想定質問:</b> 子育て世帯への経済支援（第2子以降の給付金・保育料無償化について）<br><hr>
            <b>📝 データベースに基づく答弁案:</b><br>
            「子育て世帯の経済的負担軽減につきましては、現在、国の動向や他自治体の実施状況を注視しているところでございます。第2子以降の給付金上乗せにつきましては、単年度の予算措置にとどまらず、持続可能な財政運営の観点から総合的に検証が必要であると考えており、現時点において即時の拡充についての具体的な決定には至っておりません。」<br><br>
            <small style="color: #6c757d;">📌 参照元: 令和8年度予算要望ヒアリング資料_p.42</small>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("ℹ️ 該当するQAがない場合の表示プレビュー"):
            st.markdown("""
            <div class="no-match">
            ⚠️ データベース内に該当する想定QAが存在しません。<br>
            （ハルシネーション防止のため、独自の推測による答弁案の生成は停止しています。）
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("#### 📁 格納されている想定QAデータベース（PDF群）")
        st.text("・令和8年度総合計画_QandA集.pdf (登録数: 142件)")
        st.text("・子育て施策_過去答弁ストック_2025.pdf (登録数: 88件)")
        st.text("・財務部_予算説明資料一覧.pdf (登録数: 215件)")
        
        if st.button("🔄 データベースを最新化（再インデックス）"):
            st.toast("データベースの同期が完了しました。", icon="✅")

# サイドバー：システム制御
with st.sidebar:
    st.header("⚙️ システムコントロール")
    session_mode = st.radio("動作モード", ["リアルタイム監視モード", "アーカイブ確認モード"])
    
    st.divider()
    st.subheader("🔒 セキュリティ設定")
    st.checkbox("セキュアAPIモード（外部学習なし）", value=True)
    st.checkbox("ハルシネーション防止フィルター（厳格）", value=True)
