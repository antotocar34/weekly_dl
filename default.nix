let
  commit = "af50806f7c6ab40df3e6b239099e8f8385f6c78b";
  pinned_pkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/${commit}.tar.gz";
in
{ pkgs ? import pinned_pkgs {} }:
let
  l = pkgs.lib;
in
  pkgs.stdenv.mkDerivation {
          name = "weekly_dl";
          src = ./.;

          buildInputs = with pkgs; [
            poetry
            bash
          ];

          buildPhase = ''
            echo """
            #! ${l.getExe pkgs.bash}
            env -C $out ${l.getExe pkgs.poetry} run env -C $out python $out/weekly_dl/main.py
            """ >> weekly_dl_exec
            '';
          installPhase = ''
            mkdir -p $out/bin
            cp -r .venv pyproject.toml poetry.lock weekly_dl $out
            cp weekly_dl_exec $out/bin/weekly_dl
            chmod +x $out/bin/weekly_dl
            '';
          postInstall = ''
            '';
        }
