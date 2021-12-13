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
	dirs, dists := parse_data(puzzle_input)

	fmt.Println(part_one(dirs, dists))
	fmt.Println(part_two(dirs, dists))
}

func parse_data(data []string) (direction []string, distance []int) {

	for i := 0; i < len(data); i++ {
		if data[i] != "" {
			split := strings.Split(data[i], " ")
			direction = append(direction, string(split[0]))
			dist, _ := strconv.Atoi(split[1])
			distance = append(distance, dist)
		}
	}

	return
}

func part_one(dirs []string, dists []int) int {
	var horiz int
	var depth int
	for i := 0; i < len(dirs); i++ {
		switch dirs[i] {
		case "forward":
			horiz += dists[i]
		case "down":
			depth += dists[i]
		case "up":
			depth -= dists[i]
		}
	}

	return horiz * depth
}

func part_two(dirs []string, dists []int) int {
	var aim int
	var horiz int
	var depth int

	for i := 0; i < len(dirs); i++ {
		switch dirs[i] {
		case "forward":
			horiz += dists[i]
			depth += aim * dists[i]
		case "down":
			aim += dists[i]
		case "up":
			aim -= dists[i]
		}
	}

	return horiz * depth
}
