class SymbolTable:
    _pre_defined_table = {
        "SP": str(bin(0x0000))[2:].zfill(16),
        "LCL": str(bin(0x0001))[2:].zfill(16),
        "ARG": str(bin(0x0002))[2:].zfill(16),
        "THIS": str(bin(0x0003))[2:].zfill(16),
        "THAT": str(bin(0x0004))[2:].zfill(16),
        "SCREEN": str(bin(0x4000))[2:].zfill(16),
        "KBD": str(bin(0x6000))[2:].zfill(16)
    }
    # binary number to string
    for i in range(0, 16):
        _pre_defined_table["R{}".format(str(i))] = str(bin(i))[2:].zfill(16)

    def __init__(self):
        self._table = {**{}, **self._pre_defined_table}
        pass

    def add_entry(self, symbol, address):
        self._table[symbol] = str(bin(address))[2:].zfill(16)

    def contains(self, symbol):
        return symbol in self._table

    def get_address(self, symbol):
        return self._table[symbol]

    def table(self):
        return self._table
