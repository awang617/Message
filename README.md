# Message
Message is an ecommerce website that sells bouquets and plants based on the language of flowers. Visitors of the site can take a personality quiz for fun and browse the shop. If they want to write a review or buy products, they will be invited to log in or sign up for an account. After they have logged in, users are free to browse the site with ease and also view their profile to see past orders and reviews.

http://iris-message.herokuapp.com/

## Technologies Used
- HTML
- CSS
- Javascript, jQuery
- Python, Flask
- Peewee, Postgres, SQLite
- Bootstrap
- Bulma
- Chart.js

## Running this Project
To run this project make sure all dependencies are installed in virtualenv using `pip3 install -r requirements.txt`:
1. Uncomment the try-except block in `app.py`
2. Run `python3 app.py`
3. Open localhost:8000

## Inspiration
My inspiration from this project sprung from a book I read once called The Language of Flowers (Vanessa Diffenbaugh). The main character of the book started a florist business called Message, and she used the language of flowers to arrange her bouquets. The idea of using the language of flowers for a floral arrangement business was very intriguing to me and something I wish actually existing. My app, Message, was built as a mockup for how this character might make an online presence for her business.

## Wireframes
![](https://trello-attachments.s3.amazonaws.com/5c9e4637f5576c5cf941a49b/5caedbdd6fe8fd34cf61b1f4/dde3a2ca8245d21fcdd57a1932b7ce57/index.jpg)

This loosely based mockup for the landing page of the website.

## Database Structure and ERD

![](https://trello-attachments.s3.amazonaws.com/5c9e4637f5576c5cf941a49b/5c9e5af7bb914116866458cf/5b29ec943faebe19fb9c4c279d86e51e/IMG_5480.jpg)

The database for this project utilize six different tables. A user has an order, which has order details that I also used to store information for the shopping cart. 

## Challenges and Wins
Some challenges (and wins) with this project were:
- Adding and subtracting items from the cart
- UI for the personality quiz
- Render a chart for ratings for a product
- Redirect users to appropriate pages based on where they were previously

The core functionality for this site is to be an ecommerce site where users can buy products. I had to find a way to make it easy for users to add and take items out of their cart and keep the experience loyal to how online vendors function. Although the concept was rather simple, there were a few different entries in the database that needed to be changed when a user added or removed items. I also wanted to add a chart to the product page that would show the number of reviews for a given rating. I used Chart.js for the chart, but grabbing the numbers from the database was difficult. I wrote a separate route in my app file for an ajax call that sent back the numbers for each rating of that particular product.

Designing and fixing the UI was also a challenge with this project. With the personality quiz, there were a lot of different pieces that had to be knit together to create a more seamless experience for the user. Although it would be easier to implement a single page quiz where all the questions and answers are althogher, I wanted to make the quiz flip through the questions automatically as the user answers each question.

## Code snippets
![](https://trello-attachments.s3.amazonaws.com/5c9e4637f5576c5cf941a49b/5cb0211dca5181560a7272ed/d7fa10b7f7b6fdc2d643ec7a3b7bb9ab/Screen_Shot_2019-04-11_at_9.36.18_PM.png)

![](https://trello-attachments.s3.amazonaws.com/5c9e4637f5576c5cf941a49b/5cb0211dca5181560a7272ed/ea4315fc48a8ffc2b6522df4ad88a6dc/Screen_Shot_2019-04-11_at_9.38.32_PM.png)

## Future Developments
Given the scope and time frame of this project, there are some feature I would like to continue working on. I would like to implement some kind of search feature with a language of flowers dictionary that users could browse separately from the shop. I would also like to enable users to purchase from the site without signing up for an account, since not all ecommerce sites make signup mandatory. 


