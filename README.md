# Bear Console
<p align="center">
    <figure>
        <img src='logo/logoBear.png'/>
    </figure>
</p>

This project is dedicated to implement the logic and  visual representations of paper games using Python and pyQt5. Each game is compose of 2 main elements: 

1. [Game logic](https://github.com/jrojas9206/ClassicGames/tree/main/src/bearconsole/games)
2. [Ui-Widget](https://github.com/jrojas9206/ClassicGames/tree/main/ui) 

This project is a hobby, it continue active and I hope along this year (2024 - 2025) I will be able to implement more games and to improve the visuals, add some music and better animations as for the moment it more like a skeleton.  The main UI can be seen in Figure 1.

<p align="center">
    <figure>
        <img src="logo/mainUI.png" width=300 />
        <figcaption><b>Figure 1.</b> Main console</figcaption>
    </figure>
</p>

The games can be run also on the terminal. An example of the game running in the console can be seen in figure 2.

<p align="center">
    <figure>
        <img src='logo/tictacToe_terminal.png' width=300/>
        <figcaption><b>Figure 2.</b> TicTacToe Running on terminal</figcaption>
    </figure>
</p>

## 1. Implemented games

Currently, the platform offers the following games:

 - TicTacToe 
 - Hangman 
 - DotAndBoxes 

## Installation 

1. Create a virtual environment to install the project.

```bash
    python -m venv .bearconsole
```

2. Activate your virtual environment 

- GNU/Linux

```bash
    source .bearconsole/bin/activate 
```

-  Windows 

```bash
    ./bearconsole/Scripts/activate 
```

3. Install the build module 

```bash
    python -m pip install build
```

4. Build the project 

```bash 
    python -m build
```

5. Install the project 

```bash
    python -m pip install -e .
```

6. Run the app Qt/Terminal

- Terminal  

```bash
    python ./terminal_app.py 
```

- Qt app  

```bash
    python ./terminal_app.py 
```