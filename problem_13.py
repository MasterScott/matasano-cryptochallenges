from collections import OrderedDict
from crypto_library import ecb_aes_encrypt, ecb_aes_decrypt
from problem_12 import find_blocksize
from crypto_library import apply_pkcs_7_padding

ENCRYPTION_KEY = ',y!3<CWn@1?wwF]\x0b'


def oracle(adversary_input):
    profile = profile_for(adversary_input)
    return ecb_aes_encrypt(profile, ENCRYPTION_KEY)


def destructure(structured):
    attrs = structured.split('&')
    destructured = {}
    for a in attrs:
        parameter, value = a.split('=')
        destructured[parameter] = value
    return OrderedDict(destructured)


def structure(destructured):
    return '&'.join([
        '='.join([parameter, value]) for parameter, value in destructured.items()
    ])


def profile_for(email_addr):
    if '&' in email_addr or '=' in email_addr:
        raise ValueError('Email address cannot contain "&" or "="')
    return structure(OrderedDict([
        ('email', email_addr),
        ('uid', '10'),
        ('role', 'user')
    ]))

blocksize = find_blocksize(oracle)

# Admin mail length should result in length("email=<admin_mail>&uid=10&role=") multiple of blocksize
admin_mail = 'jim1@test.com'
ciphertext = oracle(admin_mail)
# All blocks minus the last are the encryption of "email=<admin_mail>&uid=10&role="
cipher_blocks = [ciphertext[i*blocksize:(i+1)*blocksize] for i in range(len(ciphertext)/blocksize)]

padded_admin = apply_pkcs_7_padding('admin')
encrypted_padded_admin = oracle((blocksize-len('email='))*'0' + padded_admin)
encrypted_padded_admin_blocks = [encrypted_padded_admin[i*blocksize:(i+1)*blocksize] for i in range(len(encrypted_padded_admin)/blocksize)]
# The second block is the encryption of the padded "admin" string
encrypted_padded_admin_block = encrypted_padded_admin_blocks[1]

# Replace the last block of the profile ciphertext with the valid padded "admin" block
admin_encrypted_profile = ''.join(cipher_blocks[:-1] + [encrypted_padded_admin_block])
print 'Encrypted:', admin_encrypted_profile
print 'Decrypted:', ecb_aes_decrypt(admin_encrypted_profile, ENCRYPTION_KEY)
