# About

This is a new form of my existing Agents Library in response to much of my workflow using llama.cpp more.
This is a client side helper for running models from a llama.cpp server.

Please see the various demo files to see how to use the features of the library.
This library is not a pip package yet so Agents2.py will need to be in the same directory as the rest of the code.

This project will be periodically updated.
Any feedback, suggestions, or collaboration is welcome!

# Installation
```
git clone https://github.com/Rohan-Bhargava/Agents2.git
cd Agents2
```

# Usage

Please see the various demo files that show how to use these modules.
All demo files assume that a llama.cpp server is running a model (llama-cli.exe etc.) on localhost or 127.0.0.1 on port 8080.
Enter in "/MENU" to access a developer menu.

# Features

## Single Agent Chat
A relatively normal chat style interface with a single agent.

## Multi Agent Chat
An experimental feature that puts a twist on the classic chat style interface.

Instead of one agent, multilpe agents will respond to your prompt!
For each prompt, each agent will respond independent of each other! i.e. each of the agents' individual responses will be buffered temporarily and not fed right away into the shared context.
This is to prevent the common issue of the agents' influencing each other.
After each agent has given their response, all the responses are added to a shared context and the cycle starts again.

## Round Table

This feature has two "sub-modes":
1. Autononmous Debate
2. Round Table Chat

### Autononmous Debate

Give the agents a question and watch them debate it out!
One can specify how many rounds the agents all debate for.

### Round Table Chat

Very similar to Multi Agent Chat but for each prompt the agents will discuss for N rounds.
I would recommend that each agent has their temperature set higher than usual.
This is because as the context grows, LLMs will want to converge to a "mean" and might end up all agreeing with each other.
If that is not the end-goal or a desired outcome, higher temperature can help mitagate, but not entirely prevent this inevitability.

## RAG

A barebones RAG engine is also built in and has a demo file showing its usage.