import streamlit as st
import numpy as np
import string

# vigenere cipher
def vigenere_cipher(text, key, mode='encrypt'):
    result = []
    key = key.upper()
    text = text.upper()
    key_idx = 0
    
    for char in text:
        if char in string.ascii_uppercase:
            shift = ord(key[key_idx % len(key)]) - 65
            if mode == 'decrypt':
                shift = -shift
                
            new_char = chr(((ord(char) - 65 + shift) % 26) + 65)
            result.append(new_char)
            key_idx += 1
        else:
            result.append(char) 
    return "".join(result)

# affine cipher
def affine_cipher(text, a, b, mode='encrypt'):
    result = []
    text = text.upper()

    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    a_inv = mod_inverse(a, 26)
    
    for char in text:
        if char in string.ascii_uppercase:
            x = ord(char) - 65
            if mode == 'encrypt':
                new_x = (a * x + b) % 26
            else:
                new_x = (a_inv * (x - b)) % 26
            result.append(chr(new_x + 65))
        else:
            result.append(char)
    return "".join(result)

# playfair cipher
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()
    
    for char in key:
        if char in string.ascii_uppercase and char not in used:
            matrix.append(char)
            used.add(char)
    
    for char in string.ascii_uppercase:
        if char == "J" :
            continue
        if char not in used:
            matrix.append(char)
            used.add(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]


# hill cipher
# enigma cipher

st.set_page_config(page_title="Kalkulator Kriptografi", layout="centered")

st.title("🔐 Kalkulator Enkripsi & Dekripsi")
st.markdown("Dibangun menggunakan **Python & Streamlit**")

cipher_choice = st.sidebar.selectbox(
    "Pilih Algoritma Cipher:",
    ("Vigenere Cipher", "Affine Cipher", "Playfair Cipher", "Hill Cipher", "Enigma Cipher")
)

st.header(cipher_choice)

text_input = st.text_area("Masukkan Plaintext / Ciphertext:", height=150)
mode = st.radio("Pilih Mode:", ("Enkripsi", "Dekripsi"))

if cipher_choice == "Vigenere Cipher":
    key_input = st.text_input("Masukkan Kunci (Huruf):", value="KUNCI")
    if st.button("Proses"):
        if text_input and key_input:
            if mode == "Enkripsi":
                output = vigenere_cipher(text_input, key_input, 'encrypt')
            else:
                output = vigenere_cipher(text_input, key_input, 'decrypt')
            st.success("Hasil:")
            st.code(output)
        else:
            st.warning("Teks dan Kunci tidak boleh kosong!")

elif cipher_choice == "Affine Cipher":
    st.markdown("Rumus Enkripsi: $E(x) = (ax + b) \pmod{26}$")
    col1, col2 = st.columns(2)
    with col1:
        a_input = st.number_input("Nilai 'a' (Harus koprima dengan 26):", min_value=1, max_value=25, value=5)
    with col2:
        b_input = st.number_input("Nilai 'b' (Shift):", min_value=0, max_value=25, value=8)

    if np.gcd(a_input, 26) != 1:
        st.error("Nilai 'a' harus koprima dengan 26 (misal: 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25).")
    else:
        if st.button("Proses"):
            if text_input:
                if mode == "Enkripsi":
                    output = affine_cipher(text_input, a_input, b_input, 'encrypt')
                else:
                    output = affine_cipher(text_input, a_input, b_input, 'decrypt')
                st.success("Hasil:")
                st.code(output)

elif cipher_choice in ["Playfair Cipher"]:
    st.warning("Fungsi Playfair Cipher belum diimplementasikan.")

elif cipher_choice in ["Playfair Cipher", "Hill Cipher", "Enigma Cipher"]:
    st.info(f"Antarmuka untuk {cipher_choice} sudah siap. Kamu bisa menambahkan fungsi logika matematikanya di bagian kode program!")
