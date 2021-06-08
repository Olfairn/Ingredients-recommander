This project result is availible [here](http://spice-it-up.win/).

## ABOUT

The website is the result of a 1-week final project from a Data Science Bootcamp at SPICED Academy. 

It is based on <b>40 000 recipes</b> provided by Yummly - data availiable on Kaggle
        
Although it is working, it should be considered as an MVP, as the model, and therefore the matching could be greatly improved. 

I don't even mention the website: I am not a web dev, and I basically "learned" it while building it. 
It's actually closer to a "collage" with a w3 background than a website So beware dev fellows if you have a look at the code source, you're likely to see many forbidden things!
        
The model was written in Python, and is actually a "simple" cosine similarity, measuring the likelihood appearance of each ingredient with one another. For multiple ingredients, I averaged the cosine (the model's biggest drawback).
        
The website hosted by Heroku, directly from a Git Repo. The model is availiable in the "model folder", and the rest is in "app"

If you have a better idea on how to use cosine similarity with multiple ingredients, or simply want to get in touch with me, don't hesitate to send me a message on [Linkedin!](https://www.linkedin.com/in/florianmarandet/)