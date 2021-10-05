import treepoem
import io
import base64

b_codes = {
    'UPC_A': 'upca',
    'UPC_E': 'upce',
    'EAN_8': 'ean8',
    'EAN_13': 'ean13',
    'CODE_39': 'code39',
    # 'CODE_39_MOD_43': 'code39ext',       ###
    'CODE_93': 'code93',
    # 'CODABAR',
    'CODE_128': 'code128',
    'ITF': 'interleaved2of5',
    'ITF_14': 'itf14',
    'AZTEC': 'azteccode',
    'DATA_MATRIX': 'datamatrix',
    'MAXICODE': 'maxicode',
    'PDF_417': 'pdf417',
    'QR_CODE': 'qrcode',
    # 'RSS_14',
    # 'RSS_EXPANDED',
}


def generate_code(type_, value):
    t_v = {k: v for k, v in b_codes.items() if k == type_}
    print(t_v)
    k = next(iter(t_v))
    g_code = get_barcode(t_v[k], value)
    return g_code


def get_barcode(type_, text):

    barcode_content = text
    if type_ == 'qrcode':
       image = treepoem.generate_barcode(
                barcode_type=type_,
                data=barcode_content,
                options={"parsefnc":True, 'height': '0.88', 'width': '0.88'}
       )
    else:
       image = treepoem.generate_barcode(
                   barcode_type=type_,
                   data=barcode_content,
                   options={"parsefnc": True, 'height': '0.475'}
       )
    buffered = io.BytesIO()
    image.convert('1').save(buffered, 'png')
    barcode_64 = base64.b64encode(buffered.getvalue())
    return barcode_64








