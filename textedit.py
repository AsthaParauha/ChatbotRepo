 
# editing the text of this.txt
with open ("this.txt", "r") as f:
    text=f.read()
    if ('{' in text):
        contant=text.replace('{', '''{
        "tag": "operator",
        "patterns": [
            "What is a operator",
            "operator in python",
            "python operator",
            "Explain operator in python"
        ],
        "responses":''')
        with open("this.txt", "w") as j:
            j.write(contant)
    else: 
        print("{ is not there")
print("work is done.")