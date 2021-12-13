package main

import (
	"fmt"
	"os"
	"strconv"
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
	depths := convert_to_ints(puzzle_input)

	fmt.Println(part_one(depths))
	fmt.Println(part_two(depths))

}

func part_one(depths []int) int {
	count := 0

	for i := 1; i < len(depths); i++ {
		if depths[i] > depths[i-1] {
			count += 1
		}
	}

	return count
}

func part_two(depths []int) int {
	count := 0

	for i := 0; i < len(depths)-3; i++ {
		if depths[i] < depths[i+3] {
			count += 1
		}
	}

	return count
}

func convert_to_ints(puzzle_input []string) []int {

	var depths []int

	for i := 0; i < len(puzzle_input); i++ {
		if puzzle_input[i] != "" {
			dep, e := strconv.Atoi(puzzle_input[i])
			check(e)

			depths = append(depths, dep)
		}
	}

	return depths
}
