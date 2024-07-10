import streamlit as st
import pandas as pd
st.title("SIMULASI BMI MONTE CARLO")
#load data
df = pd.read_csv('dataset.csv')
df
df.rename(columns={'Mahasiswa Ke-':'mahasiswa_ke', 'Tinggi Badan (cm)':'tinggi_badan', 'Berat Badan (Kg)':'berat_badan'}, inplace=True)

tab1, tab2 = st.tabs(["LCG Statis", "LCG Dinamis"])

with tab1:

#tabel tinggi badan
    st.write("Tinggi Badan")
    tinggi_badan = df[['mahasiswa_ke', 'tinggi_badan']]
    tinggi_badan
    st.write("Frekuensi Tinggi Badan")
    frekuensi_tinggi = df['tinggi_badan'].value_counts().reset_index()
    frekuensi_tinggi.columns = ['tinggi_badan', 'frekuensi']

    frekuensi_tinggi = frekuensi_tinggi.sort_values(by='tinggi_badan').reset_index(drop=True)
    frekuensi_tinggi

    total_tinggi = frekuensi_tinggi['frekuensi'].sum()

    st.write("Probabilitas Kumulatif Tinggi Badan")
    frekuensi_tinggi['probabilitas'] = (frekuensi_tinggi['frekuensi'] / total_tinggi).round(2)
    frekuensi_tinggi['probabilitas_kumulatif'] = (frekuensi_tinggi['probabilitas'].cumsum()).round(2)

    frekuensi_tinggi

    frekuensi_tinggi['probabilitas_kumulatif_x100'] = (frekuensi_tinggi['probabilitas_kumulatif'] * 100).astype(int)

    frekuensi_tinggi

        # Menghitung kolom tambahan untuk berat badan

    frekuensi_tinggi['probabilitas_kumulatif_x100'] = (frekuensi_tinggi['probabilitas_kumulatif'] * 100).astype(int)
    frekuensi_tinggi['interval_angka_random'] = frekuensi_tinggi['probabilitas_kumulatif_x100'].shift(1, fill_value=0) + 1
    frekuensi_tinggi['interval_angka_random'] = frekuensi_tinggi['interval_angka_random'].astype(str) + '-' + frekuensi_tinggi['probabilitas_kumulatif_x100'].astype(str)

    frekuensi_tinggi

    #tabel berat badan
    st.write("Berat Badan")
    berat_badan = df[['mahasiswa_ke', 'berat_badan']]
    berat_badan

    st.write("Frekuensi Berat Badan")
    frekuensi_berat = df['berat_badan'].value_counts().reset_index()
    frekuensi_berat.columns = ['berat_badan', 'frekuensi']

    frekuensi_berat = frekuensi_berat.sort_values(by='berat_badan').reset_index(drop=True)
    frekuensi_berat

    total_berat = frekuensi_berat['frekuensi'].sum()

    st.write("Probabilitas Kumulatif Berat Badan")
    frekuensi_berat['probabilitas'] = (frekuensi_berat['frekuensi'] / total_berat).round(2)
    frekuensi_berat['probabilitas_kumulatif'] = (frekuensi_berat['probabilitas'].cumsum()).round(2)

    frekuensi_berat

    frekuensi_berat['probabilitas_kumulatif_x100'] = (frekuensi_berat['probabilitas_kumulatif'] * 100).astype(int)

    frekuensi_berat
    #LCG
    st.write("LCG")
    def lcg(z, a, c, m):
        return (a * z + c) % m
    def lcg_simulation(a, c, m, z0):
        zi = z0
        rows = []

        # Menghasilkan 300 baris data
        for _ in range(0, 300):
            zi_next = lcg(zi, a, c, m)
            ui = zi_next / m
            ui_100 = ui * 100
            rows.append([_, zi, zi_next, round(ui, 5), round(ui_100)])
            zi = zi_next

        return pd.DataFrame(rows, columns=['i', 'Zi-1', 'Zi', 'Ui', 'Ui x100'])
    a = 16421
    c = 12237
    m = 2147483647
    z0 = 10122005

    df_lcg = lcg_simulation(a, c, m, z0)
    df_lcg

    df_mahasiswa = pd.DataFrame({'mahasiswa_ke': range(1, 101)})
    df_lcg_tb = df_lcg['Ui x100'].iloc[0:100]
    df_lcg_tb


    df_lcg_bb = df_lcg['Ui x100'].iloc[100:200].reset_index(drop=True)
    df_lcg_bb

    df_simulasi_bmi = pd.concat([df_mahasiswa,df_lcg_tb, df_lcg_bb], axis=1)
    df_simulasi_bmi.columns = ['mahasiswa_ke', 'Tinggi Badan (Acak)', 'Berat Badan (Acak)']
    df_simulasi_bmi

    def simulasi_berat_badan(simulasi_value):
        for _, row in frekuensi_berat.iterrows():
            if simulasi_value <= row['probabilitas_kumulatif_x100']:
                return row['berat_badan']
        return None

    def simulasi_tinggi_badan(simulasi_value):
        for _, row in frekuensi_tinggi.iterrows():
            if simulasi_value <= row['probabilitas_kumulatif_x100']:
                return row['tinggi_badan']
        return None

    df_simulasi_bmi['Tinggi Badan (Simulasi)'] = df_simulasi_bmi['Tinggi Badan (Acak)'].apply(simulasi_tinggi_badan) / 100
    df_simulasi_bmi['Berat Badan (Simulasi)'] = df_simulasi_bmi['Berat Badan (Acak)'].apply(simulasi_berat_badan)

    df_simulasi_bmi

    df_simulasi_bmi['BMI'] = df_simulasi_bmi['Berat Badan (Simulasi)'] / (df_simulasi_bmi['Tinggi Badan (Simulasi)'] ** 2)
    df_simulasi_bmi['BMI'] = df_simulasi_bmi['BMI'].round(2)
    df_simulasi_bmi

    # Fungsi untuk mendapatkan status BMI
    def get_bmi_status(bmi):
        if bmi <= 17:
            return 'Underweight'
        elif 18 <= bmi <= 24:
            return 'Normal'
        elif 25 <= bmi <= 30:
            return 'Overweight'
        else:
            return 'Obesitas'

    # Tambahkan status BMI ke dalam dataframe
    df_simulasi_bmi['Status BMI'] = df_simulasi_bmi['BMI'].apply(get_bmi_status)

    # Tampilkan dataframe akhir
    df_simulasi_bmi

