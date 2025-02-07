from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import seaborn as sns
import matplotlib.pyplot as plt

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

def decode_mlt3(input: list) -> list:
    output = input

    print('\nDecode(MLT3): \n\t* encoded:', input ,'\n\t* decoded:', output)

    return output

def decode_bit(input: list) -> str:
    output = ''.join([chr(int(''.join(map(str, input[i:i+8])), 2)) for i in range(0, len(input), 8)])

    print('\nDecode(Bit): \n\t* encoded:', input ,'\n\t* decoded:', output)

    return output

def decode(mlt3_message: list):
    bit_message = decode_mlt3(mlt3_message)
    string_message = decode_bit(bit_message)
    plot(string_message, bit_message, mlt3_message)

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

if __name__ == "__main__":
    run_server()