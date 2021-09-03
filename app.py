if __name__ == "__main__":
    # this dotenv should be loaded and called first
    # had to place it here because autoformatting of the code places
    # it below the other modules
    # meaning some modules will end up not getting env variables
    from dotenv import load_dotenv

    load_dotenv()

    from flask_restful import Api
    from views import TotalSessions

    from constants import config
    from application import application

    api = Api(application, catch_all_404s=True)

    api.add_resource(TotalSessions, "/api/v1/total-sessions")
    # api.add_resource(LogComplexSearch, "/search-complex/v1/<string:expression>")

    application.run(host="0.0.0.0", debug=False)
