# 🌹 RoseBot

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![aiogram](https://img.shields.io/badge/aiogram-3.x-green?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/MongoDB-4.7.2-green?style=for-the-badge&logo=mongodb)

RoseBot is an engaging Telegram bot built with Python using the asynchronous **aiogram** framework and **MongoDB** for persistent data storage. The bot features interactive game mechanics centered around growing and managing virtual flowers like roses and peonies.

## ✨ Features

*   **Interactive Game Mechanics:** Engage users with a unique flower-growing game.
*   **Asynchronous & High-Performance:** Built on `aiogram` to handle many users concurrently without blocking.
*   **Persistent Data Storage:** User progress, inventory, and settings are securely stored in a MongoDB database.
*   **Modular and Clean Code:** The project is organized into logical modules for easy maintenance and scalability.

## 📂 Project Structure

The repository is structured to separate concerns, making the codebase clean and understandable.

```
.
├── app/
│   ├── db_utils.py         # Utility functions for database interactions (CRUD operations).
│   ├── game_mechanics.py   # Core logic for the flower-growing game.
│   ├── handlers.py         # Message and callback query handlers for the bot.
│   ├── keyboards.py        # Functions to generate inline and reply keyboards.
│   ├── peonies.py          # Module related to 'peony' flower logic (if separate from rose).
│   ├── rose.py             # Module containing the main 'rose' flower logic.
│   └── text_utils.py       # Helper functions for formatting text messages.
│
├── config.py               # Handles loading configuration from environment variables.
├── rosebot.py              # The main entry point to start the bot.
├── utils.py                # General utility functions used across the project.
│
├── LICENSE                 # Project license file.
├── README.md               # You are here!
└── requirements.txt        # (Recommended) A file listing all project dependencies.
```

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine or server.

### Prerequisites

*   Python 3.9+
*   Git
*   A MongoDB database instance (local or cloud-based like MongoDB Atlas)

### 1. Clone the Repository

```bash
git clone https://github.com/regw1d/RoseBot.git
cd RoseBot
```

### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python libraries. It's best practice to have a `requirements.txt` file. You can create one with `pip freeze > requirements.txt`.

```bash
pip install -r requirements.txt
```
If you don't have a `requirements.txt` file yet, install the core libraries:
```bash
pip install aiogram pymongo python-dotenv
```

### 4. Configure Environment Variables

Create a file named `.env` in the root directory of the project and add the following configuration.

```env
# Get this token from @BotFather on Telegram
BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# Your MongoDB connection string
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
MONGO_DB_NAME="RoseBotDB"
```
**Important:** Never commit your `.env` file to version control! Add it to your `.gitignore` file.

### 5. Run the Bot

Execute the main script to start the bot.

```bash
python rosebot.py
```

## Usage

Once the bot is running, you can interact with it on Telegram. Here are some example commands (you should update this section with your actual commands):

*   `/start` - Check bot work.
*   `/rose` - Get roses on your balance.
*   `/help` - Get a list of available commands.

## 📄 License

This project is licensed under the [Your License Name Here] - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Author: **@regwid1337** on Telegram

If you wish to use this code in your own project, please contact me first.
