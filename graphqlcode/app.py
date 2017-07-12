#!/usr/bin/env python



from flask import Flask

#from database import db_session, init_db
from flask_graphql import GraphQLView
from schema import schema
#import agent_info as agent
#import variables

app = Flask(__name__)
app.debug = True

# default_query = '''
# {
#   allEmployees {
#     edges {
#       node {
#         id,
#         name,
#         department {
#           id,
#           name
#         },
#         role {
#           id,
#           name
#         }
#       }
#     }
#   }
# }'''.strip()


app.add_url_rule('/graphql.json', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.teardown_appcontext
def shutdown_session(exception=None):
    #db_session.remove()
    pass

if __name__ == '__main__':
    #init_db()
    #host = variables.host
    app.run(debug=True, host='0.0.0.0', port=80)
    #agent.checkConnection("%s"%host)

