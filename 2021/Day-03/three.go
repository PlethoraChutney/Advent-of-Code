package main

import (
	"fmt"
	"os"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	data, err := os.ReadFile(os.Args[1])
	check(err)

	puzzle_input := strings.Split(string(data), "\n")

	var diags []int
	for i := 0; i < len(puzzle_input); i++ {
		if puzzle_input[i] != "" {
			diags = append(diags, str_to_bin(puzzle_input[i]))
		}
	}

	fmt.Println(part_one(diags))
	fmt.Println(part_two(diags))
}

func str_to_bin(in_string string) int {
	rune_list := []rune(in_string)
	var converted int

	for i := 0; i < len(rune_list); i++ {
		converted = converted << 1
		if rune_list[i] == '1' {
			converted += 1
		} else if rune_list[i] != '0' {
			converted = converted >> 1
		}
	}

	return converted
}

// these are all twelve bit numbers
const len_bits int = 12

func part_one(diags []int) int {
	var bitlist [len_bits]int

	for i := 0; i < len_bits; i++ {
		bitlist[i] = balance_bits(diags, len_bits-(i+1), 1, 0)
	}

	var gamma int
	var epsilon int
	for i := 0; i < len(bitlist); i++ {
		gamma = gamma << 1
		epsilon = epsilon << 1
		// if bitlist[i] is > 0, the most common bit was 1, so gamma
		// should get a 1 bit there. Otherwise, epsilon gets a bump
		//
		// bits which are all zero should be ignored, or else epsilon
		// gets very big
		if bitlist[i] == -len(diags) {
			continue
		}

		if bitlist[i] > 0 {
			gamma += 1
		} else {
			epsilon += 1
		}
	}

	return gamma * epsilon
}

func part_two(diags []int) int {
	oxygen := oxygen_rating(diags)
	co2 := co2_rating(diags)
	fmt.Println("")

	fmt.Println(oxygen, co2)

	return oxygen * co2
}

func oxygen_rating(diags []int) int {
	for i := 0; i < len_bits+1; i++ {
		var sum int
		if len(diags) == 1 {
			break
		}
		for j := 0; j < len(diags); j++ {
			sum += diags[j] >> (len_bits - i) & 1
		}

		if sum == 0 {
			continue
		}
		proportion_one := float32(sum) / float32(len(diags))
		var new_mask_bit int
		if proportion_one >= 0.5 {
			new_mask_bit = 1
		} else {
			new_mask_bit = 0
		}
		var new_diags []int
		for len(diags) > 0 {
			var d int
			d, diags = diags[0], diags[1:]
			if d>>(len_bits-i)&1 == new_mask_bit {
				new_diags = append(new_diags, d)
			}
		}
		diags = new_diags
	}

	return diags[0]
}

func co2_rating(diags []int) int {

	for i := 0; i < len_bits+1; i++ {
		var sum int
		if len(diags) == 1 {
			break
		}
		for j := 0; j < len(diags); j++ {
			sum += diags[j] >> (len_bits - i) & 1
		}

		if sum == 0 {
			continue
		}
		proportion_one := float32(sum) / float32(len(diags))
		var new_mask_bit int
		if proportion_one < 0.5 {
			new_mask_bit = 1
		} else {
			new_mask_bit = 0
		}
		var new_diags []int
		for len(diags) > 0 {
			var d int
			d, diags = diags[0], diags[1:]
			if d>>(len_bits-i)&1 == new_mask_bit {
				new_diags = append(new_diags, d)
			}
		}
		diags = new_diags
	}

	return diags[0]
}

func balance_bits(diags []int, position int, part int, filter int) int {
	var mcb int

	filter = filter >> (position + 1)
	for i := 0; i < len(diags); i++ {
		if part == 2 {
			if diags[i]>>(position+1)^filter != filter {
				continue
			}
		}
		if (diags[i]>>position)%2 == 1 {
			mcb += 1
		} else {
			mcb -= 1
		}
	}

	return mcb
}
