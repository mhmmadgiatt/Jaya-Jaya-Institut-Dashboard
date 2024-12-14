# Proyek Akhir: Meningkatkan Performa dan Retensi Mahasiswa di Jaya Jaya Institut

## Business Understanding

Jaya Jaya Institut adalah sebuah institusi pendidikan tinggi yang berfokus pada peningkatan kualitas pendidikan melalui pemanfaatan data. Salah satu tantangan yang dihadapi adalah rendahnya tingkat retensi mahasiswa dan ketidakjelasan faktor-faktor yang memengaruhi performa akademik siswa.

### Permasalahan Bisnis

1. Tingkat **dropout** yang tinggi di kalangan mahasiswa.
2. Kesulitan dalam mengidentifikasi faktor-faktor yang berkontribusi terhadap performa siswa.
3. Kurangnya wawasan untuk merancang strategi peningkatan retensi mahasiswa.

### Cakupan Proyek

1. Melakukan analisis data mahasiswa untuk memahami pola demografis, akademik, dan keuangan.
2. Mengembangkan model prediktif untuk memprediksi status mahasiswa (lulus, dropout, atau aktif).
3. Membuat dashboard bisnis untuk membantu pemangku kepentingan memonitor performa siswa dan mengambil keputusan berbasis data.

### Persiapan

**Sumber Data:** [Students' Performance](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

**Setup Environment**:

1. **Clone Repository**:

   Jika Anda menggunakan Git untuk mengelola proyek, clone repository ini ke komputer lokal Anda.

   ```bash
   git clone [https://github.com/mhmmadgiatt/HR-Attrition-Analysis-Dashboard.git](https://github.com/mhmmadgiatt/Jaya-Jaya-Institut-Dashboard.git)
   ```

2. **Install Dependencies**:

   Install semua dependensi yang diperlukan dengan menjalankan:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run Dashboard**:

   Setelah menginstal dependensi, jalankan dashboard menggunakan:

   ```bash
   streamlit run app.py
   ```

---

## Business Dashboard

**Deskripsi Dashboard:**
Dashboard ini dibuat menggunakan Streamlit untuk memberikan wawasan mendalam tentang performa dan retensi mahasiswa. Fitur utama dashboard meliputi:

- **Overview:** Gambaran umum seperti total mahasiswa, rata-rata nilai penerimaan, dan jumlah penerima beasiswa.
- **Student Status Analysis:** Visualisasi status mahasiswa berdasarkan pembayaran biaya kuliah, penerimaan beasiswa, dan status perkawinan.
- **Academic Performance:** Analisis performa akademik, termasuk distribusi nilai penerimaan dan hubungan antara usia dengan nilai akademik.
- **Demographic Insights:** Profil demografis mahasiswa berdasarkan program studi, kewarganegaraan, dan gender.
- **Predictive Analytics:** Prediksi status mahasiswa berdasarkan input data tertentu, dengan distribusi probabilitas prediksi.

**Link Dashboard:** *([Klik Link Dashboard](https://jaya-jaya-institut-dashboard.streamlit.app/), atau gunakan localhost: http://localhost:8501 untuk menjalankan di lokal)*

---

## Menjalankan Sistem Machine Learning

**Prototype Sistem:**
Sistem machine learning menggunakan model Random Forest Classifier yang telah dilatih untuk memprediksi status mahasiswa (lulus, dropout, aktif) berdasarkan fitur penting seperti status perkawinan, gender, usia, nilai penerimaan, dan jumlah mata kuliah yang diambil.

**Cara Menjalankan Prototype:**
1. Pastikan model tersimpan dalam file `model.pkl`.
2. Jalankan file `predict.py` untuk mengakses fitur prediksi.

```bash
# Menjalankan prototype
streamlit run predict.py
```
**Link Prototype:** *([Klik Link Prototype](https://prediction-jaya-jaya-institut-dashboard.streamlit.app/), atau gunakan localhost: http://localhost:8502 untuk menjalankan di lokal)*

**Fungsi Prediksi:**
Berikan input data seperti berikut untuk memprediksi status mahasiswa:
- Status Perkawinan
- Usia Saat Pendaftaran
- Nilai Penerimaan
- Jumlah Mata Kuliah Semester Pertama
- Gender

---

## Conclusion

### Kesimpulan Proyek
1. Analisis data menunjukkan bahwa status finansial (pembayaran biaya kuliah) dan beasiswa merupakan faktor utama yang memengaruhi status mahasiswa.
2. Model prediksi berhasil mencapai akurasi yang belum maksimal,tapi diharapkan untuk pengembangan dapat memberikan prediksi yang andal untuk status mahasiswa.
3. Dashboard yang dibuat membantu pemangku kepentingan untuk memonitor performa siswa dengan visualisasi yang mudah dipahami.

### Rekomendasi Action Items

1. **Tingkatkan Beasiswa:** Perluasan program beasiswa untuk meningkatkan retensi mahasiswa, terutama bagi mereka dengan status keuangan rentan.
2. **Pengawasan Lebih Ketat:** Implementasi pengawasan yang lebih ketat terhadap mahasiswa yang memiliki risiko tinggi dropout.
3. **Program Intervensi Dini:** Mengembangkan program intervensi berbasis data untuk mendukung mahasiswa yang performanya di bawah rata-rata.
4. **Optimasi Pengambilan Mata Kuliah:** Menyesuaikan kurikulum untuk mencegah overload pada semester pertama.

---
