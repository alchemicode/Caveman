# Run normally using current Python environment
run:
    ./src/main.py

# Run using the env defined in `flake.nix`
nix:
    nix run
