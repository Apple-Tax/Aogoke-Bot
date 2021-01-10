def textPadding(text, length, alignment="left"):
    padLength = length - len(text)
    if padLength <= 0:
        return text
    if alignment.lower() == "left":
        return text + (" " * padLength)
    else:
        return (" " * padLength) + text
