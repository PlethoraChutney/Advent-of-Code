from itertools import combinations

class Cipher():
    
    def __init__(self, cipher) -> None:
        self.cipher = cipher
        self.invalid = None
        self.weakness = None

    def check_valid(self, index) -> bool:
        if index <= 25:
            return True

        components = self.cipher[index-25:index]
        test = self.cipher[index]

        if test in [sum(x) for x in combinations(components, 2)]:
            return True
        else:
            return False

    def find_invalid(self) -> None:
        self.invalid = [self.cipher[i] for i in range(len(self.cipher)) if not self.check_valid(i)]
        self.invalid = self.invalid[0]

    def find_weakness(self) -> None:
        if not self.invalid:
            self.find_invalid()
        
        for i in range(len(self.cipher)):
            contig_sum = self.cipher[i]
            j = i
            while contig_sum < self.invalid and not self.weakness:
                j += 1
                
                contig_sum += self.cipher[j]
                if contig_sum == self.invalid:
                    self.weakness = min(self.cipher[i:j+1]) + max(self.cipher[i:j+1])

                

cipher = Cipher([int(x.rstrip()) for x in open('input.txt')])
cipher.find_weakness()
print(cipher.invalid)
print(cipher.weakness)