import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# fungsi untuk memasukkan histogram
def plot_histogram(data, column, title):
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=20, color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frekuensi')
    st.pyplot(plt)

# fungsi untuk memasukkan pie chart
def plot_pie_chart(data, column, title):
    status_counts = data[column].value_counts()
    labels = status_counts.index
    sizes = status_counts.values

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.title(title)
    st.pyplot(plt)

# --- load data ---
df = pd.read_csv('dataset.csv')
df.rename(columns={'Mahasiswa Ke-':'mahasiswa_ke', 'Tinggi Badan (cm)':'tinggi_badan', 'Berat Badan (Kg)':'berat_badan'}, inplace=True)

# --- Pengolahan Data ---
# Mengambil data mahasiswa dan tinggi badan dari df utama
tinggi_badan = df[['mahasiswa_ke', 'tinggi_badan']]

# Mengambil data mahasiswa dan berat badan dari df utama
berat_badan = df[['mahasiswa_ke', 'berat_badan']]

# -- Tinggi Badan --
# Mencari Frekuensi Tinggi Badan
frekuensi_tinggi = df['tinggi_badan'].value_counts().reset_index()
frekuensi_tinggi.columns = ['tinggi_badan', 'frekuensi']
frekuensi_tinggi = frekuensi_tinggi.sort_values(by='tinggi_badan').reset_index(drop=True)

# Total Frekuensi Tinggi Badan
total_tinggi = frekuensi_tinggi['frekuensi'].sum()

# Mencari Probabilitas Kumulatif Tinggi Badan
frekuensi_tinggi['probabilitas'] = (frekuensi_tinggi['frekuensi'] / total_tinggi).round(2)
frekuensi_tinggi['probabilitas_kumulatif'] = (frekuensi_tinggi['probabilitas'].cumsum()).round(2)
frekuensi_tinggi['probabilitas_kumulatif_x100'] = (frekuensi_tinggi['probabilitas_kumulatif'] * 100).astype(int)

# Mencari Interval Data Tinggi Badan
frekuensi_tinggi['interval_angka_random'] = frekuensi_tinggi['probabilitas_kumulatif_x100'].shift(1, fill_value=0) + 1
frekuensi_tinggi['interval_angka_random'] = frekuensi_tinggi['interval_angka_random'].astype(str) + '-' + frekuensi_tinggi['probabilitas_kumulatif_x100'].astype(str)

# -- Berat Badan --
# Mencari Frekuensi Berat Badan
frekuensi_berat = df['berat_badan'].value_counts().reset_index()
frekuensi_berat.columns = ['berat_badan', 'frekuensi']
frekuensi_berat = frekuensi_berat.sort_values(by='berat_badan').reset_index(drop=True)

# Total Frekuensi Berat Badan
total_berat = frekuensi_berat['frekuensi'].sum()

# Mencari Probabilitas Kumulatif Berat Badan
frekuensi_berat['probabilitas'] = (frekuensi_berat['frekuensi'] / total_berat).round(2)
frekuensi_berat['probabilitas_kumulatif'] = (frekuensi_berat['probabilitas'].cumsum()).round(2)
frekuensi_berat['probabilitas_kumulatif_x100'] = (frekuensi_berat['probabilitas_kumulatif'] * 100).astype(int)

# Mencari Interval Data Berat Badan
frekuensi_berat['interval_angka_random'] = frekuensi_berat['probabilitas_kumulatif_x100'].shift(1, fill_value=0) + 1
frekuensi_berat['interval_angka_random'] = frekuensi_berat['interval_angka_random'].astype(str) + '-' + frekuensi_berat['probabilitas_kumulatif_x100'].astype(str)

# -- Nilai Acak LCG --
def lcg(z, a, c, m):
    return (a * z + c) % m

def lcg_simulation(a, c, m, z0):
    zi = z0
    rows = []

    # Menghasilkan data
    for _ in range(1, 201):
        zi_next = lcg(zi, a, c, m)
        ui = zi_next / m
        ui_100 = ui * 100
        rows.append([_, zi, zi_next, round(ui, 5), round(ui_100)])
        zi = zi_next

    return pd.DataFrame(rows, columns=['i', 'Zi-1', 'Zi', 'Ui', 'Ui x100'])

# -- Simulasi Monte Carlo --
# Membuat Dataframe baru untuk simulasi
df_mahasiswa = pd.DataFrame({'mahasiswa_ke': range(1, 101)})

# Parameter LCG
a = 16421
c = 12237
m = 2147483647
z0 = 10122005

# Dataframe simulasi LCG
df_lcg = lcg_simulation(a, c, m, z0)

# Index 100 data dari df simulasi lcg untuk simulasi monte carlo
df_lcg_tb = df_lcg['Ui x100'].iloc[0:100].astype(int)
df_lcg_bb = df_lcg['Ui x100'].iloc[100:200].astype(int).reset_index(drop=True)

# Membuat dataframe baru yang menggabungkan tabel mahasiswa dan nilai acak lcg untuk simulasi
df_simulasi_bmi = pd.concat([df_mahasiswa,df_lcg_tb, df_lcg_bb], axis=1)
df_simulasi_bmi.columns = ['mahasiswa_ke', 'Tinggi Badan (Acak)', 'Berat Badan (Acak)']

