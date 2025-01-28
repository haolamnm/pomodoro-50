# Pomodoro 50

<div>
	<img src="./app/static/img/preview.png" alt="Screenshot of the Pomodoro 50 app home page" width="100%" title="Screenshot of the Pomodoro 50 app home page">
</div>

[![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/haolamnm)
[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=flat&logo=paypal&logoColor=white)](https://paypal.me/haolamnm)
[![Ko-Fi](https://img.shields.io/badge/Ko--fi-F16061?style=flat&logo=ko-fi&logoColor=white)](https://ko-fi.com/haolamnm)
[![GitHub Sponsor](https://img.shields.io/badge/GitHub%20Sponsors-%23121011.svg?style=flat&logo=github&logoColor=white)](https://github.com/sponsors/haolamnm)

First of all, This is my project for CS50x 2024.

Welcome to Pomodoro 50! A Flask web application that helps you manage your study session. The difference between Pomodoro 50 and other Pomodoro timers is that Pomodoro 50 is a 50-minute timer, not a 25-minute timer. Yes, you read that right! I found that 25 minutes is too short for me to focus on my work, so I decided to make a 50-minute timer instead.

But that's not all! The key feature of Pomodoro 50 is that it has an AI assistant that will motivate you when you intentionally pause your work session for bad reasons.

In conclusion, with Pomodoro 50, you can:
+ Start your study session.
+ Have your to-do list.
+ Have your own account that will track your progress throughout the year.
+ Have an AI assistant that will motivate you when you intentionally pause for bad reasons.

## Getting Started

### 1. Online access

You can access the website at [Pomodoro 50](https://pomodoro-50.vercel.app/home).

### 2. Local setup

1. Folk the repository.

2. Clone the repository.
```bash
git clone https://github.com/haolamnm/CS50x-project.git
```

3. Install the required packages.
```bash
pip install -r requirements.txt
```

4. Set the environment variables.

> Create a `.env` file in the root directory. Take a look at the `.env.example` [here](./app/logs/.env.example) file for the required environment variables.

5. Run the application.

Connect to the local session system
```bash
python dev.py
```

Connect to the Redis cache session system
```bash
python run.py
```

## How to use

Start by create your own account via the [register](https://pomodoro-50.vercel.app/signup/email/) page. The UI is pretty straightforward, so you should be able to navigate through the website easily.

<div align="center">
	<a href="https://youtu.be/HSemsQzqEoQ" target="_blank">
		<img src="https://img.youtube.com/vi/HSemsQzqEoQ/0.jpg" alt="Pomodoro 50 demo video" width="100%" title="Pomodoro 50 demo video">
	</a>
</div>

## Inspiration

I was inspired by the actual Pomodoro I used to study which is [Pomofocus](https://pomofocus.io/app). It was a great tool, but it offers a premium feature which shows the statistics of your study session. I thought it would be a great idea to make my own version. Besides, I also learned about AI and thought it would be cool to have a mini AI assistant that motivates you when you pause your work session for some kind of bad reason.

## Technical Stack

0. **Python**: I used Python 3.13 for this project. [Python](https://docs.python.org/3/).
1. **Flask**: For routing and backend. [Flask](https://flask.palletsprojects.com/en/stable/).
2. **PostgreSQL**: I used Supabase as the database, [Supabase](https://supabase.com/).
3. **Redis**: I used Redis to store the session data, [Upstash](https://upstash.com/).
4. **Vercel**: I used Vercel to deploy the website, [Vercel](https://vercel.com/).
5. **Pytest**: I wrote lots of unit tests for this project.
6. **Gemini**: I used Gemini for the AI assistant, [Gemini](https://ai.google.dev/gemini-api/docs).

## For Developers

If you want to contribute to this project, feel free to fork the repository and make a pull request. I would love to see your contribution!

Email: [haolamnm.work@gmail.com](mailto:haolamnm.work@gmail.com).

GitHub: [@haolamnm](https://github.com/haolamnm).

LinkedIn: [@haolamnm](https://www.linkedin.com/in/haolamnm/).

---
