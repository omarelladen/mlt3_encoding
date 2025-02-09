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


def encrypt(input: list) -> list:
    output = input
    
    # TODO: Implement encryption algorithm
    
    return output


def encode(message_file='message.txt') -> list:
    string_message = read_file(message_file)

    bit_message = encode_bit(string_message)
    print('\nEncode(Bit): \n\t* encoded:', bit_message ,'\n\t* decoded:', string_message)

    encrypt_message = encrypt(bit_message)
    print('\nEncrypt: \n\t* encrypted:', encrypt_message ,'\n\t* decrypted:', bit_message)

    mlt3_message = encode_mlt3(encrypt_message)
    print('\nEncode(MLT3): \n\t* encoded:', mlt3_message ,'\n\t* decoded:', encrypt_message)


    requests.post('http://localhost:8080', data=json.dumps(mlt3_message), headers={'Content-Type': 'application/json'})
    plot(string_message, bit_message, mlt3_message)

    return mlt3_message

#-----------------------------------------------------------
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
    encode()