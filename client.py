import requests
import json
import seaborn as sns
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
    encrypted_message = [pow(ord(char), e, n) for char in message] #c^e mod n
    return encrypted_message

def get_public_key():
    response = requests.post('http://localhost:8080/send_public_key', json={})
    response_data = response.json()
    public_key = tuple(response_data['public_key'])
    return public_key

def convert_to_binary(encrypted_message):
    binary_bits = []
    for num in encrypted_message:
        # Converte o número criptografado em binário e adiciona cada bit à lista
        bits = bin(num)[2:].zfill(16)  # Zera até 16 bits (ou ajuste conforme necessário)
        binary_bits.extend([int(bit) for bit in bits])  # Adiciona cada bit individualmente na lista
    return binary_bits
    
def encode(message_file='message.txt') -> list:
    public_key = get_public_key()


    string_message = read_file(message_file)
    print('\nMessage:\n', string_message)

    bit_message = encode_bit(string_message)
    print('\n*Message -> Bin:\n', bit_message)

    encrypted_message = encrypt_rsa(string_message, public_key)
    print('\n(TODO em ASCII estendido)Message -> Encrypted:\n', encrypted_message)

    binary_encrypted_message = convert_to_binary(encrypted_message)
    print('\nMessage -> Encrypted -> Bin:\n', binary_encrypted_message)

    mlt3_message = encode_mlt3(binary_encrypted_message)
    print('\nMessage -> Encrypted -> Bin -> MLT-3 Encoded:\n', mlt3_message)

    print('\n(TODO)MLT-3 Plot:\n')
    #plot(string_message, bit_message, mlt3_message)

    return mlt3_message


def send_encrypted_message_to_server(encrypted_message):
    response = requests.post('http://localhost:8080/receive_encrypted', data=json.dumps(encrypted_message), headers={'Content-Type': 'application/json'})
    print('Response from server:', response.json())


def plot(string_input: str, bit_input: list, mlt3_input: list):
    fig, axs = plt.subplots(3, 1, figsize=(10, 6))

    # Plot the string input
    axs[0].text(0.5, 0.5, string_input, horizontalalignment='center', verticalalignment='center', fontsize=12)
    axs[0].set_title('String Input')
    axs[0].axis('off')

    # Plot the bit input
    sns.lineplot(x=range(len(bit_input)), y=bit_input, ax=axs[1], drawstyle='steps-pre')
    axs[1].set_title('Bit Input')
    axs[1].set_ylim(-0.5, 1.5)

    # Plot the MLT-3 input
    sns.lineplot(x=range(len(mlt3_input)), y=mlt3_input, ax=axs[2], drawstyle='steps-pre')
    axs[2].set_title('MLT-3 Input')
    axs[2].set_ylim(-1.5, 1.5)

    fig.suptitle('MLT-3 Encoding Visualization', fontsize=16)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    mlt3_message = encode()
    send_encrypted_message_to_server(mlt3_message)