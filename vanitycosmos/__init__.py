import multiprocessing as mp
from multiprocessing import Event, Manager, Pool, Queue
from typing import Optional, Callable, Set, List

import secp256k1
import hashlib
import bech32

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

def _ends_with(suffix: str, bech_addr: str) -> bool:
    return bech_addr.endswith(suffix)

def _starts_with(prefix: str, bech_addr: str) -> bool:
    return bech_addr[7:].startswith(prefix)

def _contains(vanity: str, bech_addr: str) -> bool:
    return vanity in bech_addr

def _is_valid_addr(vanity: str, predicates, candidate: str) -> Optional[str]:
    is_valid = set()
    for predicate in predicates:
        is_valid.add(predicate(vanity, candidate))
    if len(is_valid) > 1:
        return None
    return candidate


def find_vanity_addr(vanity: str, predicates: List[Callable], event: Event(), queue: Queue):
    while not event.is_set():
        candidate, pub, priv = generate_wallet()
        if _is_valid_addr(vanity, predicates, candidate):
            queue.put((candidate, pub, priv))
            event.set()


test = "paul"

for c in test:
    if c not in BECH32_CHARSET:
        print(f"ERROR: character not {c} not in bech32 charset")
