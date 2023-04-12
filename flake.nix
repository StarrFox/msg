{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    naersk.url = "github:nix-community/naersk";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = {self, flake-utils, naersk, nixpkgs}:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = (import nixpkgs) {
          inherit system;
        };

        naersk' = pkgs.callPackage naersk {};
        project_cargo = builtins.fromTOML (builtins.readFile ./Cargo.toml);

      in rec {
        defaultPackage = naersk'.buildPackage {
          name = "msg";
          src = ./.;
          # extra built inputs here
          buildInputs = with pkgs; [];
          version = project_cargo.package.version;
        };

        devShell = pkgs.mkShell {
          nativeBuildInputs = with pkgs; [rustc cargo];
        };
      }
    );
}