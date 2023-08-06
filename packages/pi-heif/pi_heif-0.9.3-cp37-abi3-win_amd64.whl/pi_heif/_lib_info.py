"""
Functions to get version and encoders/decoders info of embedded C libraries.
"""

from _pi_heif_cffi import ffi, lib

from .constants import HeifCompressionFormat


def libheif_version() -> str:
    """Wrapper around `libheif.heif_get_version`"""
    return ffi.string(lib.heif_get_version()).decode()


def have_decoder_for_format(format_id: HeifCompressionFormat) -> bool:
    """Wrapper around `libheif.heif_have_decoder_for_format`"""
    return lib.heif_have_decoder_for_format(format_id)


def have_encoder_for_format(format_id: HeifCompressionFormat) -> bool:
    """Wrapper around `libheif.heif_have_encoder_for_format`"""
    return lib.heif_have_encoder_for_format(format_id)


def libheif_info() -> dict:
    """Returns dictionary with available decoders & encoders and libheif version.
    Keys are `versions`, `decoders`, `encoders`.

    {'version': {
        'libheif': '1.14.0',
        'x265': 'x265 HEVC encoder (3.4+31-6722fce1f)',
        'aom': 'AOMedia Project AV1 Encoder 3.5.0'
        },
     'decoders': {'HEVC': 1, 'AV1': 1, 'AVC': 0},
     'encoders': {'HEVC': 1, 'AV1': 1, 'AVC': 0}
    }"""

    decoders = {}
    encoders = {}
    for format_id in (HeifCompressionFormat.HEVC, HeifCompressionFormat.AV1, HeifCompressionFormat.AVC):
        decoders[format_id.name] = have_decoder_for_format(format_id)
        encoders[format_id.name] = have_encoder_for_format(format_id)

    _version = {"libheif": libheif_version(), "x265": "", "aom": ""}
    p_enc_desc = ffi.new("struct heif_encoder_descriptor**")
    if lib.heif_context_get_encoder_descriptors(ffi.NULL, HeifCompressionFormat.HEVC, ffi.NULL, p_enc_desc, 1):
        p_enc_name = lib.heif_encoder_descriptor_get_name(p_enc_desc[0])
        _version["x265"] = ffi.string(p_enc_name).decode()
    if lib.heif_context_get_encoder_descriptors(ffi.NULL, HeifCompressionFormat.AV1, ffi.NULL, p_enc_desc, 1):
        p_enc_name = lib.heif_encoder_descriptor_get_name(p_enc_desc[0])
        _version["aom"] = ffi.string(p_enc_name).decode()

    return {"version": _version, "decoders": decoders, "encoders": encoders}
