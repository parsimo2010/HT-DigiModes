# SPDX-License-Identifier: MIT
"""Host-only M17 channel framing from the public M17 Protocol Specification."""

from itertools import chain

# Appendix B, indexed most significant bit first.
RANDOMIZER = bytes.fromhex(
    "d6b5e23082ff8462ba4e9690d898dd5d0cc85243911df8"
    "6e682f35da14eacd76198dd580d133871357182d2978c3"
)
LEVELS = (1, 3, -1, -3)


def bits(data):
    return [(byte >> shift) & 1 for byte in data for shift in range(7, -1, -1)]


def crc16(data):
    crc = 0xffff
    for bit in bits(data):
        feedback = (crc >> 15) ^ bit
        crc = (crc << 1) & 0xffff
        if feedback:
            crc ^= 0x5935
    return crc


def convolutional(data, puncture):
    """Convolutional encoding with four terminating zeros and periodic puncturing."""
    state = 0
    encoded = []
    for bit in chain(bits(data), (0, 0, 0, 0)):
        state = ((state << 1) | bit) & 31
        for taps in (0x19, 0x17):
            encoded.append(bin(state & taps).count("1") % 2)
    return [bit for i, bit in enumerate(encoded) if puncture[i % len(puncture)]]


def channel_frame(sync, coded):
    if len(coded) != 368:
        raise ValueError("M17 frame requires 368 coded payload bits")
    result = bits(sync.to_bytes(2, "big"))
    for i, mask in enumerate(bits(RANDOMIZER)):
        j = (45 * i + 92 * i * i) % 368
        result.append(coded[j] ^ mask)
    return result


def link_setup_bits(link_data):
    """Encode 28 bytes (destination, source, type and META) into 384 channel bits."""
    if len(link_data) != 28:
        raise ValueError("Link setup data must contain 28 bytes")
    lsf = link_data + crc16(link_data).to_bytes(2, "big")
    return channel_frame(0x55f7, convolutional(lsf, [1] + [1, 0, 1, 1] * 15))


def golay24(word):
    remainder = word << 11
    for degree in range(22, 10, -1):
        if remainder & (1 << degree):
            remainder ^= 0xc75 << (degree - 11)
    code = (word << 11) | remainder
    return (code << 1) | (bin(code).count("1") % 2)


def stream_bits(link_fragment, fragment_index, number, payload):
    """Encode one stream frame using a five-byte fragment of the 30-byte LSF."""
    if len(link_fragment) != 5 or not 0 <= fragment_index < 6:
        raise ValueError("Expected one of six five-byte link information fragments")
    if len(payload) != 16 or not 0 <= number <= 0xffff:
        raise ValueError("Expected a 16-bit frame number and 16 payload bytes")
    lich = (int.from_bytes(link_fragment, "big") << 8) | (fragment_index << 5)
    protected = bytearray()
    for shift in (36, 24, 12, 0):
        word = (lich >> shift) & 0xfff
        protected.extend(golay24(word).to_bytes(3, "big"))
    stream = number.to_bytes(2, "big") + payload
    return channel_frame(0xff5d, bits(protected) + convolutional(stream, [1] * 11 + [0]))


def symbols(frame_bits):
    if len(frame_bits) != 384 or any(bit not in (0, 1) for bit in frame_bits):
        raise ValueError("Expected 384 binary channel bits")
    return [LEVELS[2 * high + low] for high, low in zip(frame_bits[::2], frame_bits[1::2])]
