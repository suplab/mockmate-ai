#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-lite.txt
echo "\n✅ Setup complete. To start the app:\nstreamlit run app.py"
