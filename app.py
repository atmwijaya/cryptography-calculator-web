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

def prepare_playfair_text(text):
    text = text.upper().replace("J", 'I')
    cleaned_text = [c for c in text if c in string.ascii_uppercase]
    
    i=0
    prepared_text = ""
    while i < len(cleaned_text):
        char1 = cleaned_text[i]
        if i + 1 < len(cleaned_text):
            char2 = cleaned_text[i + 1]
            if char1 == char2:
                prepared_text += char1 + 'X'
                i += 1
            else:
                prepared_text += char1 + char2
                i += 2
        else:
            prepared_text += char1 + 'X'
            i += 1
    return prepared_text

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j]== char:
                return i, j
    return -1, -1

def playfair_cipher(text, key, mode='encrypt'):
    if not text or not key:
        return "Teks dan Kunci tidak boleh kosong!"
    
    matrix = generate_playfair_matrix(key)
    
    if mode == 'encrypt':
        text = prepare_playfair_text(text)
    else:
        text = text.upper().replace("J", 'I')
        text = "".join([c for c in text if c in string.ascii_uppercase])
        if len(text) % 2 != 0:
            text += 'X'
        
    result = ""
    for i in range(0, len(text), 2):
        char1 = text[i]
        char2 = text[i + 1]
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:
            if mode == 'encrypt':
                result += matrix[row1][(col1 + 1) % 5]
                result += matrix[row2][(col2 + 1) % 5]
            else:
                result += matrix[row1][(col1 - 1) % 5]
                result += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            if mode == 'encrypt':
                result += matrix[(row1 + 1) % 5][col1]
                result += matrix[(row2 + 1) % 5][col2]
            else:
                result += matrix[(row1 - 1) % 5][col1]
                result += matrix[(row2 - 1) % 5][col2]
        else:
            result += matrix[row1][col2]
            result += matrix[row2][col1]
    return result

