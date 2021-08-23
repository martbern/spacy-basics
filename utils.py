def file_generator(dir: str) -> Generator[str, None, None]:
    for filename in os.listdir(dir):
        if "danavis" in filename:
            filepath = os.path.join(dir, filename)

            with open(filepath, "r") as f:
                yield f.read()