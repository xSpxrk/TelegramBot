from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

greeting_template = env.get_template('greeting.txt')
weather_template = env.get_template('weather.txt')
user_template = env.get_template('user.txt')


def load_greeting_template(name, bot_name):
    return greeting_template.render(name=name, bot_name=bot_name)


def load_weather_template(*weather):
    return weather_template.render(temp=weather[0], feels_like=weather[1], wind=weather[2])


def load_user_template(first_name, last_name, username, id):
    return user_template.render(first_name=first_name, last_name=last_name, username=username, id=id)