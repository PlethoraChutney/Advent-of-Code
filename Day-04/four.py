import re

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

    def valid_part_one(self) -> bool:
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
            return False

    def valid_part_two(self) -> bool:        
        try:
            assert self.valid_part_one()
            assert 1920 <= int(self.byr) <= 2002
            assert 2010 <= int(self.iyr) <= 2020
            assert 2020 <= int(self.eyr) <= 2030
            
            if 'cm' in self.hgt:
                assert 150 <= int(self.hgt.replace('cm', '')) <= 193
            elif 'in' in self.hgt:
                assert 59 <= int(self.hgt.replace('in', '')) <= 76
            else:
                return False

            assert re.match('^#[0-9,a-f,A-F]{6}$', self.hcl)

            assert self.ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
            assert re.match('^[0-9]{9}$', self.pid)
            
        except AssertionError:
            return False

        return True



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

old_valid = 0
new_valid = 0
for passport in passports:
    if passport.valid_part_one():
        old_valid += 1

    if passport.valid_part_two():
        new_valid += 1
        print(passport.byr + ' ' + passport.iyr + ' ' + passport.eyr)
        print(passport.hgt + ' ' + passport.hcl + ' ' + passport.ecl + ' ' + passport.pid)

print(old_valid)
print(new_valid)
