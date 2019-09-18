import base64, codecs
magic = 'DQppbXBvcnQgYmFzZTY0LCBjb2RlY3MNCnRoZWNyZXcgPSAnYVcxd2IzSjBJSEpsY1hWbGMzUnpEUXBtY205dElHSnpOQ0JwYlhCdmNuUWdRbVZoZFhScFpuVnNVMjkxY0EwS2FXMXdiM0owSUhKbERRcHBiWEJ2Y25RZ2MzbHpEUW9OQ21kaGJXVmZiR2x6ZENBOUlGdGREUXBrWldZZ1oyVjBYMmRoYldVb0tUb05DaUFnSUNCSVpXRmtaWEp6SUQwZ2V5ZFZjMlZ5TFVGblpXNTBKeUE2SUNkTmIzcHBiR3hoTHpVdU1DQW9WMmx1Wkc5M2N5Qk9WQ0F4TUM0d095QlhhVzQyTkRzZ2VEWTBLU0JCY0hCc1pWZGxZa3RwZEM4MU16Y3VNellnS0V0SVZFMU1MQ0JzYVd0bElFZGxZMnR2S1NCRGFISnZiV1V2TmpBdU1DNHpNVEV5TGpFeE15QlRZV1poY21rdk5UTTNMak0ySnlCOURRb2dJQ0FnYkdsdWF5QTlJSEpsY1hWbGMzUnpMbWRsZENnbmFIUjBjRG92TDNsdmRYSnpjRzl5ZEhNdWMzUnlaV0Z0THljc2FHVmhaR1Z5Y3oxSVpXRmtaWEp6S1M1amIyNTBaVzUwRFFvZ0lDQWdjMjkxY0NBOUlFSmxZWFYwYVdaMWJGTnZkWEFvYkdsdWF5d2dKMmgwYld3dWNHRnljMlZ5SnlrTkNpQWdJQ0IwYVhSc1pWOXNhWE4wSUQwZ2MyOTFjQzVtYVc1a1gyRnNiQ2duYzNCaGJpY3NjM1I1YkdVOWV5ZG1iMjUwTFhkbGFXZG9kRHBpYjJ4a095ZDlLUTBLSUNBZ0lHWnZjaUIwYVhSc1pTQnBiaUIwYVhSc1pWOXNhWE4wT2cwS0lDQWdJQ0FnSUNBamNISnBiblFvZEdsMGJHVXVkR1Y0ZENrTkNpQWdJQ0FnSUNBZ1oyRnRaVjlzYVhOMExtRndjR1Z1WkNoN0ozUnBkR3hsSnpwMGFYUnNaUzUwWlhoMExtVnVZMjlrWlNnbllYTmphV2tuTENkcFoyNXZjbVVuS1gwcERRb05DaUFnSUNCeVpYUjFjbTRnWjJGdFpWOXNhWE4wRFFvTkNnMEtiR2wyWlNBOUlGdGREUXBrWldZZ1oyVjBYM04wY21WaGJTaG5ZVzFsS1RvTkNpQWdJQ0JJWldGa1pYSnpJRDBnZXlkVmMyVnlMVUZuWlc1MEp5QTZJQ2ROYjNwcGJHeGhMelV1TUNBb1YybHVaRzkzY3lCT1ZDQXhNQzR3T3lCWGFXNDJORHNnZURZMEtTQkJjSEJzWlZkbFlrdHBkQzgxTXpjdU16WWdLRXRJVkUxTUxDQnNhV3RsSUVkbFkydHZLU0JEYUhKdmJXVXZOakF1TUM0ek1URXlMakV4TXlCVFlXWmhjbWt2TlRNM0xqTTJKeUI5RFFvZ0lDQWdiR2x1YXlBOUlISmxjWFZsYzNSekxtZGxkQ2duYUhSMGNEb3ZMM2x2ZFhKemNHOXlkSE11YzNSeVpXRnRMeWNzYUdWaFpHVnljejFJWldGa1pYSnpLUzVqYjI1MFpXNTBEUW9nSUNBZ2MyOTFjQ0E5SUVKbFlYVjBhV1oxYkZOdmRYQW9iR2x1YXl3Z0oyaDBiV3d1Y0dGeWMyVnlKeWtOQ2lBZ0lDQnNhU0E5SUhOdmRYQXVabWx1WkY5aGJHd29KMnhwSnl3Z1kyeGhjM05mUFhzbmR6TXRZbUZ5SUhjekxYUmxlSFF0ZDJocGRHVWdkek10Y0dGa1pHbHVaeTF6YldGc2JDZDlLUTBLSUNBZ0lHWnZjaUJwSUdsdUlHeHBPZzBLSUNBZ0lDQWdJQ0IwY25rNkRRb2dJQ0FnSUNBZ0lDQWdJQ0IwYVhSc1pTQTlJR2t1Wm1sdVpDZ25jM0JoYmknDQpkb2VzbnQgPSAncGZwM0U1b1RIOXJscXpvMjUwWUtxeW5KcWJxUWN2bzJreEJscTlYRDBYVlBOdFZQTnRWUE50VlBOdHFUeTBvVEh0Q0ZPMG5LRWZNRjUwTUt1MF'
love = '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'
god = 'SEowY3k1NGVYb3ZKeUFySUdodmJXVmZabVZsWkY5MWNtd05DaUFnSUNBZ0lDQWdJQ0FnSUd4cGJtc2dQU0J5WlhGMVpYTjBjeTVuWlhRb2JXRnpkR1Z5WDJGM1lYbGZkWEpzTENCb1pXRmtaWEp6UFVobFlXUmxjbk1wTG1OdmJuUmxiblFOQ2lBZ0lDQWdJQ0FnSUNBZ0lHMHpkVGhmWVhkaGVTQTlJSEpsTG1acGJtUmhiR3dvSnljbmRtRnlYSE1yYlhWemRHRjJaVDFiSnlKZEtGdGVKeUpkS3lsYkp5SmRMaW8vSnljbkxITjBjaWhzYVc1cktTeG1iR0ZuY3oxeVpTNUVUMVJCVEV3cFd6QmREUW9nSUNBZ0lDQWdJQ0FnSUNCc2FXNXJJRDBnY21WeGRXVnpkSE11WjJWMEtHMWhjM1JsY2w5b2IyMWxYM1Z5YkN3Z2FHVmhaR1Z5Y3oxSVpXRmtaWEp6S1M1amIyNTBaVzUwRFFvZ0lDQWdJQ0FnSUNBZ0lDQnRNM1U0WDJodmJXVWdQU0J5WlM1bWFXNWtZV3hzS0NjbkozWmhjbHh6SzIxMWMzUmhkbVU5V3ljaVhTaGJYaWNpWFNzcFd5Y2lYUzRxUHljbkp5eHpkSElvYkdsdWF5a3NabXhoWjNNOWNtVXVSRTlVUVV4TUtWc3dYUTBLSUNBZ0lDQWdJQ0FnSUNBZ2JUTjFPRjloZDJGNUlEMGdiVE4xT0Y5aGQyRjVMbkpsY0d4aFkyVW9JajkyUFNJc0p5Y3BJQTBLSUNBZ0lDQWdJQ0FnSUNBZ2JUTjFPRjlvYjIxbElEMGdiVE4xT0Y5b2IyMWxMbkpsY0d4aFkyVW9JajkyUFNJc0p5Y3BEUW9nSUNBZ0lDQWdJQ0FnSUNCcGJtUmxlRjloZDJGNUlEMGdiVE4xT0Y5aGQyRjVMbVpwYm1Rb0oyaDBkSEJ6SnlrTkNpQWdJQ0FnSUNBZ0lDQWdJR2xtSUdsdVpHVjRYMkYzWVhrZ0lUMGdMVEU2RFFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnYlROMU9GOWhkMkY1SUQwZ2JUTjFPRjloZDJGNVcybHVaR1Y0WDJGM1lYazZYUTBLSUNBZ0lDQWdJQ0FnSUNBZ0lDQWdJRzB6ZFRoZllYZGhlU0E5SUcwemRUaGZZWGRoZVM1eVpYQnNZV05sS0NkamIyMXdiR1YwWlNjc0ozTnNhV1JsSnlrZ0t5QnRiR0pCZFhSb0RRb2dJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0kyMHpkVGhmWVhkaGVTQTlJRzB6ZFRoZllYZGhlUzV5WlhCc1lXTmxLQ2RvZEhSd2N5Y3NKMmgwZEhBbktRMEtJQ0FnSUNBZ0lDQWdJQ0FnSUNBZ0lHMHpkVGhmWVhkaGVTQTlJRzB6ZFRoZllYZGhlUzV5WlhCc1lXTmxLQ2R0WVhOMFpYSmZaR1Z6YTNSdmNGOXpiR2xrWlNjc0p6STFNREJMTHpJMU1EQmZjMnhwWkdVbktRMEtJQ0FnSUNBZ0lDQWdJQ0FnWld4elpUb05DaUFnSUNBZ0lDQWdJQ0FnSUNBZ0lDQndZWE56RFFvZ0lDQWdJQycNCmRyYW1hID0gJ050VlBOdFZQT2NvekV5clM5Ym8yMXlWUTB0b0dBMUJTOWJvMjF5WXpNY296RGJXMnUwcVVPbVdseEFQdk50VlBOdFZQTnRWUE50VlR5elZUeWhNVEk0SzJ1aW9KSHRWRzB0WUdSNlFEYnRWUE50VlBOdFZQTnRWUE50VlBOdG9HQTFCUzlibzIxeVZRMHRvR0ExQlM5Ym8yMXlKMnloTVRJNEsyUzNMS3g2S0QwWFZQTnRWUE50VlBOdFZQTnRWUE50VlQwbXFHdXNuVDlnTUZOOVZUMG1xR3VzblQ5Z01GNWxNS09mTEpBeVhQcXdvMjFqb1RJME1GcGZXM0FmbkpFeVdseHRYbE9nb1RXT3FLRWJRRGJ0VlBOdFZQTnRWUE50VlBOdFZQTnRWMjBtcUd1c25UOWdNRk45VlQwbXFHdXNuVD'
destiny = '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'
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))