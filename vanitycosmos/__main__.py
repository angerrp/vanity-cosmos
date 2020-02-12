import argparse
import multiprocessing as mp
from multiprocessing import Manager, Pool

from cosmosvanity import BECH32_CHARSET
from cosmosvanity.cosmosvanity import ends_with, contains, starts_with, find_vanity_addr, letters, \
    digits


def main(vanity_dict, addresses):
    with Pool() as pool:
        manager = Manager()
        event = manager.Event()
        queue = manager.Queue()
        for i in range(addresses):
            [pool.apply_async(find_vanity_addr, args=(vanity_dict, event, queue)) for _ in range(mp.cpu_count())]
            print(queue.get())


def _is_valid_bech32(vanity: str):
    for c in vanity:
        if c not in BECH32_CHARSET:
            print(f"Not valid bech32 vanity input for {vanity}")
            exit(1)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cosmosvanity, create custom cosmos addresses.")
    parser.add_argument("--startswith", type=str, help="Find an address ending with the provided argument.")
    parser.add_argument("--endswith", type=str, help="Find an address starting with the provided argument.")
    parser.add_argument("--contains", type=str, help="Find an address containing the provided argument.")
    parser.add_argument("--letters", type=int, help="Find an address containing the provided number of letters.")
    parser.add_argument("--digits", type=int, help="Find an address containing the provided number of digits.")
    parser.add_argument("--addresses", type=int, help="Number of addresses to search for.", default=1)
    args = parser.parse_args()

    vanity_args = {}
    if args.startswith and _is_valid_bech32(args.startswith):
        vanity_args[starts_with] = str(args.startswith)
    if args.endswith and _is_valid_bech32(args.endswith):
        vanity_args[ends_with] = str(args.endswith)
    if args.contains and _is_valid_bech32(args.contains):
        vanity_args[contains] = args.contains
    if args.letters and _is_valid_bech32(args.letters):
        vanity_args[letters] = args.letters
    if args.digits and _is_valid_bech32(args.digits):
        vanity_args[digits] = args.digits
    main(vanity_args, args.addresses)
