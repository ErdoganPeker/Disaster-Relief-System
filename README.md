# Disaster Relief System

![C](https://img.shields.io/badge/C-99-A8B9CC?style=flat&logo=c&logoColor=white)
![Data Structures](https://img.shields.io/badge/Data%20Structures-Arrays%20%26%20Files-orange?style=flat)
![Domain](https://img.shields.io/badge/Domain-Crisis%20Management-red?style=flat)

> A C program for managing and searching disaster victim records to enable fast, organized aid delivery during emergencies.

---

## Overview

In disaster scenarios, response teams need rapid access to victim information — name, location, contact details, and aid requests. This system provides a terminal-based interface to register victims, record their needs, search through records, and track the status of aid requests, all stored persistently via file I/O.

## Features

- Register disaster victims with name, surname, phone, and address
- Record and track individual aid requests per victim
- Search victims by name or ID for rapid retrieval
- File-based persistent storage — data survives program restarts
- Handles up to 100 victims and 300 aid requests per session
- Input validation and error handling throughout

## Tech Stack

- **Language:** C (C99 standard)
- **Storage:** File I/O (text-based persistence)
- **Data Structures:** Static arrays with index-based lookup
- **I/O:** Standard terminal input/output

## Project Structure

```
Disaster-Relief-System/
├── main.c          # Full application — victim registration, search, request handling
└── .gitignore
```

## Getting Started

### Prerequisites

- GCC or any C99-compatible compiler

### Build & Run

```bash
git clone https://github.com/ErdoganPeker/Disaster-Relief-System.git
cd Disaster-Relief-System
gcc -std=c99 -o relief main.c
./relief
```

On Windows with MinGW:

```bash
gcc -std=c99 -o relief.exe main.c
relief.exe
```

## Usage

The program presents a menu on startup:

```
1. Register new victim
2. Add aid request
3. Search victim by name
4. List all victims
5. List all requests
0. Exit
```

Data is saved to a file automatically so records persist across sessions.

## Author

**Erdogan Yasin Peker** — Computer Engineer

[GitHub](https://github.com/ErdoganPeker) · [LinkedIn](https://www.linkedin.com/in/erdogan-yasin-peker-b107ba24b/)
