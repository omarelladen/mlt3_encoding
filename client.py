# import matplotlib
# matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json


def get_public_key() -> tuple:
    response = requests.post('http://localhost:8080/send_public_key', json={})
    response_data = response.json()
    public_key = tuple(response_data['public_key'])
    return public_key

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        message = file.read()
    return message

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

def str_to_bin(input: str, n_bits: int) -> list: #Unicode
    output = []
    for char in input:
        bits = bin(ord(char))[2:].zfill(n_bits)
        output.extend([int(bit) for bit in bits])   
    return output

# RSA character by character
def encrypt_rsa(message: str, public_key: tuple) -> list:
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message] #c^e mod n
    return encrypted_message

def num_to_bin(input: list, n_bits: int) -> list:
    binary_bits = []
    for num in input:
        bits = bin(num)[2:].zfill(n_bits)  # Zera até 16 bits
        binary_bits.extend([int(bit) for bit in bits])
    return binary_bits

def bin_to_8bit_char(bin_list: list) -> list:
    if len(bin_list) % 8 != 0:
        raise ValueError("The list must have a number of elements that is a multiple of 8")
    
    characters = []
    for i in range(0, len(bin_list), 8):
        byte = bin_list[i:i+8]
        byte_int = int("".join(map(str, byte)), 2)
        characters.append(chr(byte_int))
    
    return characters

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

def send_encrypted_message_to_server(encrypted_message):
    response = requests.post('http://localhost:8080/receive_encrypted', data=json.dumps(encrypted_message), headers={'Content-Type': 'application/json'})
    print('Response from server:', response.json())

def encode(message_file_path='message.txt') -> list:
    public_key = get_public_key()

    string_message = read_file(message_file_path)
    print('\nMessage:\n', string_message)

    bit_message = str_to_bin(string_message, 8)
    print('\nMessage -> Bin:\n', bit_message)

    encrypted_message = encrypt_rsa(string_message, public_key)
    print('\nMessage -> Encrypted:\n', encrypted_message)

    binary_encrypted_message = num_to_bin(encrypted_message, 16)
    print('\nMessage -> Encrypted -> Bin:\n', binary_encrypted_message)

    char_encrypted_message = bin_to_8bit_char(binary_encrypted_message)
    print('\nMessage -> Encrypted -> Bin -> Char 8bits:\n', char_encrypted_message)

    mlt3_message = encode_mlt3(binary_encrypted_message)
    print('\nMessage -> Encrypted -> Bin -> MLT-3 Encoded:\n', mlt3_message)

    plot_signal(mlt3_message)

    return mlt3_message

if __name__ == "__main__":
    mlt3_message = encode()
    send_encrypted_message_to_server(mlt3_message)