# Fungsi untuk mencari nilai Tinggi Badan dari nilai acak dan membandingkannya dengan interval angka acak
def simulasi_tinggi_badan(simulasi_value):
    for _, row in frekuensi_tinggi.iterrows():
        if simulasi_value <= row['probabilitas_kumulatif_x100']:
            return row['tinggi_badan']
    return None

# Fungsi untuk mencari nilai Berat Badan dari nilai acak dan membandingkannya dengan interval angka acak
def simulasi_berat_badan(simulasi_value):
    for _, row in frekuensi_berat.iterrows():
        if simulasi_value <= row['probabilitas_kumulatif_x100']:
            return row['berat_badan']
    return None

# Mencari Nilai Tinggi Badan dengan menggunakan fungsi yang sudah dibuat
df_simulasi_bmi['Tinggi Badan (Simulasi)'] = df_simulasi_bmi['Tinggi Badan (Acak)'].apply(simulasi_tinggi_badan) / 100

# Mencari Nilai Berat Badan dengan menggunakan fungsi yang sudah dibuat
df_simulasi_bmi['Berat Badan (Simulasi)'] = df_simulasi_bmi['Berat Badan (Acak)'].apply(simulasi_berat_badan)

# Mencari nilai BMI (Body Mass Index)
df_simulasi_bmi['BMI'] = df_simulasi_bmi['Berat Badan (Simulasi)'] / (df_simulasi_bmi['Tinggi Badan (Simulasi)'] ** 2)
df_simulasi_bmi['BMI'] = df_simulasi_bmi['BMI']

# Fungsi untuk mencari Status BMI
def get_bmi_status(bmi):
    if bmi < 18:
        return 'Underweight'
    elif 18 < bmi < 25:
        return 'Normal'
    elif 25 < bmi < 31:
        return 'Overweight'
    else:
        return 'Obesitas'

# Mencari Status BMI dengan menggunakan fungsi yang sudah dibuat
df_simulasi_bmi['Status BMI'] = df_simulasi_bmi['BMI'].apply(get_bmi_status)




# --- Main Menu Tampilan ---
st.header("Kelompok 6")
st.write(f"""
    - 10122003 - Andrian Baros
    - 10122005 - Zulfi Fadilah Azhar
    - 10122029 - Alif Vidya Kusumah
""")

st.title("Simulasi Sistem Body Mass Index (BMI)")
st.write("Diketahui data tinggi dan berat badan 90 mahasiswa Informatika UNIKOM adalah sebagai berikut.")
df



tab1, tab2, tab3, tab4 = st.tabs(["Studi Kasus Simulasi", "Membangkitkan Nilai Acak", "Simulasi Statis", "Simulasi Dinamis"])


with tab1:
    st.header("Pengolahan Data")
    st.write("Proses untuk mengubah data mentah tinggi badan dan berat badan dari 90 mahasiswa melibatkan tahapan awal pengolahan dengan pembuatan tabel yang memuat informasi tinggi badan dan berat badan masing-masing individu.")


    st.write("**Frekuensi Data Tinggi Badan**")
    st.table(frekuensi_tinggi[["tinggi_badan","frekuensi"]])

    st.write("**Frekuensi Data Berat Badan**")
    st.table(frekuensi_berat[["berat_badan","frekuensi"]])

    st.write("Setelah tabel tinggi badan dan berat badan, berikutnya adalah tabel yang menampilkan probabilitas dan probabilitas kumulatif untuk masing-masing tinggi badan dan berat badan.")

    st.subheader("Probabilitas Data")
    
    st.write("Probabilitas Data Tinggi Badan")
    st.table(frekuensi_tinggi[["tinggi_badan", "probabilitas", "probabilitas_kumulatif"]])
    
    st.write("Probabilitas Data Berat Badan")
    st.table(frekuensi_berat[["berat_badan", "probabilitas", "probabilitas_kumulatif"]])

    st.write("Tabel di atas menggambarkan data tinggi badan dan berat badan, setelah itu membuat probabilitas kumulatifnya di kalikan 100 dan kemunculan angka acaknya.")

    st.write("Probabilitas Kumulatif x100 dan Interval Angka Random Data Tinggi Badan")
    st.table(frekuensi_tinggi[["tinggi_badan", "probabilitas", "probabilitas_kumulatif_x100", "interval_angka_random"]])
    
    st.write("Probabilitas Kumulatif x100 dan Interval Angka Random Data Berat Badan")
    st.table(frekuensi_berat[["berat_badan", "probabilitas", "probabilitas_kumulatif_x100", "interval_angka_random"]])

