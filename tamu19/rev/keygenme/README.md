# KeyGenMe

Flow of the program:
1. checks 0x9 < len(input) < 0x64
2. compare enc(input) to "[OIonU2_<__nK<KsK"

No clue what enc() actually does, so I just mimic it in python. It's pretty messy (shown in the file).

Some important things that ARE clear:
1. enc() generates an encrypted string based off of each individual character of the original. This means we can probably brute-force it; it's at most 256*64=163834 tries.
2. Each character of the encrypted input is based off of the previous, and the first character is based off of "H"