# hill cipher
def mod_inverse_matrix(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    
    try:
        det.inv = pow(det % modulus, -1, modulus)
    except ValueError:
        return None
    
    adj = np.array([[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]])
    
    matrix_mod_inv = (det.inv * adj) % modulus
    return np.round(matrix_mod_inv).astype(int)

def hill_cipher(text, key_matrix, mode='encrypt'):
    text = "".join([c for c in text.upper() if c in string.ascii_uppercase])
    n = 2
    
    if len(text) % n != 0:
        text += 'X'
    
    if mode == 'decrypt':
        key_matrix = mod_inverse_matrix(key_matrix, 26)
        if key_matrix is None:
            return "Kunci tidak valid untuk dekripsi!"
    
    result = ""
    for i in range(0, len(text), n):
        block = [ord(c) - 65 for c in text[i:i+n]]
        block_vector = np.array(block)
        
        res_vector = np.dot(key_matrix, block_vector) % 26
        
        for val in res_vector:
            result += chr(int(val) + 65)
    return result

# enigma cipher
class EnigmaMachine:
    def __init__(self, p1, p2, p3):
        self.r1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
        self.r2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
        self.r3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
        self.reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        self.pos = [p1, p2, p3]
        self.alphabet = string.ascii_uppercase
        
    def step_rotors(self):
        self.pos[0] = (self.pos[0] + 1) % 26
        if self.pos[0] == 0:
            self.pos[1] = (self.pos[1] + 1) % 26
            if self.pos[1] == 0:
                self.pos[2] = (self.pos[2] + 1) % 26
    
    def process_text(self, text):
        result = ""
        text = "".join([c for c in text.upper() if c in self.alphabet])
        
        for char in text:
            self.step_rotors()
            idx = self.alphabet.index(char)
            idx = self.alphabet.index(self.r1[(idx + self.pos[0]) % 26])
            idx = self.alphabet.index(self.r2[(idx + self.pos[1]) % 26])
            idx = self.alphabet.index(self.r3[(idx + self.pos[2]) % 26])
            idx = self.alphabet.index(self.reflector[idx])
            idx = (self.r3.index(self.alphabet[idx]) - self.pos[2]) % 26
            idx = (self.r2.index(self.alphabet[idx]) - self.pos[1]) % 26
            idx = (self.r1.index(self.alphabet[idx]) - self.pos[0]) % 26
            result += self.alphabet[idx]
        return result

def enigma_cipher(text, p1, p2, p3):
    enigma = EnigmaMachine(p1, p2, p3)
    return enigma.process_text(text)

st.set_page_config(page_title="Kalkulator Kriptografi", layout="centered")

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🔐 Kalkulator Enkripsi & Dekripsi")
st.markdown("Created by Arrasyid Atma Wijaya - 21120123140114")

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
            
            st.session_state.history.append({
                'cipher': "Vigenere Cipher",
                'mode': mode,
                'input': text_input,
                'output': output
            })
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
                
                st.session_state.history.append({
                'cipher': "Affine Cipher",
                'mode': mode,
                'input': text_input,
                'output': output
            })

elif cipher_choice in ["Playfair Cipher"]:
    st.markdown("💡 **Info Playfair:** Huruf **J** dilebur menjadi **I**. Teks akan diproses berpasangan (digraph). Huruf kembar akan dipisahkan dengan huruf **X**.")
    key_input = st.text_input("Masukkan Kunci (Huruf):", value="KUNCI")
    
    if st.button("Proses"):
        if text_input and key_input:
            if mode == "Enkripsi":
                output = playfair_cipher(text_input, key_input, 'encrypt')
            else:
                output = playfair_cipher(text_input, key_input, 'decrypt')
            st.write("Matriks Kunci 5x5:")
            matrix = generate_playfair_matrix(key_input)
            matrix_display = "\n".join([" ".join(row) for row in matrix])
            st.text(matrix_display)
            st.success("Hasil:")
            st.code(output)
            st.session_state.history.append({
                'cipher': "Playfair Cipher",
                'mode': mode,
                'input': text_input,
                'output': output
            })
        else:
            st.warning("Teks dan Kunci tidak boleh kosong!")

elif cipher_choice in ["Hill Cipher"]:
    st.markdown("💡 **Info Hill Cipher:** Kunci berupa matriks 2x2. Pastikan determinan matriks koprima dengan 26 untuk dekripsi.")
    st.write("Masukkan elemen matriks kunci (2x2):")
    col1, col2 = st.columns(2)
    with col1:
        k00 = st.number_input("baris 1, kolom 1", value=3)
        k10 = st.number_input("baris 2, kolom 1", value=2)
    with col2:
        k01 = st.number_input("baris 1, kolom 2", value=3)
        k11 = st.number_input("baris 2, kolom 2", value=5)
    
    key_matrix = np.array([[k00, k01], [k10, k11]])
    
    if st.button("Proses"):
        if text_input:
            if mode == "Enkripsi":
                output = hill_cipher(text_input, key_matrix, 'encrypt')
            else:
                output = hill_cipher(text_input, key_matrix, 'decrypt')
            
            if "Kunci tidak valid" in output:
                st.error(output)
            else:
                st.success("Hasil:")
                st.code(output)
                st.session_state.history.append({
                'cipher': "Hill Cipher",
                'mode': mode,
                'input': text_input,
                'output': output
            })
    
elif cipher_choice in ["Enigma Cipher"]:
    st.markdown("💡 **Info Enigma Cipher:** Masukkan posisi awal rotor (0-25) untuk masing-masing rotor (R1, R2, R3).")
    col1, col2, col3 = st.columns(3)
    with col1:
        r1 = st.number_input("Posisi awal Rotor R1:", min_value=0, max_value=25, value=0)
    with col2:
        r2 = st.number_input("Posisi awal Rotor R2:", min_value=0, max_value=25, value=0)
    with col3:
        r3 = st.number_input("Posisi awal Rotor R3:", min_value=0, max_value=25, value=0)
    
    if st.button("Proses"):
        if text_input:
            output = enigma_cipher(text_input, r1, r2, r3)
            st.success("Hasil:")
            st.code(output)
            st.session_state.history.append({
                'cipher': "Enigma Cipher",
                'mode': mode,
                'input': text_input,
                'output': output
            })
            
st.markdown("---")
st.sidebar.subheader("Riwayat Proses")

if st.sidebar.button("Hapus Riwayat"):
    st.session_state.history = []
    st.rerun()

if not st.session_state.history:
    st.sidebar.info("Belum ada riwayat proses.")
else:
    for idx, item in enumerate(st.session_state.history):
        with st.sidebar.expander(f"{item['cipher']} - {item['mode']}"):
            st.markdown(f"**Input:**\n {item['input']}")
            st.markdown(f"**Output:**\n {item['output']}")