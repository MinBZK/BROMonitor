import uvicorn


# Script used to run fastAPI backend in debug mode.

# Use 'debug current python file' mode in visual studio code on this file.

# Make sure correct environment is activated


if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, debug=True)
