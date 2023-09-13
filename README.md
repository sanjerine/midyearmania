# Mid-Year Mania 🏆 - Gambling Interface

![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white) ![Django](https://img.shields.io/badge/django-%104C34.svg?style=for-the-badge&logo=django&logoColor=white) ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

## Overview

Every mid-semester break I run a small tournament with my friends where we are sorted into teams and compete in a variety of events, with the highest scoring team being crowned the winner. What better way to 'spice up' competition than to introduce a friendly, gambling aspect? :grin:

I decided to build a website to allow users to 'gamble' with their points on the outcomes of other events. Markets are dynamic, with odds changing depending on the liquidity of an event. When an event's time concludes, it is unable to be wagered on. Users are sorted into teams, and the status of each team is displayed on the homepage as the event runs. The wninning team is the team with the highest average points!

📸 **Screenshots**:

![Home Page](/screenshots/home.PNG)
![Leaderboard](/screenshots/leaderboard.PNG)
![Dropdown](/screenshots/dropdown.PNG)
![Bets](/screenshots/bets.PNG)
![Event Page](/screenshots/event.PNG)
![Admin Panel](/screenshots/admin.PNG)

## Features

- **Dynamic Betting Market**: Market system calculates and distributes payouts. Winners receive their rewards as a percentage of the available betting pool, ensuring dynamic odds and payouts that reflect the community's sentiments.
- **Data-Validated Betting**: Data validation mechanisms are in place to prevent arbitrage betting, ensuring fair play and maintaining the integrity of the gaming experience.
- **Leaderboards & Statistics**: Track top players, view team and event statistics, and gain insights into the betting patterns and strategies of the community.
- **Admin Panel**: Allows easy updating of all data - models saved back propagate through and update statistics automatically when a match winner is added.

## Technology Stack

- **Backend**: Django (Version: 4.2.5)
- **Database**: MySQL
- **Frontend**: Bootstrap
- **Deployment**: A2Hosting 

## Installation & Setup

1. **Clone the Repository**:
```bash
git clone https://github.com/sanjerine/midyearmania.git
cd midyearmania
```

2. **Set up a Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up the Database**:
   - Modify the `DATABASES` settings in `settings.py` according to your database setup.
     - You may have to create a new MySQL database.
   - You will have to add example/filler teams and players using Django Admin interface such that the Jinja templates render correctly.
   - Run migrations:
```bash
python manage.py migrate
```

5. **Run the Server**:
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.