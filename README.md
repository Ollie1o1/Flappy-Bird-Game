# Flappy Bird AI Game

A Python-based clone of Flappy Bird with built-in AI training using NEAT (NeuroEvolution of Augmenting Topologies). This repository contains both a manual, player-controlled version of Flappy Bird and scripts to train a neural network agent to play and improve over generations.

---

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Directory Structure](#directory-structure)  
4. [Dependencies](#dependencies)  
5. [Installation & Setup](#installation--setup)  
6. [How to Play (Manual Mode)](#how-to-play-manual-mode)  
7. [AI Training (NEAT)](#ai-training-neat)  
8. [Watching the Trained Agent](#watching-the-trained-agent)  
9. [Adjustable Parameters](#adjustable-parameters)  
10. [Customization](#customization)  
11. [Credits](#credits)  

---

## Overview

This project recreates the classic Flappy Bird experience using Pygame and extends it with an AI “bird” that learns to play by itself. The AI is trained via NEAT-Python:  
- **Manual Game**: Press Space to flap and navigate the bird through oncoming pipes.  
- **AI Training**: The NEAT algorithm evolves a population of neural networks over many generations. Each “genome” controls its own bird; fitness is based on how many pipes it passes. As the score increases, pipe speed gradually ramps up.  

---

## Features

- **Classic Flappy Bird Mechanics**  
  - The bird has gravity, can “flap” to rise, and must avoid colliding with pipes.  
  - Score increments by 1 for every pipe passed.  
  - Every time the score is a multiple of 5, pipe movement speed increases by 20% (×1.2).  

- **High-Resolution, Scaled Assets**  
  - Custom-sized background, bird, and pipe images that scale to a 600×800 game window.

- **AI Training with NEAT**  
  - Uses `neat-python` to evolve neural networks over generations.  
  - Each generation: a population of birds “play” simultaneously; those that survive longer (pass more pipes) get higher fitness.  
  - The best genome is saved (`best_flappy_genome.pkl`) for later evaluation.

- **Watch Mode**  
  - After training finishes, load the saved genome to watch a single bird controlled by the trained network.  

- **Adjustable Difficulty**  
  - Initial pipe speed can be changed in `pipe.py` or overridden in `main.py`.  
  - Automatic speed scaling as score increases.

---

## Directory Structure

YourProject/
│ README.md
│ config-feedforward.txt ← NEAT configuration (handles activation, mutation, etc.)
│ train.py ← Script to train AI using NEAT
│ watch.py ← (Optional) Script to load & watch best-trained agent
│
├── assets/ ← All PNG assets
│ ├─ bg.png
│ ├─ bird.png
│ └─ pipe.png
│
├── src/ ← Source code for game logic
│ ├─ bird.py ← Bird class: physics (gravity, flap, tilt), drawing, collision mask
│ ├─ pipe.py ← Pipe class: random gap generation, movement, collision logic, PIPE_SPEED variable
│ └─ main.py ← Manual game loop: player input, drawing, score handling, speed ramp-up
│
└── .venv/ ← Python virtual environment (ignored in version control)