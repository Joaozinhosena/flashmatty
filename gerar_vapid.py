import base64

from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)


def b64url(
    dados
):

    return (
        base64
        .urlsafe_b64encode(
            dados
        )
        .rstrip(
            b"="
        )
        .decode(
            "ascii"
        )
    )


chave_privada = (
    ec.generate_private_key(
        ec.SECP256R1()
    )
)


numero_privado = (
    chave_privada
    .private_numbers()
    .private_value
)


privada = (
    numero_privado
    .to_bytes(
        32,
        "big"
    )
)


publica = (

    chave_privada
    .public_key()
    .public_bytes(
        Encoding.X962,
        PublicFormat.UncompressedPoint
    )

)


print("")
print("============================================")
print(" FLASHMATTY - CHAVES VAPID")
print("============================================")
print("")

print(
    "VAPID_PUBLIC_KEY="
    +
    b64url(
        publica
    )
)

print("")

print(
    "VAPID_PRIVATE_KEY="
    +
    b64url(
        privada
    )
)

print("")