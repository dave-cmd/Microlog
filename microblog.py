from app import app, manager, db, cli
from app.model import People, Post

@app.shell_context_processor
def make_shell_context():
    return {"db":db, "People":People, "Post":Post}


if __name__=="__main__":
    app.run(debug=True)
    #manager.run()