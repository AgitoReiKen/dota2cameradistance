import os
import io
import re
import struct


def isRegexControlCharacter(ch):
    return (
        ch >= 0x20
        and ch <= 0x2F
        or ch >= 0x3A
        and ch <= 0x40
        or ch >= 0x5B
        and ch <= 0x60
        or ch >= 0x7B
        and ch <= 0x7E
    )


def prepareByteRegexp(exp: str):
    exp = exp.replace("\n", " ")
    words = exp.split(" ")
    result = bytearray()
    for word in words:
        if len(word) == 2:
            x = bytearray.fromhex(word)
            if isRegexControlCharacter(x[0]):
                result.extend(bytearray(b"\\"))
            result.extend(x)
            continue

        result.extend(bytearray(word, "ascii"))

    return bytes(result)


def main():
   
    PATH = "C:/rei/Software/steam/steamapps/common/dota 2 beta/game/dota/bin/win64/client.dll"
    PATTERN_PATH = "./pattern.txt"

    with open(PATTERN_PATH, "r") as patternFile:
        pattern = patternFile.read()
        bytePattern = prepareByteRegexp(pattern)

    with open(PATH, "rb") as file:
        chunk = file.read()
        foundLen = 0
        for it in re.compile(bytePattern).finditer(chunk):
            if foundLen >= 1:
                print("More than 1 target found. Update the pattern")
                exit()
            foundLen += 1
            previousValue = struct.unpack("f", it.group(1))[0]
            valuePattern = it.group(1)
            offsetToValue = it.start()
            fullMatch = it.group(0)
        if foundLen == 0:
            print("No target found. Update the pattern");
            exit();
        
        foundLen = 0
        for it in re.compile(valuePattern).finditer(fullMatch):
            if foundLen >= 1:
                print("More than 1 value target found. Update the logic")
                exit()
            foundLen += 1
            offsetToValue += it.start()
        

        print(f"Previous value: {previousValue}")
        newValue = input("Enter new value: ")
        newValue = float(newValue);
        file.close();
        with open(f"{PATH}", "wb") as new:
            new.write(chunk[:offsetToValue])
            new.write(bytearray(struct.pack("f", newValue)))
            new.write(chunk[offsetToValue+4:]);


if __name__ == "__main__":
    main()
