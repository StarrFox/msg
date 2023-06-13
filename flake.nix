{
  description = "Open source messaging platform";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-parts.url = "github:hercules-ci/flake-parts/";
    nix-systems.url = "github:nix-systems/default";
  };

  outputs = inputs @ {
    flake-parts,
    nix-systems,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      debug = true;
      systems = import nix-systems;
      perSystem = {
        config,
        self',
        inputs',
        pkgs,
        system,
        ...
      }: {
        packages.default = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          overrides = [
            pkgs.poetry2nix.defaultPoetryOverrides
          ];
        };

        devShells.default = pkgs.mkShell {
          packages = with pkgs; [
            poetry
            commitizen
            just
            alejandra
          ];
        };
      };
    };
}
