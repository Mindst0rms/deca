from deca.file import ArchiveFile


class EntrySarc:
    def __init__(self, index=None, v_path=None):
        self.index = index
        self.v_path = v_path
        self.string_offset = None
        self.offset = None
        self.length = None
        self.shash = None
        self.u32_4 = None

    def deserialize(self, f):
        self.string_offset = f.read_u32()
        self.offset = f.read_u32()
        self.length = f.read_u32()
        self.shash = f.read_u32()
        self.u32_4 = f.read_u32()

    def dump_str(self):
        return 'o:{} s:{} h:{:08X} vp:{}'.format(self.offset, self.length, self.shash, self.v_path.decode('utf-8'))


class FileSarc:
    def __init__(self):
        self.version = None
        self.magic = None
        self.ver2 = None
        self.dir_block_len = None
        self.strings0 = None
        self.strings = None
        self.entries = None

    def deserialize(self, fin):
        with ArchiveFile(fin) as f:
            self.version = f.read_u32()
            self.magic = f.read(4)
            self.ver2 = f.read_u32()
            self.dir_block_len = f.read_u32()

            string_len = f.read_u32()
            self.strings0 = f.read(string_len)
            self.strings = self.strings0.split(b'\00')
            if len(self.strings[-1]) == 0:
                self.strings = self.strings[:-1]

            self.entries = [EntrySarc(v_path=self.strings[i], index=i) for i in range(len(self.strings))]
            for ent in self.entries:
                ent.deserialize(f)

    def dump_str(self):
        sbuf = ''
        for ent in self.entries:
            sbuf = sbuf + ent.dump_str() + '\n'
        return sbuf