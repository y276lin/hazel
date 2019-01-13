# Hazel

:smile_cat:Hazel is a chatbot that reminds you to complete your tasks online and keep your days organized.

**Naming Inspiration**

> I own 2 cats: Hazel & Siri. Since Apple has coined the term Siri, I decided to name my chatbot Hazel.

> Watch out Apple. :apple:

## Demo

- [Full Demo Video](https://github.com/y276lin/hazel/blob/master/demo/demo.mp4?raw=true)

<div align="center" width="100%">
  <img align="center" src="https://github.com/y276lin/hazel/blob/master/demo/demo.gif?raw=true" width="30%"/>
</div>


## Features

- WeChat Support
- Automatically parse

## Technology Used

- Rasa, Spacy, Sklearn, SVM

## Conversation Transcript - Creation Flow

```diff
+ Hey
- Hi, I'm Hazel, your personal reminder. Let's start with create or review your notes
+ Hello
- Hi, I'm a bot to remind you!
+ I want to create a new task
- Let's get started. May I have a brief description from you?
+ video conference
- tomorrow 4pm, with Chloe
+ <Description>: video conference
+ <Detail>:
+ tomorrow 4pm, with Chloe
+ <People>: Chloe
+ <Deadline>: 2019-01-14 16:00:00
+ Please confirm the information.
- yes
+ Good to go!
```


