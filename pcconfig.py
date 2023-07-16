import pynecone as pc

class SimpleConfig(pc.Config):
    pass

config = SimpleConfig(
    app_name="simple",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
    port=3000
)