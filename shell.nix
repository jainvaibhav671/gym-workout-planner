# shell.nix

{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Define the Python environment
  buildInputs = [
    pkgs.python312  # or another version like python3.8, python3.10, etc.
    pkgs.python312Packages.pip  # Install pip for additional dependencies
    pkgs.poetry

    pkgs.gcc
    pkgs.stdenv.cc.cc.lib
  ];

  # Set LD_LIBRARY_PATH to include GCC's libstdc++ location
  shellHook = ''
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH"

    # poetry shell
    source "$(poetry env info -p)/bin/activate"
  '';

  # Additional configurations (if any)
  # nativeBuildInputs = [  ];
}
