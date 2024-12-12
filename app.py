import os
import py_eureka_client.eureka_client as eureka_client
from flask import Flask

from api.v1.routes import routes


app = Flask(__name__)
app.register_blueprint(routes)
port = int(os.environ.get('PORT', 8050))
eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="ocr-service-py",
                   instance_port=port)

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=port)