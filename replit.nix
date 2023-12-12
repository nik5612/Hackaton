{ pkgs }: {
  deps = [
    pkgs.libev
    pkgs.sqlite-interactive.bin
    pkgs.mailutils
  ];
  env = {
    PYTHON_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.libev
    ];
  };
}