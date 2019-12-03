from __future__ import annotations

from cryptography.hazmat.primitives import serialization

from codemagic_cli_tools.models import Certificate
from codemagic_cli_tools.models import PrivateKey

public_bytes = \
    b'-----BEGIN CERTIFICATE REQUEST-----\n' \
    b'MIICZDCCAUwCAQAwDjEMMAoGA1UEAwwDUEVNMIIBIjANBgkqhkiG9w0BAQEFAAOC\n' \
    b'AQ8AMIIBCgKCAQEA0L+h5RVDhRpTjNttmXX5n0gNOVYTvSNPYRcNFlSISboQStDm\n' \
    b'I65Ncv3Snsun7pzZfCSo+si/JFYw/C8hrwHTEmHS2AbK94w1oSYiQ1fiSKszmtc7\n' \
    b'khw0vRUPJyzr+Ib8otXsdAgzpCoFYe6nQn3I/QWufLb3EOiul5R5yq6dMhhs0Fgc\n' \
    b'y9hKA74ADk3TEk2cxz/9FyaNoc2MiQmkKX1WPWM74LVMKo0HXtp2xYZKVmX4hLaK\n' \
    b'5w2fHP7qvm0wVTt5B3IJrgDEvg25/irYudIuy4T6gWOvhvUfJYDCqZ0N2kdGi3kQ\n' \
    b'uguGTABIjdB54/9FN/ZyX3UL7fqRg9jG7P4i4QIDAQABoBEwDwYJKoZIhvcNAQkO\n' \
    b'MQIwADANBgkqhkiG9w0BAQsFAAOCAQEAv2/0ny9h+I/vikx88yyRGM8P6M7/tf85\n' \
    b'/74pVXF29IcZQp7znL+U+n9A8dNT1oQXZoTgX6wdkm3s5ICPJ++o9nrbEhtfmidq\n' \
    b'S5FayCrBUdHYBTjctn9twbAk8fH1rYseJpV4IMgoLM6tsfdKsPAzSC3TXLjcfi2/\n' \
    b'hm71Rcn+dc4U90D4VS+SHXlkhIgzCQ0/Z3s1+C8ivZH4xg3KpcBlWd/a38tpbVqe\n' \
    b'2eaWoUwyRzv3cDOOGbxecHnohTVV4Ck7afAPoGnkobN9jUz51PFHFYBBMu0c/bWI\n' \
    b'B6TOwQ+xSyp1ZMFenb75fp6hzZmoPY+OMvVbO49YJuv3AHioZ3d1Cg==\n' \
    b'-----END CERTIFICATE REQUEST-----\n'


def test_create_certificate_signing_request(unencrypted_pem):
    rsa = PrivateKey.pem_to_rsa(unencrypted_pem.content)
    csr = Certificate.create_certificate_signing_request(rsa)
    assert csr.signature_hash_algorithm.name == 'sha256'
    assert csr.is_signature_valid is True
    assert csr.public_bytes(serialization.Encoding.PEM) == public_bytes