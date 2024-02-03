def get_compress_type_str(compression_type: int) -> str:
    match compression_type:
        case 0:
            return "ZIP_STORED"
        case 8:
            return "ZIP_DEFLATED"
        case 12:
            return "ZIP_BZIP2"
        case 14:
            return "ZIP_LZMA"
        case _:
            return "UNKNOWN"
