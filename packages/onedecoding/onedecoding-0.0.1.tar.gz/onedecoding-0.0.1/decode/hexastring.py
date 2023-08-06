from struct import unpack
from binascii import unhexlify


class Hexastring(str):
    """
    Custom string-like class that implements conversion from hexadecimal.
    """
    def to_decimal(self, dtype, digits: int = 1) -> float:
        """
        :param dtype: 'f' --> float, 'uint' --> integer
        :param digits: number of decimal digits to use (1 for spl data, more for GPS)
        """
        encoded_byte = unhexlify(self)

        if dtype == "float":
            encoded_byte = unhexlify(self.reverse_by())
            output = round(unpack('>f', encoded_byte)[0], digits)
        elif "uint" in dtype:
            output = int.from_bytes(encoded_byte, byteorder='little')
        else:
            output = None

        return output

    def split_by(self, by=8) -> list:
        """
            Takes string "inp" and returns a list of strings of "by" characters.
            :arg inp_str: string type input
            :arg by: length of the elements of the list
        """
        n = len(self)
        if isinstance(by, list):
            slices = [
                Hexastring(self[
                           sum(by[:k+1]): sum(by[:k+1]) + by[k+1]
                           ]) for k in range(len(by)-1)
            ]
        else:
            slices = [Hexastring(self[by * k: by * (k + 1)]) for k in range(n // by)]

        return slices

    def reverse_by(self, by: int = 2) -> str:
        """
        Takes string "inp" and returns the reversed version by groups of "by"
        Example: reverse_by('ABCDEFGH') = 'GHEFCDAB'
        :arg inp_str: string type input
        :arg by: length to group to reverse
        """
        n = len(self)
        slices = [self[by * k:by * (k + 1)] for k in range(n // by)]
        rev = Hexastring("".join(slices[::-1]))
        return rev
