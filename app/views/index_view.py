from flask_classful import FlaskView


class IndexView(FlaskView):
    def index(self):
        """
        Tweak later..
        :return: Hello World
        """
        return 'Hello World!'
