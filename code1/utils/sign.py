# import time
# from cryptography.hazmat.primitives.asymmetric import ed25519
# from cryptography.hazmat.primitives import serialization
# from hashlib import sha256
# import pickle

# # 生成客户端的公私钥
# def generate_eddsa_keys():
#     # 生成私钥和公钥（Ed25519）
#     private_key = ed25519.Ed25519PrivateKey.generate()
#     public_key = private_key.public_key()
    
#     return private_key, public_key

# # 将私钥和公钥转换为字节形式（便于存储和pickle序列化）
# def serialize_key(key):
#     return key.private_bytes(
#         encoding=serialization.Encoding.Raw,
#         format=serialization.PrivateFormat.Raw,
#         encryption_algorithm=serialization.NoEncryption()
#     ) if isinstance(key, ed25519.Ed25519PrivateKey) else key.public_bytes(
#         encoding=serialization.Encoding.Raw,
#         format=serialization.PublicFormat.Raw
#     )

# # 从字节形式恢复私钥和公钥
# def deserialize_private_key(serialized_key):
#     return ed25519.Ed25519PrivateKey.from_private_bytes(serialized_key)

# def deserialize_public_key(serialized_key):
#     return ed25519.Ed25519PublicKey.from_public_bytes(serialized_key)

# # 客户端签名函数
# def sign_message(private_key, c_id, mask, cipher):
#     # 计算消息构造时间
#     message_start_time = time.time()
#     message = f"{c_id}_{mask}_{cipher}"
#     # c_id = str(c_id)
#     # mask = str(mask)
#     # cipher = str(cipher)
#     # message = '_'.join([c_id, mask, cipher])
#     message_end_time = time.time()
    
#     # 计算消息的哈希值
#     msg_hash_start_time = time.time()
#     msg_hash = sha256(message.encode('utf-8')).digest()
#     msg_hash_end_time = time.time()

#     # 使用 EdDSA 对消息哈希进行签名
#     signature_start_time = time.time()
#     signature = private_key.sign(msg_hash)
#     signature_end_time = time.time()
    
#     # 输出每一步的时间开销
#     print(f"Message Construction Time: {message_end_time - message_start_time:.6f} seconds")
#     print(f"Message Hash Time: {msg_hash_end_time - msg_hash_start_time:.6f} seconds")
#     print(f"Signature Generation Time: {signature_end_time - signature_start_time:.6f} seconds")
    
#     return signature, msg_hash

# # 生成8个客户端的公私钥
# clients_keys = {}
# for i in range(8):
#     private_key, public_key = generate_eddsa_keys()
#     clients_keys[i] = {
#         'private_key': serialize_key(private_key),
#         'public_key': serialize_key(public_key)
#     }

# # 将客户端的公私钥存入文件（可选）
# with open('clients_keys.pkl', 'wb') as f:
#     pickle.dump(clients_keys, f)

import time
from blspy import AugSchemeMPL, G1Element, G2Element, PrivateKey
from hashlib import sha256
import os
import pickle

# 生成客户端的公私钥
def generate_bls_keys():
    seed = os.urandom(32)
    private_key = AugSchemeMPL.key_gen(seed)
    public_key = private_key.get_g1()
    
    return private_key, public_key

# 将私钥和公钥序列化为字节
def serialize_keys(private_key, public_key):
    sk_bytes = bytes(private_key)  # 32 bytes
    pk_bytes = bytes(public_key)  # 48 bytes
    return sk_bytes, pk_bytes

# 从字节反序列化私钥和公钥
def deserialize_keys(sk_bytes, pk_bytes):
    private_key = PrivateKey.from_bytes(sk_bytes)
    public_key = G1Element.from_bytes(pk_bytes)
    return private_key, public_key

# 客户端签名函数
def sign_message(private_key, c_id, cipher, mask):
    # 拼接消息
    message = f"{c_id}_{cipher}_{mask}"
    # 计算消息的哈希值
    msg_hash = sha256(message.encode('utf-8')).digest()
    
    # 使用 BLS 对消息哈希进行签名
    signature = AugSchemeMPL.sign(private_key, msg_hash)
    
    return signature, msg_hash

# 生成8个客户端的公私钥并存储
clients_keys = {}
for i in range(8):
    private_key, public_key = generate_bls_keys()
    sk_bytes, pk_bytes = serialize_keys(private_key, public_key)
    clients_keys[i] = {
        'private_key': sk_bytes,
        'public_key': pk_bytes
    }

# 将客户端的公私钥存入文件
with open('clients_keys.pkl', 'wb') as f:
    pickle.dump(clients_keys, f)