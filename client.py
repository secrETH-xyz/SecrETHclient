from threshold_crypto.threshold_crypto import *

# load signer's key_share
curve_params = CurveParameters()
thresh_params = ThresholdParameters(t=3, n=5)
pub_key, key_shares = create_public_key_and_shares_centralized(curve_params, thresh_params)
signers_index = 0

key_share = key_shares[signers_index]

# get encrypted_message from the blockchain
message = 'Some secret message to be encrypted :)' 
encrypted_message = encrypt_message(message, pub_key)
encrypted_message_C1_x = str(encrypted_message.C1.x)
encrypted_message_C1_y = str(encrypted_message.C1.y)
encrypted_message_C2_x = str(encrypted_message.C2.x)
encrypted_message_C2_y = str(encrypted_message.C2.y)
encrypted_message_ciphertext = str(encrypted_message.ciphertext)

def computePartialDecryption(_encrypted_message_C1_x, _encrypted_message_C1_y, _encrypted_message_C2_x, _encrypted_message_C2_y, _encrypted_message_ciphertext, participant_share = key_share):
    _encrypted_message_C1 = ECC.EccPoint(int(_encrypted_message_C1_x), int(_encrypted_message_C1_y))
    _encrypted_message_C2 = ECC.EccPoint(int(_encrypted_message_C2_x), int(_encrypted_message_C2_y))
    _encrypted_message = EncryptedMessage(_encrypted_message_C1, _encrypted_message_C2, bytes(_encrypted_message_ciphertext, encoding='utf-8'))
    partial_decryption = compute_partial_decryption(_encrypted_message, participant_share)
    return (partial_decryption.x, partial_decryption.yC1.x, partial_decryption.yC1.y) # these values are uploaded to the blockchain

# get partial decryptions from the blockchain
partial_decryptions = []
for participant in [0, 2, 4]:
    participant_share = key_shares[participant]
    partial_decryption = computePartialDecryption(encrypted_message_C1_x, encrypted_message_C1_y, encrypted_message_C2_x, encrypted_message_C2_y, encrypted_message_ciphertext, participant_share)
    partial_decryptions.append(partial_decryption)

partial_decryptions_formatted = []
def decryptMessage(partial_decryptions):
    for partial_decryption in partial_decryptions:
        partial_decryptions_formatted.append(PartialDecryption(partial_decryption[0], ECC.EccPoint(partial_decryption[1], partial_decryption[2]), curve_params))
    return decrypt_message(partial_decryptions_formatted, encrypted_message, thresh_params) # if CipherInfo.storeDecryption == true, submit to the blockchain and earn fees