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
		// ASCII 1 is '49', ASCII 0 is '48'
		converted = converted << 1
		if rune_list[i] == '1' {
			converted += 1
		}
	}

	return converted
}

// these are all twelve bit numbers
const len_bits int = 12

func part_one(diags []int) int {
	var bitlist [len_bits]int

	for i := 0; i < len_bits; i++ {
		bitlist[i] = balance_bits(diags, len_bits-(i+1))
	}

	fmt.Println(bitlist)
	var gamma int
	var epsilon int
	for i := 0; i < len(bitlist); i++ {
		gamma = gamma << 1
		epsilon = epsilon << 1
		// if bitlist[i] is > 0, the most common bit was 1, so gamma
		// should get a 1 bit there. Otherwise, epsilon
		if bitlist[i] > 0 {
			gamma += 1
		} else {
			epsilon += 1
		}
	}

	return gamma * epsilon
}

func part_two(diags []int) int {
	var oxygen, co2 int

	return oxygen * co2
}

func balance_bits(diags []int, position int) int {
	var mcb int
	for i := 0; i < len(diags); i++ {
		if (diags[i]>>position)%2 == 1 {
			mcb += 1
		} else {
			mcb -= 1
		}
	}

	return mcb
}
