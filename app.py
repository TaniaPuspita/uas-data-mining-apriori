import streamlit as st
import pandas as pd

# 1. Mengatur tampilan halaman web
st.set_page_config(page_title="Market Basket Analysis", page_icon="🛍️", layout="centered")

st.title("🛍️ Sistem Rekomendasi Produk Toko Groceries")
st.write("Aplikasi ini membantu pemilik toko menentukan penataan barang berdasarkan pola belanja pelanggan.")
st.markdown("---")

# 2. Membaca file CSV hasil dari Google Colab
try:
    df_rules = pd.read_csv('rules_terbaik.csv')
    
    # Fungsi pembersihan karakter frozenset khusus untuk file kamu
    def clean_item(text):
        return text.replace("frozenset({", "").replace("})", "").replace("'", "").replace('"', "").strip()

    df_rules['antecedents'] = df_rules['antecedents'].apply(clean_item)
    df_rules['consequents'] = df_rules['consequents'].apply(clean_item)

    # 3. Fitur Utama: Memilih Produk
    st.subheader("Pilih Produk yang Dibeli Pelanggan:")
    daftar_produk = sorted(df_rules['antecedents'].unique())
    produk_pilihan = st.selectbox("Cari atau pilih item:", daftar_produk)

    # 4. Tombol untuk Memunculkan Rekomendasi
    if st.button("Cek Rekomendasi Kombinasi Produk"):
        # Cari pasangan produk di dalam dataframe
        hasil = df_rules[(df_rules['antecedents'] == produk_pilihan) & (df_rules['lift'] > 1)]
        
        if not hasil.empty:
            st.success("### 🔥 Rekomendasi Strategi Toko:")
            for index, row in hasil.iterrows():
                item_rekomendasi = row['consequents']
                nilai_confidence = row['confidence'] * 100
                nilai_lift = row['lift']
                
                st.write(f"👉 Pasangkan atau letakkan produk **{item_rekomendasi.upper()}** di dekat produk **{produk_pilihan.upper()}**.")
                st.info(f"💡 **Analisis:** Pelanggan yang membeli *{produk_pilihan}* memiliki peluang sebesar **{nilai_confidence:.1f}%** untuk membeli *{item_rekomendasi}* (Nilai Keterikatan Lift: {nilai_lift:.2f}).")
                st.markdown("---")
        else:
            st.warning("Belum ada aturan asosiasi yang kuat untuk produk ini.")

except FileNotFoundError:
    st.error("Gagal memuat data! Pastikan file 'rules_terbaik.csv' berada di folder yang sama dengan 'app.py'.")