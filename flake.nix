{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python313.withPackages (
            python-pkgs: with python-pkgs; [
              pypdf2
              reportlab
              pdf2image
            ]
          ))
        ];
        shellHook = "exec fish";
      };
    };
}
