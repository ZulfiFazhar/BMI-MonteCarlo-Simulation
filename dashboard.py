import streamlit as st
import pandas as pd

# Fungsi LCG
def lcg(z, a, c, m):
    return (a * z + c) % m

# Fungsi invers CDF
def diskrit_uniform(U,i,j):
    return i + ((j-i+1)*U)

# Fungsi untuk menghasilkan variate generator
def variate_generator(a, c, m, z0, i, j):
    zi = z0
    rows = []

    # Menghasilkan 300 baris data
    for _ in range(1, 301):
        zi_next = lcg(zi, a, c, m)
        ui = zi_next / m
        xi = round(diskrit_uniform(ui,i,j),2)
        xi_str = f'Rp{xi:,}'
        rows.append([_, zi, zi_next, round(ui, 5), xi_str, xi])
        zi = zi_next

    return pd.DataFrame(rows, columns=['i', 'Zi-1', 'Zi', 'Ui', 'Xi', 'Xi_float'])

# Membuat Tampilan untuk Streamlit
st.write("""
         #### NIM : 10122005
         #### Nama : Zulfi Fadilah Azhar
         #### Kelas : IF-1""")
st.divider()
st.title("2. b) Random Variate Generator")
st.write(r"Simulasi variable acak $x$ **Distribusi Uniform Diskrit** menggunakan **Linear Congruential Generator (LCG)** dan **Metode Inverse** sebanyak 300 data.")

st.divider()

st.write("### Linear Congruential Generator (LCG)")
st.latex(r'''Z_i =  (a \cdot Z_{i-1} + c) \mod m''')
st.write(r"""
        Dimana:
        - $Z_i$ = nilai bilangan ke-i dari deretnya (RN yang baru)
        - $Z_{i–1}$ = nilai bilangan sebelumnya (RN yang lama/semula)
        - $a$ = konstanta pengali
        - $c$ = increment (angka konstan yang bersyarat)
        - $m$ = modulus (modulo)
        - **Kunci pembangkit adalah $Z_0$ yang disebut seed.**
        """)
st.write(r"Bilangan acak seragam (Distribusi Uniform) : $U_i = \frac{Z_i}{m}$")

st.divider()

st.write("### Random Variate dengan Distribusi Uniform Diskrit")    
st.write(r"""
         Algoritma untuk memperoleh Variate acak yang berdistribusi uniform diskrit adalah sebagai berikut:
         1. Bangkitkan bilangan acak $U_i(0,1)$
         2. Tentukan nilai $i$ dimana $i$ adalah integer dan $i ≤ j$
         2. Bangkitkan $x = i + [(j-i+1)U]$
         """)

tab1, tab2 = st.tabs(['Static Input', 'User Input'])

with tab1:
    # Parameter LCG
    a_static = 16421
    c_static = 12237
    m_static = 2147483647
    z0_static = 10122005
    i_static = 800000
    j_static = 1000000

    df_static = variate_generator(a_static, c_static, m_static, z0_static, i_static, j_static)

    st.write("Membangkitkan 300 bilangan acak dengan ketentuan sebagai berikut:")
    st.write(r"""
             - $a$ = 16421
             - $c$ = 12237
             - $m$ = 2147483647
             - $Z_0$ = 10122005
             - $i$ = Rp800,000
             - $j$ = Rp1,000,000
             """)
    st.write(f"Penghasilan rata-rata perbulan adalah **Rp{round(df_static['Xi_float'].mean(),2):,}**")
    st.table(df_static.set_index("i").loc[:,['Zi-1', 'Zi', 'Ui', 'Xi']])

with tab2:
    st.write("Masukkan nilai untuk parameter LCG:")
    a = st.number_input(r"Masukkan nilai $a$", value=16421, step=1)
    c = st.number_input(r"Masukkan nilai $c$", value=12237, step=1)
    m = st.number_input(r"Masukkan nilai $m$", value=2147483647, step=1)
    z0 = st.number_input(r"Masukkan nilai $Z_0$", value=10122005, step=1)
    i = st.number_input(r"Masukkan nilai $Z_0$", value=800000, step=1)
    j = st.number_input(r"Masukkan nilai $Z_0$", value=1000000, step=1)

    df_user = variate_generator(a, c, m, z0, i, j)

    st.write(f"Membangkitkan 300 bilangan acak dengan User Input:")
    st.write(f"Penghasilan rata-rata perbulan adalah **Rp{round(df_user['Xi_float'].mean(),2):,}**")
    st.table(df_user.set_index("i").loc[:,['Zi-1', 'Zi', 'Ui', 'Xi']])
