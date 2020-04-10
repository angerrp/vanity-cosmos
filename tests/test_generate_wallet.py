import time

from unittest.mock import patch
from multiprocessing import Event, Queue, Process
from vanitycosmos.vanitycosmos import (
    generate_wallet,
    starts_with,
    ends_with,
    letters,
    digits,
    find_vanity_addr,
)

_WALLET = (
    "cosmos16zfzju9q6y9nfqeaxp3yvfvzvrx9rlam4ezznm",
    "0374a436044b4904bbd7a074b098d65fad39fc5b66f28da8440f10dbcf86568429",
    "b66022fff8b6322f8b8fa444d6d097457b6b9e7bb05add5b75f9c827df7bd3b6",
)


def test_generate_wallet():
    mocked_rand = b"\xb6`\"\xff\xf8\xb62/\x8b\x8f\xa4D\xd6\xd0\x97E{k\x9e{\xb0Z\xdd[u\xf9\xc8'\xdf{\xd3\xb6"

    with patch("os.urandom", return_value=mocked_rand):
        wallet = generate_wallet()
        assert wallet == _WALLET


def test_starts_with():
    assert starts_with("aaa", "cosmos1aaa")


def test_endswith():
    assert ends_with("aaa", "cosmos1ldsfjalsaaa")


def test_letters():
    assert letters(5, "cosmos1aaaaa6")


def test_digits():
    assert digits(5, "cosmos112345")


def _trigger_event(event: Event):
    time.sleep(1)
    event.set()


def test_find_vanity_address_success():
    predicates = {
        starts_with: "0000",
        ends_with: "0000",
    }
    event = Event()
    queue_mock = Queue()
    process = Process(target=_trigger_event, args=(event,))
    process.start()
    with patch("vanitycosmos.vanitycosmos.starts_with", return_value=True), patch(
        "vanitycosmos.vanitycosmos.ends_with", return_value=True
    ):
        find_vanity_addr(predicates, event, queue_mock)


def test_find_vanity_address_fails():
    predicates = {
        starts_with: "0000",
        ends_with: "0000",
    }
    event = Event()
    queue_mock = Queue()
    process = Process(target=_trigger_event, args=(event,))
    process.start()
    with patch("vanitycosmos.vanitycosmos.starts_with", return_value=False), patch(
        "vanitycosmos.vanitycosmos.ends_with", return_value=False
    ):
        find_vanity_addr(predicates, event, queue_mock)
