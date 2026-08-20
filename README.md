# ISI–DRDO Project

### Quantum Cryptanalysis of Polyalphabetic Cipher Cryptographic Schemes

> **Research & Development Project in Cryptography and Quantum Cryptanalysis**

This repository contains the implementation and experimental framework developed as part of research on **quantum cryptanalysis of classical and post-quantum cryptographic schemes**, with a particular focus on the analysis of classical substitution and polyalphabetic ciphers and the integration of **quantum-inspired / quantum algorithmic techniques** into cryptanalytic workflows.

The current implementation provides a web-based cryptographic laboratory supporting **Vigenère Cipher**, **Hill Cipher**, classical cryptanalysis, brute-force key search, periodicity analysis, and a hybrid **quantum–classical Vigenère cryptanalysis pipeline**.

---

## Table of Contents

* [Overview](#overview)
* [Objectives](#objectives)
* [Key Features](#key-features)
* [System Architecture](#system-architecture)
* [Cryptographic Modules](#cryptographic-modules)
* [Quantum–Classical Cryptanalysis Pipeline](#quantumclassical-cryptanalysis-pipeline)
* [Repository Structure](#repository-structure)
* [Technology Stack](#technology-stack)
* [Installation](#installation)
* [Running the Application](#running-the-application)
* [Using the Cryptographic Modules](#using-the-cryptographic-modules)
* [Research Methodology](#research-methodology)
* [Security and Research Disclaimer](#security-and-research-disclaimer)
* [Future Work](#future-work)
* [Acknowledgements](#acknowledgements)
* [License](#license)

---

## Overview

Classical cryptographic schemes provide an important foundation for understanding modern cryptanalysis. Although algorithms such as the **Vigenère Cipher** and **Hill Cipher** are not considered secure for contemporary applications, they provide useful mathematical structures for studying:

* cryptanalysis,
* key recovery,
* frequency analysis,
* periodicity,
* brute-force search,
* collision search,
* quantum search techniques, and
* hybrid quantum–classical cryptanalytic architectures.

This repository brings these concepts together into an experimental framework.

The project combines conventional cryptanalysis with simulated quantum procedures to investigate how quantum algorithms can potentially be incorporated into cryptanalytic workflows.

---

## Objectives

The primary objectives of the project are:

1. Implement classical encryption and decryption algorithms.
2. Develop automated cryptanalysis techniques for classical ciphers.
3. Study key-length detection and periodicity in Vigenère ciphertexts.
4. Investigate brute-force key-search approaches.
5. Explore quantum search techniques in cryptanalytic problems.
6. Develop a hybrid quantum–classical cryptanalysis pipeline.
7. Provide a web-based interface for experimentation.
8. Establish a foundation for further research into quantum cryptanalysis.

---

## Key Features

### Classical Cryptography

* Vigenère encryption
* Vigenère decryption
* Vigenère cryptanalysis
* Hill Cipher encryption
* Hill Cipher decryption
* Hill Cipher known-plaintext/key-recovery approaches

### Classical Cryptanalysis

* Kasiski examination
* Repeated-substring analysis
* GCD-based key-period detection
* Frequency analysis
* Coset analysis
* Key recovery using English-language frequency distributions
* Brute-force search

### Quantum / Quantum-Inspired Components

* BHT-style collision search simulation
* Quantum Swap Test simulation
* Quantum similarity estimation
* Hybrid quantum–classical cryptanalysis
* Quantum-assisted periodicity/collision analysis

### Web Application

The project includes a Flask-based web application that exposes the cryptographic functionality through a browser interface.

The Flask application integrates the Vigenère and Hill Cipher modules together with cryptanalysis and brute-force components.

---

# System Architecture

The overall architecture can be represented as:

```text
                         ┌──────────────────────┐
                         │     Web Interface    │
                         │   Flask Application  │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
        │ Vigenère       │  │ Hill Cipher    │  │ Cryptanalysis  │
        │ Module         │  │ Module         │  │ Module         │
        └───────┬────────┘  └───────┬────────┘  └───────┬────────┘
                │                   │                   │
                ▼                   ▼                   ▼
        ┌────────────────┐  ┌────────────────┐  ┌────────────────┐
        │ Encryption /   │  │ Matrix-based   │  │ Key Length /   │
        │ Decryption     │  │ Encryption     │  │ Frequency      │
        └────────────────┘  └────────────────┘  └───────┬────────┘
                                                         │
                                                         ▼
                                              ┌────────────────────┐
                                              │ Quantum-Classical  │
                                              │ Cryptanalysis      │
                                              └─────────┬──────────┘
                                                        │
                                      ┌─────────────────┼─────────────────┐
                                      │                 │                 │
                                      ▼                 ▼                 ▼
                                BHT Search         Swap Test       Key Recovery
                                      │                 │                 │
                                      └─────────────────┼─────────────────┘
                                                        ▼
                                                  Final Key
```

---

# Cryptographic Modules

## 1. Vigenère Cipher

The repository implements the complete Vigenère workflow:

```text
Plaintext
    │
    ▼
Vigenère Encryption
    │
    ▼
Ciphertext
    │
    ▼
Cryptanalysis
    │
    ▼
Recovered Key
    │
    ▼
Decryption
    │
    ▼
Recovered Plaintext
```

The implementation includes separate modules for encryption, decryption, and cryptanalysis.

### Files

```text
vigenere_enc.py
vigenere_dec.py
vigenere_crypt.py
vigenere_bruteforce.py
```

---

## 2. Hill Cipher

The project also implements the Hill Cipher using matrix-based transformations.

### Files

```text
hill_enc.py
hill_dec.py
hill_crypt.py
hill_bruteforce.py
```

The encryption/decryption modules perform the matrix transformations required by the Hill Cipher, while the cryptanalysis components investigate key recovery and brute-force approaches.

---

# Quantum–Classical Cryptanalysis Pipeline

One of the primary research components of this repository is the **hybrid quantum–classical cryptanalysis pipeline**.

The pipeline implemented in `quantumpipeline.py` combines several stages:

```text
                 Vigenère Ciphertext
                         │
                         ▼
              ┌─────────────────────┐
              │  Phase 1             │
              │  BHT Collision      │
              │  Search Simulation   │
              └──────────┬──────────┘
                         │
                         ▼
              Repeated Substring
                         │
                         ▼
              ┌─────────────────────┐
              │  Phase 2             │
              │  GCD Periodicity    │
              │  / Key Length       │
              └──────────┬──────────┘
                         │
                         ▼
                  Estimated Key
                      Length
                         │
                         ▼
              ┌─────────────────────┐
              │  Phase 3             │
              │  Quantum Swap Test  │
              │  Verification       │
              └──────────┬──────────┘
                         │
                         ▼
                  Similarity Score
                         │
                         ▼
              ┌─────────────────────┐
              │  Phase 4             │
              │  Classical Frequency│
              │  Based Key Recovery │
              └──────────┬──────────┘
                         │
                         ▼
                    Recovered Key
```

The implementation explicitly describes the pipeline as a sequence of **BHT search → GCD periodicity → Swap Test verification → classical key recovery**.

---

## Phase 1 — BHT Collision Search

The first stage searches for repeated structures within the ciphertext.

The BHT component is used to simulate a collision-search procedure and identify repeated substrings together with their positions.

```python
bht_results = run_bht_simulation(ciphertext)
```

The resulting collision information is passed to the next stage of the pipeline.

---

## Phase 2 — Key-Length Detection

Repeated substring positions can provide information about the periodic structure of the Vigenère key.

The project calculates the GCD of relevant positional differences to estimate the key length:

```python
gcd_results = calculate_key_length(indices)
estimated_key_length = gcd_results['gcd']
```

This produces an estimated period that is subsequently used to divide the ciphertext into cosets.

---

## Phase 3 — Quantum Swap Test

The estimated key length is used to generate a ciphertext coset.

The project compares the frequency distribution of the coset against an expected English-language distribution and passes the resulting probability distributions into a Swap Test simulation.

```text
Expected English Distribution
             │
             │
             ▼
        ┌───────────┐
        │ Swap Test  │
        └─────┬─────┘
              │
              ▼
       Similarity Score
```

The pipeline reports a quantum similarity score for this comparison.

---

## Phase 4 — Classical Key Recovery

After determining the probable key length, the project performs classical frequency-based key recovery.

For every coset, all 26 possible shifts are evaluated against standard English letter frequencies.

The shift producing the strongest correlation is selected as the corresponding key character.

This produces the final recovered Vigenère key.

---

# Repository Structure

```text
ISI-DRDO-PROJECT/
│
├── app.py
│
├── templates/
│   └── Web interface templates
│
├── static/
│   └── Static web assets
│
├── vigenere_enc.py
├── vigenere_dec.py
├── vigenere_crypt.py
├── vigenere_bruteforce.py
│
├── hill_enc.py
├── hill_dec.py
├── hill_crypt.py
├── hill_bruteforce.py
│
├── repsubsearch.py
├── periodkeylendetect.py
├── swaptest.py
├── quantumpipeline.py
│
├── ciphered_output.txt
├── hill_ciphered_output.txt
│
├── INSTRUCTIONS.txt
└── README.md
```

The current repository contains separate implementations for the Vigenère and Hill cipher workflows, supporting cryptanalysis modules, quantum-related components, and a Flask application.

---

# Technology Stack

| Component               | Technology                                   |
| ----------------------- | -------------------------------------------- |
| Programming Language    | Python                                       |
| Web Framework           | Flask                                        |
| Classical Cryptography  | Vigenère, Hill Cipher                        |
| Cryptanalysis           | Kasiski, frequency analysis, GCD periodicity |
| Quantum Simulation      | Python-based simulation                      |
| Frontend                | HTML / CSS / JavaScript                      |
| Mathematical Processing | Python numerical / matrix operations         |

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/CodingDecodingGithub/ISI-DRDO-PROJECT.git
cd ISI-DRDO-PROJECT
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install flask
```

If additional dependencies are required by the local implementation, install them according to the imports used by the corresponding module.

---

# Running the Application

The main web application is implemented in `app.py` using Flask.

Run:

```bash
python app.py
```

The Flask development server should then be accessible through the local address displayed in the terminal.

Open the displayed URL in a browser to access the cryptographic interface.

---

# Using the Cryptographic Modules

The repository can also be used without the web interface.

For example:

```bash
python vigenere_enc.py
```

```bash
python vigenere_dec.py
```

```bash
python vigenere_crypt.py
```

For Hill Cipher:

```bash
python hill_enc.py
```

```bash
python hill_dec.py
```

```bash
python hill_crypt.py
```

The exact input format depends on the individual implementation.

---

# Research Methodology

The project follows a hybrid methodology:

### Classical Layer

Classical algorithms are used for:

* encryption,
* decryption,
* frequency analysis,
* periodicity detection,
* key-length estimation,
* statistical key recovery, and
* brute-force search.

### Quantum Layer

Quantum algorithmic concepts are investigated through simulations of:

* collision search,
* quantum similarity estimation, and
* Swap Test based comparisons.

### Hybrid Layer

The two approaches are combined into a single pipeline:

```text
Classical Cipher
       ↓
Ciphertext Analysis
       ↓
Quantum-Assisted Search
       ↓
Periodicity Estimation
       ↓
Quantum Verification
       ↓
Classical Statistical Recovery
       ↓
Recovered Key
       ↓
Plaintext
```

This hybrid architecture allows the project to study how quantum techniques may complement classical cryptanalytic methods rather than treating quantum computation as an isolated component.

---

# Research Scope

The present repository is primarily an **experimental research implementation**.

The classical cryptographic algorithms are intentionally used as research subjects because their mathematical structure makes them suitable for studying cryptanalysis and quantum algorithmic techniques.

The quantum components currently represent computational simulations and research prototypes. They should therefore not be interpreted as demonstrating a practical quantum attack against real-world cryptographic infrastructure.

---

# Security and Research Disclaimer

This repository is intended for:

* academic research,
* cryptography education,
* algorithmic experimentation,
* quantum computing research, and
* controlled cryptanalysis experiments.

The classical ciphers implemented here are **not suitable for protecting sensitive or real-world communications**.

Furthermore, simulated quantum procedures do not imply that an equivalent attack can currently be executed on a fault-tolerant quantum computer.

---

# Future Work

Potential extensions include:

* [ ] Integration with actual quantum computing frameworks.
* [ ] Execution on available quantum hardware.
* [ ] Improved BHT collision-search implementations.
* [ ] More robust Vigenère key-length estimation.
* [ ] Improved statistical key recovery.
* [ ] Quantum-assisted Hill Cipher cryptanalysis.
* [ ] Grover-based key search experiments.
* [ ] Comparative analysis of classical and quantum search complexity.
* [ ] Automated experimental benchmarking.
* [ ] Support for larger ciphertext datasets.
* [ ] Improved visualization of quantum circuits and measurement distributions.
* [ ] Extension of the framework to additional cryptographic schemes.

---

# Project Status

**Status:** Active Research / Experimental Prototype

The repository is being developed as a research-oriented platform for investigating cryptanalysis techniques and quantum computational approaches.

---

# Acknowledgements

This work is associated with research activities involving:

* **Indian Statistical Institute (ISI), Kolkata**
* **Defence Research and Development Organisation (DRDO)**

The repository is intended to document the computational and experimental components of the research work.

---

# Author / Contributors

Developed and maintained by the project contributors under the associated research initiative.

For collaboration, research discussion, or technical questions, please use the repository's GitHub issues/discussions where applicable.

---

# Repository

**GitHub:**
[ISI–DRDO Project Repository](https://github.com/CodingDecodingGithub/ISI-DRDO-PROJECT?utm_source=chatgpt.com)

---

## Disclaimer

The terminology used in this README describes the **research and experimental implementation contained in this repository**. References to quantum cryptanalysis, BHT search, and Swap Test refer to simulated or computational implementations present in the project and should not be interpreted as claims of practical cryptographic compromise.

---

> **Exploring the intersection of classical cryptanalysis, quantum algorithms, and secure computation.**
