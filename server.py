from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import seaborn as sns
import matplotlib.pyplot as plt
import random
from math import gcd
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def generate_rsa_keys(bits=8):

    # Gerar dois num primos p e q
    p=0
    while (not is_prime(p) or p < 200):
        p = random.getrandbits(bits)
    print('\np:', p)
    q=0
    while (not is_prime(q) or p == q or q < 200):
        q = random.getrandbits(bits)
    print('\nq:', q)
    
    n = p * q

    # Calcular phi(n)
    phi_n = (p - 1) * (q - 1)
    
    # Escolher e (geralmente um pequeno número coprimo com phi(n))
    e = 65537
    while gcd(e, phi_n) != 1:
        e = random.randrange(2, phi_n)
    
    # Calcular d tal que (d * e) % phi(n) = 1
    d = mod_inverse(e, phi_n)
    
    # Retornar chave pública (e, n) e chave privada (d, n)
    return ((e, n), (d, n))

def write_file(file_name: str, content: str):
    with open(file_name, 'w') as file:
        file.write(content)

def decode_bit(input: list) -> str:
    # Verifica se a entrada tem apenas 0s e 1s
    if not all(bit in [0, 1] for bit in input):
        raise ValueError("Input contains non-binary values")

    # Ajusta o comprimento para ser múltiplo de 8, caso necessário
    if len(input) % 8 != 0:
        padding = 8 - (len(input) % 8)
        input.extend([0] * padding)  # Adiciona 0s para completar o último byte

    # Converte a lista de bits em uma string de caracteres
    output = ''.join([chr(int(''.join(map(str, input[i:i+8])), 2)) for i in range(0, len(input), 8)])

    return output

def decode_mlt3(input: list) -> list:
    mlt3_data = []

    # First output signal is the same
    signal_out = input[0]
    mlt3_data.append(signal_out)

    # Sign initialization
    if signal_out == 1:
        sign = 1
    else:
        sign = -1

    # MLT-3 decoding
    for i in range(1, len(input)):
        if input[i] == input[i-1]:
            signal_out = 0
        else:
            signal_out = 1
        mlt3_data.append(signal_out)

    return mlt3_data

# RSA caracter por caracter
def decrypt_rsa(encrypted_message, private_key):
    d, n = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message]) #c^d mod n
    return decrypted_message

def encode_bit(input: str) -> list:
    output = []
    for char in input:
        bits = bin(ord(char))[2:].zfill(8)
        output.extend([int(bit) for bit in bits])   
    return output

def convert_bits_to_numbers(binary_bits, bits_per_number=16):
    encrypted_message = []
    for i in range(0, len(binary_bits), bits_per_number):
        bit_segment = binary_bits[i:i+bits_per_number]
        # Converte o segmento de bits de volta para um número inteiro
        num = int(''.join(map(str, bit_segment)), 2)
        encrypted_message.append(num)
    return encrypted_message

def decode(mlt3_message: list):
    print('\nRecieved (Message -> Encrypted -> Bin -> MLT-3 Encoded):\n', mlt3_message)
    
    print('\nMLT-3 Plot:\n')
    plot_signal(mlt3_message)

    encrypted_message = decode_mlt3(mlt3_message)
    print('\nRecieved -> MLT-3 Decoded:\n', encrypted_message)

    encrypted_message_from_bits = convert_bits_to_numbers(encrypted_message)
    print('\nRecieved -> MLT-3 Decoded -> DeBin:\n', encrypted_message_from_bits)

    bit_message = decrypt_rsa(encrypted_message_from_bits, private_key)
    print('\nRecieved -> MLT-3 Decoded -> DeBin -> Decrypted:\n', bit_message)

    msg_bin_decrypt = encode_bit(bit_message)
    print('\n*Recieved -> MLT-3 Decoded -> DeBin -> Decrypted -> Bin:\n', msg_bin_decrypt)

    write_file('decoded_message.txt', bit_message)

def plot_signal(signal):
    plt.ion()
    
    t = list(range(len(signal)))
    plt.plot(t, signal, drawstyle='steps-post')
    plt.title("MLT-3")
    plt.xlabel("time (s)")
    plt.grid(True)
    plt.show()

    plt.pause(0.1)
    plt.ioff()


class SimpleRouter(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode('utf-8'))

        # Endpoint que envia a chave pública
        if self.path == '/send_public_key':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'public_key': public_key
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        # Endpoint para receber a mensagem criptografada
        elif self.path == '/receive_encrypted':
            encrypted_data = data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'Message received'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
            decode(encrypted_data)

def run_server():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, SimpleRouter)
    print("Serving on port 8080")
    httpd.serve_forever()
    

public_key, private_key = generate_rsa_keys(bits=8)
print('Public key (e, n):', public_key)
print('Private key (d, n):', private_key)
print('\n')

if __name__ == "__main__":
    run_server()