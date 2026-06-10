import hashlib
from datetime import datetime

from src.core.security.anonymizer import PIIAnonymizer
from src.core.contracts.review_contract import PlayStoreReviewContract


def test_hash_sha256_valid_string():
    input_str = "JohnDoe123"
    expected_hash = hashlib.sha256(input_str.encode("utf-8")).hexdigest()
    assert PIIAnonymizer.hash_sha256(input_str) == expected_hash


def test_hash_sha256_empty_string():
    assert PIIAnonymizer.hash_sha256("") == ""


def test_hash_sha256_none():
    assert PIIAnonymizer.hash_sha256(None) is None


def test_hash_sha256_determinism():
    input_str = "Alice"
    hash1 = PIIAnonymizer.hash_sha256(input_str)
    hash2 = PIIAnonymizer.hash_sha256(input_str)
    assert hash1 == hash2


def test_review_contract_anonymization():
    user_name = "RealUser"
    user_image = "http://example.com/image.png"

    contract = PlayStoreReviewContract(
        reviewId="123",
        userName=user_name,
        userImage=user_image,
        score=5,
        thumbsUpCount=0,
        at=datetime.now(),
    )

    expected_name_hash = PIIAnonymizer.hash_sha256(user_name)
    expected_image_hash = PIIAnonymizer.hash_sha256(user_image)

    assert contract.userName == expected_name_hash
    assert contract.userImage == expected_image_hash
