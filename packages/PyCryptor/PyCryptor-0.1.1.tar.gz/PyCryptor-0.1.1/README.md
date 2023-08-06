# PyCrypytor

PyCryptor is a cli tool used for encrypting/decrypting files. The tool uses EAX signature verification and CBC cipher. The password provided by the user is used as a 256-bit symmetric key after getting hashed 100 000 times.

## Installation
```
$ pip install PyCryptor
```

## Usage

- :lock: Encrypting files
```
$ pycryptor -e -k 12345 test_files/*
 ╔═════════════════════════════════════════════════════════╗
 ║      ____        ______                 __              ║
 ║     / __ \__  __/ ____/______  ______  / /_____  _____  ║
 ║    / /_/ / / / / /   / ___/ / / / __ \/ __/ __ \/ ___/  ║
 ║   / ____/ /_/ / /___/ /  / /_/ / /_/ / /_/ /_/ / /      ║
 ║  /_/    \__, /\____/_/   \__, / .___/\__/\____/_/       ║
 ║        /____/           /____/_/                        ║
 ║                                                         ║
 ╚═════════════════════════════════════════════════════════╝

 operation mode : encrypt
 total files    : 3 files
 buffer size    : 4096

 file_1.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
 file_2.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
 file_3.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```

- :unlock: Encrypting files
```
$ pycryptor -d -k 12345 test_files/*
 ╔═════════════════════════════════════════════════════════╗
 ║      ____        ______                 __              ║
 ║     / __ \__  __/ ____/______  ______  / /_____  _____  ║
 ║    / /_/ / / / / /   / ___/ / / / __ \/ __/ __ \/ ___/  ║
 ║   / ____/ /_/ / /___/ /  / /_/ / /_/ / /_/ /_/ / /      ║
 ║  /_/    \__, /\____/_/   \__, / .___/\__/\____/_/       ║
 ║        /____/           /____/_/                        ║
 ║                                                         ║
 ╚═════════════════════════════════════════════════════════╝

 operation mode : decrypt
 total files    : 3 files
 buffer size    : 4096

 file_1.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
 file_2.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
 file_3.txt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```