import hashlib
from multiprocessing import Event, Queue
from typing import Optional, Callable, Dict

import bech32
import secp256k1

# on mac brew install automake pkg-config libtool libffi gmp

BECH32_CHARSET = "023456789acdefghjklmnpqrstuvwxyzACDEFGHJKLMNPQRSTUVWXYZ"

def generate_wallet():
    priv_key: secp256k1.PrivateKey = secp256k1.PrivateKey()
    pub_key: secp256k1.PublicKey = priv_key.pubkey
    byte_arr = pub_key.serialize(compressed=True)
    s = hashlib.new("sha256", byte_arr).digest()
    r = hashlib.new("ripemd160", s).digest()
    bech_addr = bech32.bech32_encode("cosmos", bech32.convertbits(r, 8, 5))
    return bech_addr, byte_arr.hex(), priv_key.serialize()

def ends_with(suffix: str, bech_addr: str) -> bool:
    return bech_addr.endswith(suffix)

def starts_with(prefix: str, bech_addr: str) -> bool:
    return bech_addr[7:].startswith(prefix)

def contains(vanity: str, bech_addr: str) -> bool:
    return vanity in bech_addr

def letters(vanity: str, bech_addr: str) -> bool:
    return vanity in bech_addr

def digits(vanity: str, bech_addr: str) -> bool:
    return vanity in bech_addr

def _is_valid_addr(predicates, candidate: str) -> Optional[str]:
    is_valid = set()
    for predicate, vanity in predicates.items():
        is_valid.add(predicate(vanity, candidate))
    if False in is_valid:
        return None
    return candidate


def find_vanity_addr(predicates: Dict[Callable, str], event: Event(), queue: Queue):
    while not event.is_set():
        candidate, pub, priv = generate_wallet()
        if _is_valid_addr(predicates, candidate):
            queue.put((candidate, pub, priv))
            event.set()
