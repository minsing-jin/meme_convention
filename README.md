
# 👾Meme convention

> _"Needed explaining, That humor flopped."_  
>  — Youtuber Shuka World-

This repository is a randomly autocomplete of meme for developers and researchers fit context.
It is designed to make writing more engaging and fun by suggesting memes that are relevant to the content being written.
This repository is backend of the meme convention and autocomplete for developers and researchers when they write something in specific situation.

# 📖 Table of Contents
- [👾Meme convention](#-meme-convention)
- [⚡️ Quick Start](#quick-start)
- [🪐 Motivation](#-motivation)
- [🔑 Key Features](#-key-features)
- [🤷 How to use this repository](#-how-to-use-this-repository)
- [🤾 How to contribute](#-how-to-contribute)
- [🚗 Roadmap](#-roadmap)
- [📜 License](#-license)
- [📫 Contact](#-contact)

# ⚡️ Quick Start
1. Git clone this repository
```bash
git clone https://github.com/minsing-jin/meme_convention.git
```
2. Change directory to the cloned repository
```bash
cd meme_convention
```

3. Run the following command to install the required packages
```bash
uv sync
```

```bash
uv run ./meme_convention/main.py
```

4. When meme convention is running, you can use the meme recommend feature and meme add feature.
```bash
1. meme recommend : shift + ctrl or cmd + M
2. meme add : shift + ctrl or cmd + A 
After that, if you drag and drop a meme image to the text area, it will be added to the local db.
```

# 🪐️ Motivation

<p float="left">
  <img src="resources/readme/sleep_clap.gif" width="250" />
  &nbsp; <!-- adds spacing -->
  &nbsp;&nbsp;&nbsp;
  <img src="https://github.com/user-attachments/assets/0c5074ef-d235-4a70-9292-9c33c3fb8dcc" width="180" />
  &nbsp;&nbsp;&nbsp;
  <img src="resources/readme/koojacheol_why.gif" width="280" />
</p>

1. Many developer and researcher write in many situations. But their writing is not engaging and fun.
2. In code reviews or issue discussions, plain text can come off as cold—like a robot wrote it—and might accidentally hurt someone's feelings or spark misunderstandings.
3. I believe that memes can help to make writing more engaging and fun, and can also help to clarify(???) the meaning of the text.

I've decided to ditch the dull writing—tech writing should be fun and easy to read.
In the future, I plan to expand my project into a general platform where anyone can use memes or funny images in the right context.


# 🔑 Key Features
1. Recommendation algorithm that suggests memes based on the context of the writing.
2. User can add their own memes to the local database.
3. We can use the meme convention using the keyboard shortcut `shift + ctrl or cmd + M` to recommend memes and `shift + ctrl or cmd + A` to add memes.

- When developers write content, the meme convention can autocomplete memes based on contextual rules(It will be automated using recommendation algorithm later), making their writing more engaging and fun.
- A collection of memes related to programming and software development
- A simple and easy-to-use interface for adding and viewing memes
- A community-driven platform where users can contribute their own memes

# 🤷 How to use this repository
You can use this repository to find memes that are related to programming, software development, and other related topics.
You can also contribute to this repository by adding your own memes.

# 🤾 How to contribute
## Contributing categories
1. Add a new meme to the 'local db' directory
2. Fix a bug in the meme recommendation algorithm
3. Improve the user interface of the meme convention

## How to contribute
1. Fork this repository
2. Create a new issue for your contribution
   - If you want to add a new meme, please include the meme image and a brief description of the meme.
   - If you want to fix a bug or improve the user interface, please include a description of the bug or improvement.
3. Create a new branch `Feature/#issue_number`
4. Create pull request your changes

# 🚗 Roadmap
This project might be chrome extension or vscode extension or other editor extension.(not discussed yet)

<p align="center">
    <img src="resources/readme/dr_strange.gif" width="250">
</p>

- [x] Create a meme(I added) convention and autocomplete for developers and researchers when they write something in github situation. (Code review, issue discussion, etc.)
- [ ] Create a meme autocomplete for all developers and researchers when they write something in their code editor.
- [ ] Check people's reaction to the meme convention and autocomplete and decided to whether continue or not.(in developer)
- [ ] If this project is successful, release it as a chrome extension or vscode extension to expand its reach and usability.
- [ ] Add many genre of meme such as sports, movies, game, animation.... to make sympathize with more people.
- [ ] Create a meme autocomplete for all writing long form writing. This step meme can be used in many blogs, articles and other places.
- [ ] Create a meme convention for all people. This step meme can be used in social media, forums and other places.
- [ ] Optimize the meme autocomplete recommendation algorithm to make it more accurate and relevant user-friendly.
- [ ] Expand the meme collection to include more diverse and inclusive memes that resonate with a wider audience.
- [ ] Create meme community webpage where users can easily search adn upload memes in various context.
- [ ] Expand the picture recommendation algorithm to include more diverse and inclusive images that resonate with a wider audience.
- [ ] Create a community-driven platform where users can contribute their own memes and share them with others.

# 📜 License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

# 📫 Contact
If you have any questions or suggestions, feel free to contact me at [email](mailto:developermisning@gmail.com)