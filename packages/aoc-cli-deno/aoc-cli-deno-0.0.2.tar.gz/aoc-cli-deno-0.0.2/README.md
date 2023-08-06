# aoc-cli-deno

A plugin for the opinionated scaffolder for Advent of Code that generates scaffolds to write solutions in javascript and execute with Deno.

# Installation

`pip install aoc-cli` to get the `aoc-cli` tool
`pip install aoc-cli-deno` to get the deno plugin.

# Usage

Scaffold a project with
`aoc init --language deno --year <current year if december, else previous year> --location .`

All other subcommands are directory aware:

\*Note: plugins (specified with the --language flag) may alter the functionality below but in general...

`aoc get` downloads the input for the day
`aoc run <part>` executes the function specified in <part> (1 or 2) file for the day
`aoc submit <part>` executes the function specified in <part> (1 or 2) file for the day, then submits the answer to the form
`aoc open` opens the current day in the browser