with tab2:
    #tabel tinggi badan
    st.write("Tinggi Badan")
    tinggi_badan = df[['mahasiswa_ke', 'tinggi_badan']]
    tinggi_badan
    st.write("Frekuensi Tinggi Badan")
    frekuensi_tinggi = df['tinggi_badan'].value_counts().reset_index()
    frekuensi_tinggi.columns = ['tinggi_badan', 'frekuensi']

    frekuensi_tinggi = frekuensi_tinggi.sort_values(by='tinggi_badan').reset_index(drop=True)
    frekuensi_tinggi

    total_tinggi = frekuensi_tinggi['frekuensi'].sum()

    st.write("Probabilitas Kumulatif Tinggi Badan")
    frekuensi_tinggi['probabilitas'] = (frekuensi_tinggi['frekuensi'] / total_tinggi).round(2)
    frekuensi_tinggi['probabilitas_kumulatif'] = (frekuensi_tinggi['probabilitas'].cumsum()).round(2)

    frekuensi_tinggi

    frekuensi_tinggi['probabilitas_kumulatif_x100'] = (frekuensi_tinggi['probabilitas_kumulatif'] * 100).astype(int)

    frekuensi_tinggi

    # Menghitung kolom tambahan untuk berat badan

    frekuensi_tinggi['probabilitas_kumulatif_x100'] = (frekuensi_tinggi['probabilitas_kumulatif'] * 100).astype(int)
    frekuensi_tinggi['interval_angka_random'] = frekuensi_tinggi['probabilitas_kumulatif_x100'].shift(1, fill_value=0) + 1
    frekuensi_tinggi['interval_angka_random'] = frekuensi_tinggi['interval_angka_random'].astype(str) + '-' + frekuensi_tinggi['probabilitas_kumulatif_x100'].astype(str)

    frekuensi_tinggi

    #tabel berat badan
    st.write("Berat Badan")
    berat_badan = df[['mahasiswa_ke', 'berat_badan']]
    berat_badan

    st.write("Frekuensi Berat Badan")
    frekuensi_berat = df['berat_badan'].value_counts().reset_index()
    frekuensi_berat.columns = ['berat_badan', 'frekuensi']

    frekuensi_berat = frekuensi_berat.sort_values(by='berat_badan').reset_index(drop=True)
    frekuensi_berat

    total_berat = frekuensi_berat['frekuensi'].sum()

    st.write("Probabilitas Kumulatif Berat Badan")
    frekuensi_berat['probabilitas'] = (frekuensi_berat['frekuensi'] / total_berat).round(2)
    frekuensi_berat['probabilitas_kumulatif'] = (frekuensi_berat['probabilitas'].cumsum()).round(2)

    frekuensi_berat

    frekuensi_berat['probabilitas_kumulatif_x100'] = (frekuensi_berat['probabilitas_kumulatif'] * 100).astype(int)

    frekuensi_berat
    #LCG
    st.write("LCG Dinamis")

    # User input for LCG parameters
    a = st.number_input("Input a:", value=16421)
    c = st.number_input("Input c:", value=12237)
    m = st.number_input("Input m:", value=2147483647)
    z0 = st.number_input("Input z0:", value=10122005)

    def lcg(z, a, c, m):
        return (a * z + c) % m

    def lcg_simulation(a, c, m, z0):
        zi = z0
        rows = []

        # Menghasilkan 300 baris data
        for _ in range(0, 300):
            zi_next = lcg(zi, a, c, m)
            ui = zi_next / m
            ui_100 = ui * 100
            rows.append([_, zi, zi_next, round(ui, 5), round(ui_100)])
            zi = zi_next

        return pd.DataFrame(rows, columns=['i', 'Zi-1', 'Zi', 'Ui', 'Ui x100'])


    df_lcg = lcg_simulation(a, c, m, z0)
    df_lcg

    df_mahasiswa = pd.DataFrame({'mahasiswa_ke': range(1, 101)})
    df_lcg_tb = df_lcg['Ui x100'].iloc[0:100]
    df_lcg_tb


    df_lcg_bb = df_lcg['Ui x100'].iloc[100:200].reset_index(drop=True)
    df_lcg_bb

    df_simulasi_bmi = pd.concat([df_mahasiswa,df_lcg_tb, df_lcg_bb], axis=1)
    df_simulasi_bmi.columns = ['mahasiswa_ke', 'Tinggi Badan (Acak)', 'Berat Badan (Acak)']
    df_simulasi_bmi

    def simulasi_berat_badan(simulasi_value):
        for _, row in frekuensi_berat.iterrows():
            if simulasi_value <= row['probabilitas_kumulatif_x100']:
                return row['berat_badan']
        return None

    def simulasi_tinggi_badan(simulasi_value):
        for _, row in frekuensi_tinggi.iterrows():
            if simulasi_value <= row['probabilitas_kumulatif_x100']:
                return row['tinggi_badan']
        return None

    df_simulasi_bmi['Tinggi Badan (Simulasi)'] = df_simulasi_bmi['Tinggi Badan (Acak)'].apply(simulasi_tinggi_badan) / 100
    df_simulasi_bmi['Berat Badan (Simulasi)'] = df_simulasi_bmi['Berat Badan (Acak)'].apply(simulasi_berat_badan)

    df_simulasi_bmi

    df_simulasi_bmi['BMI'] = df_simulasi_bmi['Berat Badan (Simulasi)'] / (df_simulasi_bmi['Tinggi Badan (Simulasi)'] ** 2)
    df_simulasi_bmi['BMI'] = df_simulasi_bmi['BMI'].round(2)
    df_simulasi_bmi

    # Fungsi untuk mendapatkan status BMI
    def get_bmi_status(bmi):
        if bmi <= 17:
            return 'Underweight'
        elif 18 <= bmi <= 24:
            return 'Normal'
        elif 25 <= bmi <= 30:
            return 'Overweight'
        else:
            return 'Obesitas'

    # Tambahkan status BMI ke dalam dataframe
    df_simulasi_bmi['Status BMI'] = df_simulasi_bmi['BMI'].apply(get_bmi_status)

    # Tampilkan dataframe akhir
    df_simulasi_bmi