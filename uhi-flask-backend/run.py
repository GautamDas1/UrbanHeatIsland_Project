from app import create_app

# Initialize Flask app
app = create_app()

if __name__ == "__main__":
    # Run on localhost:5000 with debug mode enabled
    app.run(debug=True, host="127.0.0.1", port=5000)
