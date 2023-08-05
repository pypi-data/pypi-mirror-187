# `cpr-generator` - An Unofficial library and tool for generating and verifying Danish CPR-numbers.

This project contains a library and some CLI-tools for generating, manipulating and verifying Danish CPR-numbers,
called "personnummer" or "CPR-nummer" in Danish, as defined by the Danish authority ["Det
Centrale Personregister"](https://cpr.dk/cpr-systemet/opbygning-af-cpr-nummeret).

## Disclaimer

This is a community project that is NOT indorsed by the Danish authorities and should
not be used as a reference.

## Getting Started

This is available on PyPI via. `pip` which includes both the library and the CLI-tools.
Simply install with the command:

```sh
pip install -U cpr-generator
```

### Using the Library

The library contains a few different modules. Most important are the `cpr_verifier` and the
`generator` modules.

The `cpr_verifier` contains three functions:

- `is_leap_year`: takes a year (`int`) checks whether the year is a leap year.
- `is_cpr_number`: takes a potential CPR-number (`str`) and checks that it fulfills
the format: `DDMMYY(-)NNNN`.
- `satisfies_mod11` takes a potential CPR-number (`str`), checks that it fulfills both
the format: `DDMMYY(-)NNNN` and the Modulus-11 control condition.

### Using the CLI-tools

#### `cpr-gen`

This is a simple CLI tool that can generate random CPR-numbers, with or without hyphens.

Example usage:

```sh
cpr-gen -n 1000 -m False --hyphen True
```

The above generates a thousand CPR-numbers with hyphens, not satisfying the Modulus-11
control condition.

#### `cpr-server`

This CLI-tools starts a HTTP server (using `flask`) on port 5000 that can generate random
CPR-numbers on demand.

Simply run:

```sh
cpr-server
```

And the server should be available at `localhost:5000`.

The server has the following available URL endpoints:

- `/`: Returns a random CPR-number (no hyphen)
- `/no-mod11/`: Returns a random CPR-number (no hyphen), not satisfying Modulus-11.
- `/hyphen/`: Returns a random CPR-number (with hyphen)
- `/no-mod11/hyphen/`: Returns a random CPR-number (with hyphen), not satisfying Modulus-11.
- `/<int:number>/`: Returns `number` random CPR-numbers (no hyphen)
- `/no-mod11/<int:number>/`: Returns `number` random CPR-numbers (no hyphens), not satisfying Modulus-11.
- `/hyphen/<int:number>/`: Returns `number` random CPR-numbers (with hyphens)
- `/no-mod11/hyphen/<int:number>/`: Returns `number` random CPR-numbers (with hyphens), not satisfying Modulus-11.

#### `cpr-verify`

This CLI-tool can be used to check the input fulfills the format of a CPR-number, with or
without hyphen, and whether or not the input satisfies the Modulus-11 control condition.

Example usage:

```sh
cpr-verify 111111-1118  # --> True
```

The above verifies that the input `111111-1118` fulfills the CPR-number format.
