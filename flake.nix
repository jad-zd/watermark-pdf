{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };
  outputs =
    { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      buildInputs = with pkgs; [
        (python313.withPackages (
          py-pkgs: with py-pkgs; [
            pypdf2
            reportlab
            pdf2image
          ]
        ))
      ];
    in
    {
      packages.${system}.watermarkPdf = pkgs.stdenv.mkDerivation rec {
        name = "watermark-pdf";
        src = ./script.py;
        propagatedBuildInputs = buildInputs;
        dontUnpack = true; # Prevent unpacking source code
        installPhase = ''
          mkdir -p $out/bin
          cp $src $out/bin/${name}
          chmod +x $out/bin/${name}
        '';
      };

      devShells.${system}.default = pkgs.mkShell {
        inherit buildInputs;
        shellHook = "exec fish";
      };
    };
}
