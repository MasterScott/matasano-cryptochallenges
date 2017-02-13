from vigenere import solve_repeating_key_xor


if __name__ == '__main__':
    with open('6.txt', 'r') as f:
        text = ''.join(f.readlines())
    cleaned_text = text.decode('base64')
    print solve_repeating_key_xor(cleaned_text)
