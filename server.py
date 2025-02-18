from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import seaborn as sns
import matplotlib.pyplot as plt

def write_file(file_name: str, content: str):
    with open(file_name, 'w') as file:
        file.write(content)


def decode_bit(input: list) -> str:
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

def decrypt(input: list) -> list:
    output = input
    
    # TODO: Implement decryption algorithm

    return output

def decode(mlt3_message: list):
    encrypt_message = decode_mlt3(mlt3_message)
    print('\nDecode(MLT3): \n\t* encoded:', mlt3_message ,'\n\t* decoded:', encrypt_message)

    bit_message = decrypt(encrypt_message)
    print('\nDecrypt: \n\t* encoded:', encrypt_message ,'\n\t* decoded:', bit_message)

    string_message = decode_bit(bit_message)
    print('\nDecode(Bit): \n\t* encoded:', bit_message ,'\n\t* decoded:', string_message)

    write_file('decoded_message.txt', string_message)
    plot(string_message, bit_message, mlt3_message)

#-----------------------------------------------------------
class SimpleRouter(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length).decode('utf-8'))
        self.send_response(200)
        self.end_headers()
        decode(data)

def run_server():
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, SimpleRouter)
    print("Serving on port 8080")
    httpd.serve_forever()
    
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

    fig.suptitle('MLT-3 Decoding Visualization', fontsize=16)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    run_server()