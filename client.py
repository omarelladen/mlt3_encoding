import requests
import json
import seaborn as sns
import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt


def read_file(file_name: str) -> str:
    with open(file_name, 'r') as file:
        message = file.read()
    return message

def encode_bit(input: str) -> list:
    output = []
    for char in input:
        bits = bin(ord(char))[2:].zfill(8)
        output.extend([int(bit) for bit in bits])   
    return output

def encode_mlt3(input: list) -> list:    
    mlt3_data = []

    # First output signal is the same
    signal_out = input[0]
    mlt3_data.append(signal_out)

    # Sign initialization
    if signal_out == 1:
        sign = 1
    else:
        sign = -1

    # MLT-3 encoding
    for i in range(1, len(input)):
        if input[i] == 1:
            if signal_out == 0:
                sign *= -1
                signal_out = sign
            else:
                signal_out = 0
        mlt3_data.append(signal_out)

    return mlt3_data

# RSA caracter por caracter
def encrypt_rsa(message, public_key):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message] #
    return encrypted_message

def get_public_key():
    response = requests.post('http://localhost:8080/send_public_key', json={})
    response_data = response.json()
    public_key = tuple(response_data['public_key'])
    return public_key

def convert_to_binary(encrypted_message):
    binary_bits = []
    for num in encrypted_message:
        bits = bin(num)[2:].zfill(16)  # Zera até 16 bits
        binary_bits.extend([int(bit) for bit in bits])  # Adiciona cada bit individualmente na lista
    return binary_bits

def bin_to_character(bin_lista):
    if len(bin_lista) % 8 != 0:
        raise ValueError("A lista deve ter um número de elementos múltiplo de 8")
    
    caracteres = []
    for i in range(0, len(bin_lista), 8):
        byte = bin_lista[i:i+8]
        byte_int = int("".join(map(str, byte)), 2)
        caracteres.append(chr(byte_int))
    
    return caracteres

def encode(message_file='message.txt') -> list:
    public_key = get_public_key()


    string_message = read_file(message_file)
    print('\nMessage:\n', string_message)

    bit_message = encode_bit(string_message)
    print('\nMessage -> Bin:\n', bit_message)

    encrypted_message = encrypt_rsa(string_message, public_key)
    print('\n(TODO em ASCII estendido)Message -> Encrypted:\n', encrypted_message)

    binary_encrypted_message = convert_to_binary(encrypted_message)
    print('\nMessage -> Encrypted -> Bin:\n', binary_encrypted_message)

    char_encrypted_message = bin_to_character(binary_encrypted_message)
    print('\nMessage -> Encrypted -> Bin -> Char 8bits:\n', char_encrypted_message)

    mlt3_message = encode_mlt3(binary_encrypted_message)
    print('\nMessage -> Encrypted -> Bin -> MLT-3 Encoded:\n', mlt3_message)

    print('\nMLT-3 Plot:\n')
    plot_signal(mlt3_message)

    return mlt3_message


def send_encrypted_message_to_server(encrypted_message):
    response = requests.post('http://localhost:8080/receive_encrypted', data=json.dumps(encrypted_message), headers={'Content-Type': 'application/json'})
    print('Response from server:', response.json())

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

if __name__ == "__main__":
    mlt3_message = encode()
    send_encrypted_message_to_server(mlt3_message)