This package allows you do call a function and immediately pickle its output to a passed filepath.

If the output has already been saved to the filepath, it will instead be loaded from there (unless easy_override=True, in which case the callback is guaranteed to be called and the original file will be overwritten, if it exists)