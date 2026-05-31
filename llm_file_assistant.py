import os
import json

from dotenv import load_dotenv
import google.generativeai as genai

from fs_tools import (
    read_file,
    list_files,
    write_file,
    search_in_file
)

load_dotenv()

genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-pro"
)

tool_map = {

    "read_file": read_file,

    "list_files": list_files,

    "write_file": write_file,

    "search_in_file": search_in_file
}

while True:

    query = input(
        "\nAsk: "
    )

    if query.lower() == "exit":
        break

    if "read all resumes" in query.lower():

        files = list_files(
            "resumes"
        )

        for file in files:

            path = (
f"resumes/"                f"{file['name']}"
            )

            result = read_file(path)

            print(
                "\n========="
            )
            print(
                result["filename"]
            )
            print(
                result["content"]
            )

    elif "python" in query.lower():

        files = list_files(
"resumes"        )

        for file in files:

            path = (
f"resumes/"                f"{file['name']}"
            )

            result = search_in_file(
                path,
                "Python"
            )

            if result["count"]:

                print(
                    file["name"]
                )
                print(
                    result["matches"]
                )

    else:

        response = model.generate_content(
            query
        )

        print(
            response.text
        )