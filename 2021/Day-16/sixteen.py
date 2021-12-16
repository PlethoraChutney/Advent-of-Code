from queue import LifoQueue

class PacketParser:

    def __init__(self, input_packet, subpacket = False):
        input_packet = int(input_packet, 16)

        self.signal = LifoQueue()
        self.versions = []
        self.processed = []

        # subtract two for "0b"
        bitlen = len(bin(input_packet)) - 2
        if bitlen % 4 and not subpacket:
            pad_to_four = 4 - bitlen % 4
        else:
            pad_to_four = 0

        while input_packet > 0:
            self.signal.put(input_packet & 1)
            input_packet = input_packet >> 1

        for _ in range(pad_to_four):
            self.signal.put(0)

        # remove the leading 1 from our subpacket implementation
        if subpacket:
            self.signal.get()

    def __repr__(self) -> str:
        signal = self.signal.queue[::-1]

        return ''.join([str(x) for x in signal])

    @property
    def empty(self):
        return self.signal.empty()

    def read_packet(self):
        version = 0
        for _ in range(3):
            version = version << 1 | self.signal.get(False)
        self.versions.append(version)

        type = 0
        for _ in range(3):
            type = type << 1 | self.signal.get(False)

        if type == 4:
            self.processed.append(self.read_literal())
        else:
            versions, processed = self.read_op()
            self.versions.extend(versions)
            self.processed.extend(processed)

    def read_literal(self):
        literal = 0
        # read the first bit, loop if it's a 1
        while self.signal.get(False):
            for _ in range(4):
                literal = literal << 1 | self.signal.get(False)
        
        # last group of bits starts with a zero, so read once
        # more after the loop breaks
        for _ in range(4):
            literal = literal << 1 | self.signal.get(False)

        return literal

    def read_op(self):
        len_type = self.signal.get(False)
        if not len_type:
            len_subpackets = 0
            for _ in range(15):
                len_subpackets = len_subpackets << 1 | self.signal.get(False)


            # a bitstream should always start with a 1 so that you're not having
            # to do this padding bullshit. So we can add that for the subpackets.
            subpacket = 1
            for _ in range(len_subpackets):
                subpacket = subpacket << 1 | self.signal.get(False)
            subpacket_parser = PacketParser(hex(subpacket), subpacket = True)
            while not subpacket_parser.empty:
                subpacket_parser.read_packet()
            return subpacket_parser.versions, subpacket_parser.processed
            

        else:
            num_subpackets = 0
            for _ in range(11):
                num_subpackets = num_subpackets << 1 | self.signal.get(False)
            # give the full queue, because we don't know the number of bits, just
            # the number of packets
            subpacket = 1
            for bit in self.signal.queue[::-1]:
                subpacket = subpacket << 1 | bit
            subpacket_parser = PacketParser(hex(subpacket), subpacket = True)

            for _ in range(num_subpackets):
                subpacket_parser.read_packet()

            # drop bits from our queue until we've dropped the number that the
            # subpacket parser used.
            while len(self.signal.queue) > len(subpacket_parser.signal.queue):
                self.signal.get()

            return subpacket_parser.versions, subpacket_parser.processed

# literal:
# test_packet = 'D2FE28'
#
# operator:
# test_packet = '38006F45291200'
# test_packet = 'EE00D40C823060'
#
# other tests:
# test_packet = '8A004A801A8002F478'
# test_packet = '620080001611562C8802118E34'
# test_packet = 'C0015000016115A2E0802F182340'
# test_packet = 'A0016C880162017C3686B18A3D4780'
#
# parser = PacketParser(test_packet)

with open('input.txt', 'r') as f:
    parser = PacketParser(f.readline().rstrip())

parser.read_packet()
print(sum(parser.versions))