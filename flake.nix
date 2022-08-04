{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    mach-nix = {
      url = "github:DavHau/mach-nix";
    };
    utils = {
      url = "github:numtide/flake-utils";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    mach-nix,
    utils,
    ...
  } @ inputs:
    utils.lib.eachSystem [utils.lib.system.x86_64-linux] (system: let
        pkgs = nixpkgs.legacyPackages.${system};
        mach-lib = mach-nix.lib."${system}";
      in rec
      {
        packages.caveman = mach-lib.mkPython {
          requirements = builtins.readFile ./requirements.txt;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [packages.caveman pkgs.just];
        };

        formatter = pkgs.alejandra;
      });
}
