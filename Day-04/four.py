class Passport:

    def __init__(self, dict, line_num) -> None:
        self.byr = False
        self.iyr = False
        self.eyr = False
        self.hgt = False
        self.hcl = False
        self.ecl = False
        self.pid = False
        self.cid = False

        self.line = line_num

        for key, value in dict.items():
            setattr(self, key, value)

    def check_valid(self) -> bool:
        if all([
            self.byr,
            self.iyr,
            self.eyr,
            self.hgt,
            self.hcl,
            self.ecl,
            self.pid]): 
            return True
        else:
        #     print('I am from ' + str(self.line) + ' and missing: ')
        #     for attr in ['byr', 'iyr', 'eyr', 'hgt', 'ecl', 'pid', 'cid']:
        #         if not getattr(self, attr):
        #             print(attr)
            return False

passports = []
curr_passport = {}

with open('input.txt', 'r') as f:
    i = 0
    for line in f:
        i += 1

        # Add keys to current passport, or add our current
        # passport to the list and start a new one.
        if line != '\n':
            for x in line.rstrip().split(' '):
                key, value = x.split(':')
                curr_passport[key] = value
            
        else:
            passports.append(Passport(curr_passport, i))
            curr_passport = {}
    passports.append(Passport(curr_passport, i + 1))

valid = 0
for passport in passports:
    if passport.check_valid():
        valid += 1
    else:
        print(passport.line)

for passport in passports:
    if passport.line == 359:
        print(passport.hcl)
print(valid)
