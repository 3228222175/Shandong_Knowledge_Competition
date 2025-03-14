const CryptoJs=require('crypto-js')

function encode(e) {
    var t = CryptoJs.enc.Utf8.parse('86aehGlzU3PKCh5i')
        , r = CryptoJs.AES.encrypt(JSON.stringify(e), t, {
        mode: CryptoJs.mode.ECB,
        padding: CryptoJs.pad.Pkcs7
    })
        , i = r.ciphertext.toString().toUpperCase()
        , o = CryptoJs.enc.Hex.parse(i);
    console.log(CryptoJs.enc.Base64.stringify(o))
    return CryptoJs.enc.Base64.stringify(o)
}


function decode(e)
{
    var t = CryptoJs.enc.Utf8.parse('86aehGlzU3PKCh5i')
              , r = CryptoJs.AES.decrypt(e, t, {
                mode: CryptoJs.mode.ECB,
                padding: CryptoJs.pad.Pkcs7
            })
              , i = r.toString(CryptoJs.enc.Utf8);
    console.log(JSON.parse(i))
            return JSON.parse(i)
}