with tab2:
    st.subheader("Membangkitkan Nilai Acak dengan Menggunakan LCG")
    st.write("Sebelum melakukan simulasi Monte Carlo, perlu membangkitkan angka acak terlebih dahulu. Dalam simulasi kali ini metode yang digunakan adalah Linear Congruential Generator (LCG). Metode LCG digunakan untuk membangkitkan bilangan acak dengan distribusi uniform. LCG memiliki pseudo RNG berbentuk")
    st.latex(r'''Z_i =  (a \cdot Z_{i-1} + c) \mod m''')
    st.write(r"""
        Dimana:
        - $Z_i$ = nilai bilangan ke-i dari deretnya (RN yang baru)
        - $Z_{i–1}$ = nilai bilangan sebelumnya (RN yang lama/semula)
        - $a$ = konstanta pengali
        - $c$ = increment (angka konstan yang bersyarat)
        - $m$ = modulus (modulo)
        """)
    st.write(r"Bilangan acak seragam (Distribusi Uniform) : $U_i = \frac{Z_i}{m}$")
    st.write(r"""
        Diketahui:
        - $Z_0$ = 10122005
        - $a$ = 16421
        - $c$ = 12237
        - $m$ = 2147483647
        """)
    st.write("Maka, hasil simulasi LCG sebagai berikut:")

    st.table(df_lcg)

with tab3:
    st.subheader("Simulasi BMI dengan menggunakan nilai acak LCG")
    st.write(r"""
        - $Z_0$ = 10122005
        - $a$ = 16421
        - $c$ = 12237
        - $m$ = 2147483647
        """)
    st.table(df_simulasi_bmi)
    # df_simulasi_bmi
    
    # histogram
    st.write("Tinggi Badan (Simulasi)")
    plot_histogram(df_simulasi_bmi, 'Tinggi Badan (Simulasi)', 'Tinggi Badan (Simulasi)')
    
    st.write(" Berat Badan (Simulasi)")
    plot_histogram(df_simulasi_bmi, 'Berat Badan (Simulasi)', 'Berat Badan (Simulasi)')
    
    st.write("BMI (Simulasi)")
    plot_histogram(df_simulasi_bmi, 'BMI', 'BMI (Simulasi)')

    st.write("Distribusi Status BMI (Simulasi)")
    plot_pie_chart(df_simulasi_bmi, 'Status BMI', 'Distribusi Status BMI (Simulasi)')

with tab4:
    st.subheader("Simulasi BMI dengan nilai acak LCG dinamis")

    # Input dinamis untuk parameter LCG
    a = st.number_input('Masukkan nilai a', value=16421)
    c = st.number_input('Masukkan nilai c', value=12237)
    m = st.number_input('Masukkan nilai m', value=2147483647)
    z0 = st.number_input('Masukkan nilai Z0', value=10122005)

    # Tombol untuk menjalankan simulasi
    if st.button('Jalankan Simulasi'):
        # Dataframe simulasi LCG
        df_lcg = lcg_simulation(a, c, m, z0)

        # Index 100 data dari df simulasi lcg untuk simulasi monte carlo
        df_lcg_tb = df_lcg['Ui x100'].iloc[0:100]
        df_lcg_bb = df_lcg['Ui x100'].iloc[100:200].reset_index(drop=True)

        # Membuat dataframe baru yang menggabungkan tabel mahasiswa dan nilai acak lcg untuk simulasi
        df_simulasi_bmi = pd.concat([df_mahasiswa, df_lcg_tb, df_lcg_bb], axis=1)
        df_simulasi_bmi.columns = ['mahasiswa_ke', 'Tinggi Badan (Acak)', 'Berat Badan (Acak)']

        # Mencari Nilai Tinggi Badan dengan menggunakan fungsi yang sudah dibuat
        df_simulasi_bmi['Tinggi Badan (Simulasi)'] = df_simulasi_bmi['Tinggi Badan (Acak)'].apply(simulasi_tinggi_badan) / 100

        # Mencari Nilai Berat Badan dengan menggunakan fungsi yang sudah dibuat
        df_simulasi_bmi['Berat Badan (Simulasi)'] = df_simulasi_bmi['Berat Badan (Acak)'].apply(simulasi_berat_badan)

        # Mencari nilai BMI (Body Mass Index)
        df_simulasi_bmi['BMI'] = df_simulasi_bmi['Berat Badan (Simulasi)'] / (df_simulasi_bmi['Tinggi Badan (Simulasi)'] ** 2)

        # Mencari Status BMI dengan menggunakan fungsi yang sudah dibuat
        df_simulasi_bmi['Status BMI'] = df_simulasi_bmi['BMI'].apply(get_bmi_status)

        st.write("Hasil Simulasi BMI:")
        st.table(df_simulasi_bmi)

        #histogram
        st.write("Tinggi Badan (Simulasi)")
        plot_histogram(df_simulasi_bmi, 'Tinggi Badan (Simulasi)', ' Tinggi Badan (Simulasi)')
        
        st.write("Berat Badan (Simulasi)")
        plot_histogram(df_simulasi_bmi, 'Berat Badan (Simulasi)', ' Berat Badan (Simulasi)')
        
        st.write("BMI (Simulasi)")
        plot_histogram(df_simulasi_bmi, 'BMI', 'BMI (Simulasi)')

        st.write("Status BMI (Simulasi)")
        plot_pie_chart(df_simulasi_bmi, 'Status BMI', 'Distribusi Status BMI (Simulasi)')